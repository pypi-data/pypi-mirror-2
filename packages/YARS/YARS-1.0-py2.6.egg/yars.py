"""
YARS - yet another RSS downloader

    by W-Mark Kubacki; wmark@hurrikane.de
    licensed under the terms of the RPL for non-commercial usage
"""

from threading import Thread
import random

import feedparser
from redis import Redis
import redis.exceptions

__all__ = ['YARS']
__author__ = "W-Mark Kubacki; wmark@hurrikane.de"
__version__ = "1.0"

def merge(comparator, left, right):
	"""Merges two sorted lists."""
	result = []
	i, j = 0, 0
	while i < len(left) and j < len(right):
		if keyf(left[i]) <= keyf(right[j]):
			result.append(left[i])
			i += 1
		else:
			result.append(right[j])
			j += 1
	result += left[i:]
	result += right[j:]
	return result

def multi_merge(keyf, items_list):
	"""Merges an arbitrary number of sorted lists."""
	result, remainder = items_list[0], items_list[1:]
	for l in remainder:
		result = merge(keyf, result, l)
	return result

def string_contains_all(haystack, needles):
	for needle in needles:
		if not needle in haystack:
			return False
	return True

def string_contains_any(haystack, needles):
	for needle in needles:
		if needle in haystack:
			return True
	return False

#######################################################
class YARS(object):

	def __init__(self, redis, prefix, verbose=False):
		self.db = redis
		self.prefix = prefix
		self.verbose = verbose

	@classmethod
	def feed_entry_id(cls, feed_entry):
		"""Guaranteed to get an ID for a given feed entry."""
		if 'id' in feed_entry:
			return feed_entry['id']
		return feed_entry['link']

	@classmethod
	def sieve_feed_entries(cls, feed_entries, lastpos):
		"""Removes entry with ID 'lastpos' and every entry after that."""
		if not lastpos:
			return feed_entries
		else:
			entries = list()
			for entry in feed_entries:
				if YARS.feed_entry_id(entry) == lastpos:
					break
				else:
					entries.append(entry)
			return entries

	def get_desired_items_from_feeds(self, show_summary=False, dry_run=False):
		if not self._check_prerequisities_for_run():
			return False
		feeds = self.get_feed_list()
		all_entries = self._get_all_new_feed_entries(feeds, dry_run)
		desired_items = self._find_desired_items_in(all_entries)
		field = 'summary' if show_summary else 'link'
		self.display_items(desired_items, field)
		return True
	run = get_desired_items_from_feeds

	def _check_prerequisities_for_run(self):
		if self.db.scard(self.prefix + '/feeds') <= 0:
			print("No feeds to download from. Exiting.")
			return False
		if self.db.scard(self.prefix + '/wanted') <= 0:
			print("No 'wanted' list for matching or list is empty. Exiting.")
			return False
		return True

	def add_feed(self, caption, url):
		n = self.db.incr(self.prefix + '/feeds/next_key')
		self.db.mset({self.prefix + '/feed/' + str(n) + '/url': url,
			      self.prefix + '/feed/' + str(n) + '/caption': caption,
			      self.prefix + '/feed/' + str(n) + '/lastpos': 0
			      })
		self.db.sadd(self.prefix + '/feeds', str(n))
		return True

	def remove_feed(self, feed_number):
		n = str(feed_number)
		if self.db.srem(self.prefix + '/feeds', n):
			for k in [self.prefix + '/feed/' + n + '/url',
				  self.prefix + '/feed/' + n + '/caption',
				  self.prefix + '/feed/' + n + '/lastpos']:
				self.db.delete(k)
			return True
		else:
			return False

	def get_feed_list(self):
		feeds = dict()
		for n in self.db.smembers(self.prefix + '/feeds'):
			caption, url = self.db.mget([self.prefix + '/feed/' + n + "/caption",
						     self.prefix + '/feed/' + n + "/url"])
			feeds[n] = {'caption': caption, 'url': url}
		return feeds

	def reset_lastpos_marks(self):
		for n in self.db.smembers(self.prefix + '/feeds'):
			self.db.set(self.prefix + '/feed/' + n + '/lastpos', 0)

	def add_item(self, caption, search_words, exclude_words=set()):
		n = str(self.db.incr(self.prefix + '/wanted/next_key'))
		self.db.set(self.prefix + '/wanted/' + n + "/caption", caption)
		for word in search_words:
			self.db.sadd(self.prefix + '/wanted/' + n + "/search_words", word)
		for word in exclude_words:
			self.db.sadd(self.prefix + '/wanted/' + n + "/exclude_words", word)
		self.db.sadd(self.prefix + '/wanted', n)
		self.reset_lastpos_marks()
		return True

	def remove_item(self, item_number):
		n = str(item_number)
		if self.db.srem(self.prefix + '/wanted', n):
			for k in [self.prefix + '/wanted/' + n + '/caption',
				  self.prefix + '/wanted/' + n + '/search_words',
				  self.prefix + '/wanted/' + n + '/exclude_words']:
				self.db.delete(k)
			return True
		else:
			return False

	def get_item_list(self):
		items = dict()
		for n in self.db.smembers(self.prefix + '/wanted'):
			caption = self.db.get(self.prefix + '/wanted/' + n + "/caption")
			search_words = self.db.smembers(self.prefix + '/wanted/' + n + "/search_words")
			exclude_words = self.db.smembers(self.prefix + '/wanted/' + n + "/exclude_words")
			items[n] = {'caption': caption, 'search_words': search_words, 'exclude_words': exclude_words}
		return items

	def cleansweep(self):
		for k in self.db.keys(self.prefix + "*"):
			self.db.delete(k)
		return True

	def _get_all_new_feed_entries(self, feeds, dry_run=False):
		items = list()
		getter = list()
		for n in feeds:
			g = FeedItemsGetter(self.db, self.prefix, self.verbose, feeds[n], n, dry_run)
			getter.append(g)
			if self.verbose: print "Starting fetching for feed %s." % feeds[n]['caption']
			g.start()
		for g in getter:
			g.join()
			if g.successfull():
				items.append(g.get_items())
			elif self.verbose:
				print "ERROR while parsing feed %s: %s." % (g.feed['caption'], g.error)
		return multi_merge(lambda e: e['updated_parsed'], items)

	def _find_desired_items_in(self, all_items):
		todo = list()
		desired = self.get_item_list()
		for n in desired:
			for item in all_items:
				if string_contains_all(item['title'], desired[n]['search_words']) \
				and not string_contains_any(item['title'], desired[n]['exclude_words']):
					todo.append((desired[n]['caption'], item))
		return todo

	def display_items(self, desired_items, field):
		if len(desired_items) > 0:
			for item in desired_items:
				print item[1][field]

class FeedItemsGetter(Thread):

	items = list()
	error = False

	def __init__(self, db, prefix, verbose, feed, feed_n, dry_run=False):
		Thread.__init__(self)
		self.db = db
		self.prefix = prefix
		self.verbose = verbose
		self.feed = feed
		self.feed_n = feed_n
		self.dry_run = dry_run

	def run(self):
		f = feedparser.parse(self.feed['url'])
		if 'bozo_exception' in f:
			if self.verbose: print "!",
			self.error = f['bozo_exception'].reason
		else:
			if self.verbose: print ".",
			# ... get and renew last parsed position
			lastpos = self.db.get(self.prefix + "/feed/" + self.feed_n + "/lastpos")
			# if the current last position has changed, update it (otherwise skip that pointless write to DB)
			if not self.dry_run and not ( lastpos and lastpos == YARS.feed_entry_id(f['entries'][0]) ):
				self.db.set(self.prefix + "/feed/" + self.feed_n + "/lastpos", YARS.feed_entry_id(f['entries'][0]))
			# ... skip entries we have parsed on previous runs
			self.items = YARS.sieve_feed_entries(f['entries'], lastpos)

	def successfull(self):
		return not self.error

	def get_items(self):
		return self.items

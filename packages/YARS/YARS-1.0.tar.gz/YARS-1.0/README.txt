YARS - Yet Another RSS downloader
==================================

:Author: W-Mark Kubacki <wmark+yars@hurrikane.de>

Finds new files (called 'items') on a set of RSS feeds.

You can get help pages for every command by appending ``-h``. I.e.:

   yars add feed -h

Example usages:
~~~~~~~~~~~~~~~~

Download everything:

   yars run | xargs -r wget

Display images from referenced pages:

   yars run | xargs -r wget -q -O - | grep -o -E 'http[^"]*\.jpeg'

Download torrents, get files by ctorrent, finally delete torrents:

   yars run | grep -F '.torrent' | tee newfiles | xargs -r wget \\
    && cat newfiles | xargs -r -L 1 ctorrent -E 1.5 -a \\
    && cat newfiles | xargs -r rm && rm newfiles

Example scenario for quickstart:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a new feed:

   yars add feed \\
    "Dilbert Strips" "http://feeds.dilbert.com/DilbertDailyStrip"

Add a new item:

   yars add item --search-words "Comic for" "part of comics' caption"

Download images from the feeds' summary:

   yars run --summary | grep -o -E 'http[^"]*\.gif' | xargs -r wget

Most probably you will want to use ``--prefix "comics"`` for all
these commands to separate them i.e., from podcasts.

License
~~~~~~~~

Licensed under the RECIPROCAL PUBLIC LICENSE, Version 1.1 or later
(the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at
http://www.opensource.org/licenses/rpl.php

In addition to the License you agree on notifying the Author by email
about changes you publish within two weeks. You notification has to
contain a link to the publication or you must sent the Author a copy
of the publication. You have to add the changes (either as patch or
a new distribution, whatever you published) as attachment to that
notification email.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

Contact & Bug reports
~~~~~~~~~~~~~~~~~~~~~~

W-Mark Kubacki <wmark+yars@hurrikane.de>

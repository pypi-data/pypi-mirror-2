# Copyright (c) 2010, Robert Escriva
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Firmant nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


'''Default settings used within Firmant.

It is not generally safe to omit any of these settings.  Change or update them
if necessary.
'''


from firmant import routing as r
from firmant.routing import components as c


PARSERS = {'feeds': 'firmant.parsers.feeds.FeedParser'
          ,'posts': 'firmant.parsers.posts.PostParser'
          ,'tags': 'firmant.parsers.tags.TagParser'
          ,'static': 'firmant.parsers.static.StaticParser'
          }
CONTENT_ROOT = 'testdata/pristine'
FEEDS_SUBDIR = 'feeds'
POSTS_SUBDIR = 'posts'
TAGS_SUBDIR = 'tags'
STATIC_SUBDIR = 'static'
REST_EXTENSION = 'rst'
WRITERS = ['firmant.writers.j2.Jinja2PostArchiveAll'
          ,'firmant.writers.j2.Jinja2PostArchiveYearly'
          ,'firmant.writers.j2.Jinja2PostArchiveMonthly'
          ,'firmant.writers.j2.Jinja2PostArchiveDaily'
          ,'firmant.writers.j2.Jinja2PostSingle'
          ,'firmant.writers.atom.AtomFeedSingle'
          ,'firmant.writers.static.StaticWriter'
          ]
POSTS_PER_PAGE = 10
TEMPLATE_DIR = 'testdata/pristine/templates'
URLS = [c.Type('post') /c.pageno
       ,c.Type('post') /c.year/c.pageno
       ,c.Type('post') /c.year/c.month/c.pageno
       ,c.Type('post') /c.year/c.month/c.day/c.pageno
       ,c.Type('post') /c.year/c.month/c.day/c.slug
       ,c.Type('feed') /c.slug
       ,r.SinglePathComponent('static', str)
       ]
OUTPUT_DIR = 'build/'
PERMALINK_ROOT = 'http://test'

SIDEBAR_POSTS_LEN = 10
SIDEBAR_ARCHIVES_LEN = 5

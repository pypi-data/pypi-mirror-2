# Copyright (c) 2009-2010, Robert Escriva, Rensselaer Polytechnic Institute
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
#     * Neither the name of this project nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


'''Consume data from Twitter's stream API.
'''


import urlparse
import httplib
import base64
import datetime
import traceback
import time
import optparse
import os
import sys
import shutil
from subprocess import Popen, PIPE


def valid_stream(url, user, passwd):
    '''Return groups of lines from the HTTP response.

    A connection will be made to `url` using basic auth and the credentials
    `user` and `passwd`.  The response will be split at line boundaries (but
    not necessarily every line boundary).
    '''
    headers = {}
    headers['Authorization'] = 'Basic %s' % \
            base64.b64encode(user + ':' + passwd)
    scheme, netloc, path = urlparse.urlparse(url)[:3]

    if scheme not in ('http', 'https'):
        raise ValueError('Bad URL (not http(s))')

    conn = httplib.HTTPConnection(netloc)
    conn.request('GET', path, headers=headers)
    resp = conn.getresponse()
    # Don't go through with the connection if Twitter doesn't say OK (for some
    # reason they don't like it when you try anyways ;-))
    if resp.status != 200:
        error = 'Error connecting: %i %s' % (resp.status, resp.reason)
        raise RuntimeError(error)

    data = ''
    while not resp.isclosed():
        data += resp.read(16384)
        if '\n' in data:
            lines, data = data.rsplit('\n', 1)
            yield lines


def daemon(stream_url, user, passwd, compression=None):
    '''Loop continuously, saving data to files.
    '''
    if compression not in (None, 'bzip2', 'gzip'):
        raise RuntimeError(_('Bad compression argument'))
    file_dt = datetime.datetime.now()
    pipe = None
    if compression == 'bzip2':
        pipe = Popen(['bzip2', '--stdout'],
                     stdin=PIPE,
                     stdout=open('.current-data', 'a+'))
        out = pipe.stdin
    elif compression == 'gzip':
        pipe = Popen(['gzip', '--stdout'],
                     stdin=PIPE,
                     stdout=open('.current-data', 'a+'))
        out = pipe.stdin
    else:
        out = open('.current-data', 'a+')
    oldbackoff = 0
    backoff = 1
    count = 0
    while (1):
        try:
            stream = valid_stream(stream_url, user, passwd)
            for line in stream:
                if count > 1000:
                    oldbackoff = 0
                    backoff = 1
                    count = 0
                now = datetime.datetime.now()
                if (file_dt.hour + 1) % 24 == now.hour:
                    out.flush()
                    out.close()
                    if pipe is not None:
                        pipe.wait()
                        pipe = None
                    filename = file_dt.strftime('%Y-%m-%d-%H.json')
                    if compression == 'bzip2':
                        filename += '.bz2'
                    elif compression == 'gzip':
                        filename += '.gz'
                    shutil.move('.current-data', filename)
                    file_dt = now
                    if compression == 'bzip2':
                        pipe = Popen(['bzip2', '--best', '--stdout'],
                                     stdin=PIPE,
                                     stdout=open('.current-data', 'a+'))
                        out = pipe.stdin
                    elif compression == 'gzip':
                        pipe = Popen(['gzip', '--best', '--stdout'],
                                     stdin=PIPE,
                                     stdout=open('.current-data', 'a+'))
                        out = pipe.stdin
                    else:
                        out = open('.current-data', 'a+')
                out.write(line)
            del stream
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
        print 'Sleeping for %i seconds' % backoff
        time.sleep(backoff)
        oldbackoff, backoff = backoff, oldbackoff + backoff


def main(argv):
    '''The main function of the collection process.

    It handles pulling from the environment and command-line arguments.  The
    command-line arguments should be provided by argv.

    Run this script with '-h' or '--help' to see available options.  The
    statuses will be saved into the current directory in files of the form
    'YYYY-mm-dd-HH.json'  where each file contains the lines (status updates)
    received by the API during the particular hour.  The filename have the 'bz2'
    suffix (resp. 'gz') if the '--bzip2' (resp. '--gzip') options are specified.

    In the event of failure, it will backoff with the time increasing according
    to the Fibonacci sequence (normal ``*=2`` backoff is boring).  In the future
    this should send email on failure, and automatically backfill gaps through
    the API count parameter.

    Usage instructions:

    1) Sign up for a Twitter account.
    2) On the server where data is stored, run the script.  I keep the script
       running in a screen session so that I may log in and check for errors
       easily. Thankfully errors have been few and far between.
       Be sure to specify the URL, username, and password.

    Modifications to this script:

    I advise against adding too much complexity to collection module (e.g.
    having it load to the database directly).  Should this script fail,
    collection stops.  Saving to a file first allows for all data to be recorded
    and analyzed offline.  It also avoids having to choose which fields are
    worth keeping.  Almost a year of Twitter data is less than 30GB (bzipped
    with some redundant status updates).
    '''
    parser = optparse.OptionParser()
    parser.add_option('-s', '--stream-url', dest='stream_url',
            help=_('''The http stream url.
            Overrides the TWITTER_STREAM_URL environment variable.
            '''))
    parser.add_option('-u', '--user', dest='user',
            help=_('''The username to use in the authentication process.
            Overrides the TWITTER_USER environment variable.
            '''))
    parser.add_option('-p', '--password', dest='passwd',
            help=_('''The password to use in the authentication process.
            Overrides the TWITTER_PASSWD environment variable.
            '''))
    parser.add_option('-j', '--bzip2', dest='compression',
            action='store_const', const='bzip2',
            help=_('''Compress all created files with bzip2.'''))
    parser.add_option('-z', '--gzip', dest='compression',
            action='store_const', const='gzip',
            help=_('''Compress all created files with gzip.'''))
    options = parser.parse_args(args=argv)[0]
    _stream_url = options.stream_url or \
                  os.environ.get('TWITTER_STREAM_URL') or \
                  None
    _user = options.user or \
            os.environ.get('TWITTER_USER') or \
            None
    _passwd = options.passwd or \
              os.environ.get('TWITTER_PASSWD') or \
              None
    if None in (_stream_url, _user, _passwd):
        parser.print_help()
        sys.exit(-1)
    daemon(_stream_url, _user, _passwd, options.compression)

# -*- coding: utf-8 -*-

"""
GistAPI.py -- A Python wrapper for GitHub's Gist API
(c) 2010 Kenneth Reitz. MIT License.

Example usage:

>>> Gist('d4507e882a07ac6f9f92').repo
u'd4507e882a07ac6f9f92'

>>> Gist('d4507e882a07ac6f9f92').owner
u'kennethreitz'

>>> Gist('d4507e882a07ac6f9f92').description
u'Example Gist for gist.py'

>>> Gist('d4507e882a07ac6f9f92').created_at.isoformat()
'2010-05-16T10:51:15-07:00'

>>> Gist('d4507e882a07ac6f9f92').public
False

>>> Gist('d4507e882a07ac6f9f92').filenames
['exampleEmptyFile', 'exampleFile']

>>> Gist('d4507e882a07ac6f9f92').files
{'exampleFile': u'Example file content.', 'exampleEmptyFile': u''}

>>> Gists.fetch_by_user('kennethreitz')[-1].description
u'My .bashrc configuration'
"""

import os.path
import urllib
import urllib2
from dateutil.parser import parse as dtime

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['Gist', 'Gists']

# Set your own credentials
USERNAME = 'YOUR GITHUB USERNAME'
TOKEN = 'YOUR GITHUB TOKEN'

GIST_BASE = 'http://gist.github.com/%s'
GIST_JSON = GIST_BASE % 'api/v1/json/%s'


class Gist(object):
    """Gist Object"""

    def __init__(self, id=None, json=None, username=None, token=None):
        self.id = id
        self._json = json
        self._username = username
        self._token = token

        # Map given repo id to gist id if none exists
        if self._json:
            self.id = json['repo']

        self.url = url = GIST_BASE % self.id
        self.embed_url = url + '.js'
        self.epic_embed_url = url + '.pibb'
        self.json_url = url + '.json'
        self.post_url = GIST_BASE % 'gists/%s' % self.id

    def __getattribute__(self, name):
        """Get attributes, but only if needed."""

        # Only make external API calls if needed
        if name in ('owner', 'description', 'created_at', 'public',
                    'files', 'filenames', 'repo'):
            if not hasattr(self, '_meta'):
                self._meta = self._get_meta()

        return object.__getattribute__(self, name)

    def _get_meta(self):
        """Fetch Gist metadata."""

        # Use json data provided if available
        if self._json:
            _meta = self._json
            setattr(self, 'id', _meta['repo'])
        else:
            # Fetch Gist metadata
            _meta_url = GIST_JSON % self.id
            _meta = json.load(urllib2.urlopen(_meta_url))['gists'][0]

        for key, value in _meta.iteritems():

            if key == 'files':
                # Remap file key from API.
                setattr(self, 'filenames', value)
                # Store the {current_name: original_name} mapping.
                setattr(self, '_renames', dict((fn, fn) for fn in value))
            elif key == 'public':
                # Attach booleans
                setattr(self, key, value)
            elif key == 'created_at':
                # Attach datetime
                setattr(self, key, dtime(value))
            else:
                # Attach properties to object
                setattr(self, key, unicode(value))

        return _meta

    def _post(self, params, headers={}):
        """POST to the web form (internal method)."""
        request = urllib2.Request(self.post_url,
                                  urllib.urlencode(params),
                                  headers)
        try:
            response = urllib2.urlopen(request)
        except IOError, exc:
            response = exc
        return response.code, response.msg

    def reset(self):
        """Clear the local cache."""
        if hasattr(self, '_files'):
            del self._files
        if hasattr(self, '_meta'):
            del self._meta

    def auth(self, username, token):
        """Set credentials."""
        self._username = username
        self._token = token

    def rename(self, from_name, to_name):
        """Rename a file."""
        if from_name not in self.files:
            raise KeyError('File %r does not exist' % from_name)
        if to_name in self.files:
            raise KeyError('File %r already exist' % to_name)
        self.files[to_name] = self.files.pop(from_name)
        try:
            self._renames[to_name] = self._renames.pop(from_name)
        except KeyError:
            # New file
            pass

    def save(self):
        """Upload the changes to Github."""
        params = {
            '_method': 'put',
            'login': self._username or USERNAME,
            'token': self._token or TOKEN,
        }
        names_map = self._renames
        original_names = names_map.values()
        index = len(original_names)
        for fn, content in self.files.items():
            ext = os.path.splitext(fn)[1] or '.txt'
            try:
                orig = names_map.pop(fn)
            except KeyError:
                # Find a unique filename
                while True:
                    orig = 'gistfile%s' % index
                    index += 1
                    if orig not in original_names:
                        break
            params.update({
                'file_name[%s]' % orig: fn,
                'file_ext[%s]' % orig: ext,
                'file_contents[%s]' % orig: content,
            })
        code, msg = self._post(params=params)
        if code == 200:  # OK
            # If successful, clear the cache
            self.reset()
        return code, msg

    @property
    def files(self):
        """Fetch Gist's files and store them in the 'files' property."""
        try:
            return self._files
        except AttributeError:
            self._files = _files = {}

        for fn in self._meta['files']:
            # Grab file contents
            _file_url = GIST_BASE % 'raw/%s/%s' % (self.id, fn)
            _files[fn] = unicode(urllib2.urlopen(_file_url).read())

        return _files


class Gists(object):
    """Gist API wrapper"""

    def __init__(self, username=None, token=None):
        # Token-based Authentication is unnecessary, gist api still in alpha
        self._username = username
        self._token = token

    @staticmethod
    def fetch_by_user(name):
        """Return a list of public Gist objects owned by
        the given GitHub username."""

        _url = GIST_JSON % 'gists/%s' % name

        # Return a list of Gist objects
        return [Gist(json=g)
                for g in json.load(urllib2.urlopen(_url))['gists']]

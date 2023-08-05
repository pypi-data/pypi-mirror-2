# fookebox, http://fookebox.googlecode.com/
#
# Copyright (C) 2007-2010 Stefan Ott. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
import mpd
import base64
import logging
from datetime import datetime
from threading import BoundedSemaphore

from pylons import config

log = logging.getLogger(__name__)

class Album(object):

	def __init__(self, artist, albumName, disc=None):
		if albumName == None:
			self.name = ''
		else:
			self.name = str(albumName)

		if artist == None:
			self.artist = ''
		else:
			self.artist = str(artist)

		self.disc = disc
		self.tracks = []

	def add(self, track):
		self.tracks.append(track)

	def hasCover(self):
		return self.getCover() != None

	def _getRockboxPath(self, compilation=False):
		pattern = re.compile('[\/:<>\?*|]')
		album = pattern.sub('_', self.name)

		if compilation:
			artist = pattern.sub('_', config.get(
				'compliations_name'))
		else:
			artist = pattern.sub('_', self.artist)

		return "%s/%s-%s.jpg" % (config.get('album_cover_path'),
				artist, album)

	def _getRhythmboxPath(self, compilation=False):
		album = self.name.replace('/', '-')

		if compilation:
			artist = config.get('compliations_name').replace(
					'/', '-')
		else:
			artist = self.artist.replace('/', '-')

		return "%s/%s - %s.jpg" % (config.get('album_cover_path'),
				artist, album)

	def getCover(self):
		path = self._getRockboxPath()
		if os.path.exists(path):
			return path

		path = self._getRockboxPath(True)
		if os.path.exists(path):
			return path

		path = self._getRhythmboxPath()
		if os.path.exists(path):
			return path

		path = self._getRhythmboxPath(True)
		if os.path.exists(path):
			return path

		return None

	def getCoverURI(self):
		return "%s/%s" % (base64.urlsafe_b64encode(self.artist),
				base64.urlsafe_b64encode(self.name))

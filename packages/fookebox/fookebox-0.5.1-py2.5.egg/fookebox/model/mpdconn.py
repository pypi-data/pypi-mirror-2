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

class Lock(object):

	class __impl:

		def __init__(self):
			self.semaphore = BoundedSemaphore(value=1)

		def acquire(self):
			return self.semaphore.acquire(False)

		def release(self):
			return self.semaphore.release()

	__instance = None

	def __init__(self):
		if Lock.__instance is None:
			Lock.__instance = Lock.__impl()

		self.__dict__['_Lock__instance'] = Lock.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

class Genre(object):

	def __init__(self, name):
		self.name = name
		self.base64 = base64.urlsafe_b64encode(name)

class Artist(object):

	def __init__(self, name):
		self.name = name
		self.base64 = base64.urlsafe_b64encode(name)

class Track(object):
	NO_ARTIST = 'Unknown artist'
	NO_TITLE = 'Unnamed track'

	artist = NO_ARTIST
	title = NO_TITLE
	album = None
	track = 0
	file = ''
	b64 = ''
	disc = 0
	queuePosition = 0

	def load(self, song):
		if 'artist' in song:
			self.artist = song['artist']
		if 'title' in song:
			self.title = song['title']
		if 'file' in song:
			self.file = song['file']
			self.b64 = base64.urlsafe_b64encode(self.file)
		if 'track' in song:
			# possible formats:
			#  - '12'
			#  - '12/21'
			#  - ['12', '21']
			t = song['track']
			if '/' in t:
				tnum = t.split('/')[0]
				self.track = int(tnum)
			elif isinstance(t, list):
				self.track = int(t[0])
			else:
				self.track = int(t)
		if 'disc' in song:
			self.disc = song['disc']
		if 'album' in song:
			self.album = str(song['album'])
		if 'pos' in song:
			self.queuePosition = int(song['pos'])

class MPDWorker(object):

	def __init__(self, num):
		self.num = num
		host = config.get('mpd_host')
		port = config.get('mpd_port')
		password = config.get('mpd_pass')

		self.mpd = mpd.MPDClient()
		self.mpd.connect(host, port)

		if password:
			self.mpd.password(password)

		self.atime = datetime.now()
		self.free = True

	def __del__(self):
		self.mpd.close()
		self.mpd.disconnect()

	def __str__(self):
		return "MPDWorker %d (last used: %s)" % (self.num, self.atime)

	def grab(self):
		self.free = False
		self.atime = datetime.now()

	def release(self):
		self.atime = datetime.now()
		self.free = True
		log.debug("Worker %s released" % self)

	def __getattr__(self, attr):
		self.atime = datetime.now()
		return getattr(self.mpd, attr)

class MPDPool(object):

	lock = None

	def __init__(self):
		self.lock = BoundedSemaphore(value=1)
		self._workers = []

	def getWorker(self):
		self.lock.acquire()

		log.debug("Pool contains %d workers" % len(self._workers))
		for worker in self._workers:
			if worker.free:
				log.debug("Re-using worker %s" % worker)
				worker.grab()
				self._cleanup()
				self.lock.release()
				return worker

		try:
			worker = MPDWorker(len(self._workers))
			log.debug("Created new worker %s" % worker)
			worker.grab()
			self._workers.append(worker)
			self.lock.release()
			return worker

		except Exception:
			worker.release()
			self.lock.release()
			log.fatal('Could not connect to MPD')
			raise

	def _cleanup(self):
		now = datetime.now()

		for worker in self._workers:
			if worker.free:
				if (now - worker.atime).seconds > 10:
					log.debug("Removing idle worker %s" %
							worker)
					self._workers.remove(worker)

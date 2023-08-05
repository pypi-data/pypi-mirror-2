from __future__ import with_statement
import os
import random
import logging
import datetime
import tempfile
import threading

from mirte.core import Module
from sarah.event import Event
from sarah.dictlike import DictLike

class Denied(Exception):
	pass
class Stopped(Exception):
	pass
class EmptyQueueException(Exception):
	pass

class Media(DictLike):
	def __init__(self, coll, data):
		super(Media, self).__init__(data)
		self.self.coll = coll
	def unlink(self):
		self.coll.unlink_media(self)
	def save(self):
		self.coll.save_media(self)
	@property
	def mediaFile(self):
		return self.coll.mediaStore.by_key(self.mediaFileKey)
	def __eq__(self, other):
		return self.key == other.key
	def __ne__(self, other):
		return self.key != other.key


class MediaFile(object):
	def __init__(self, store, key):
		self._key = key
		self.store = store
	def get_named_file(self):
		raise NotImplementedError
	def open(self):
		raise NotImplementedError
	def remove(self):
		self.store.remove(self)
	def __eq__(self, other):
		return self._key == other.key
	def __ne__(self, other):
		return self._key != other.key
	def get_info(self):
		stream = self.open()
		ret = self.store.mediaInfo.get_info(stream)
		if hasattr(stream, 'close'):
			stream.close()
		return ret
	@property
	def key(self):
		return self._key
class BaseRequest(DictLike):
	pass
class PastRequest(BaseRequest):
	def __init__(self, history, data):
		super(PastRequest, self).__init__(data)
		self.self.history = history
	def remove(self):
		raise NotImplementedError
class Request(BaseRequest):
	def __init__(self, queue, data):
		super(Request, self).__init__(data)
		self.self.queue = queue
	def move(self, amount):
		self.queue.move(self, amount)
	def cancel(self):
		self.queue.cancel(self)
class User(DictLike):
	def has_access(self):
		raise NotImplementedError
	def __eq__(self, other):
		return self.key == other.key
	def __ne__(self, other):
		return self.key != other.key

class Desk(Module):
	def __init__(self, settings, logger):
		super(Desk, self).__init__(settings, logger)
		self.on_playing_changed = Event()
		self.on_media_changed = Event()
		self.orchestrator.on_playing_changed.register(
				self._on_playing_changed)
		self.collection.on_changed.register(
				self._on_collection_changed)
	def _on_playing_changed(self, previous_playing):
		self.on_playing_changed(previous_playing)
	def _on_collection_changed(self):
		self.on_media_changed()
	def list_media(self):
		return self.collection.media
	def request_media(self, media, user):
		self.users.assert_request(user, media)
		self.queue.request(media, user)
	def add_media(self, stream, user, customInfo=None):
		mediaFile = self.mediaStore.create(stream)
		try:
			self.users.assert_addition(user, mediaFile)
		except Denied:
			mediaFile.remove()
			raise
		self.collection.add(mediaFile, user, customInfo)
	def list_requests(self):
		return self.queue.requests
	def cancel_request(self, request, user):
		self.users.assert_cancel(user, request)
		request.cancel()
	def move_request(self, request, amount):
		self.users.assert_move(user, request, amount)
		request.move(amount)
	def get_playing(self):
		return self.orchestrator.get_playing()
	def user_by_key(self, key):
		return self.users.by_key(key)
	def media_by_key(self, key):
		return self.collection.by_key(key)

class History(Module):
	def __init__(self, settings, logger):
		super(History, self).__init__(settings, logger)
		# when a record is added runtime
		self.on_record = Event()
		# when the whole history is changed (db change, et al)
		self.on_pretty_changed = Event()
	def record(self, media, request, at):
		raise NotImplementedError
	def list_past_requests(self):
		raise NotImplementedError

class Users(Module):
	def assert_request(self, user, media):
		raise NotImplementedError
	def assert_addition(self, user, mediaFile):
		raise NotImplementedError
	def assert_cancel(self, user, request):
		raise NotImplementedError
	def assert_move(self, user, request, amount):
		raise NotImplementedError
	def assert_access(self, user):
		return NotImplementedError
	def by_key(self, key):
		return NotImplementedError

class RandomQueue(Module):
	def __init__(self, settings, logger):
		super(RandomQueue, self).__init__(settings, logger)
		self.list = list()
		self.register_on_setting_changed('length', self.osc_length)
		self.osc_length()
		self.random.on_ready.register(self._random_on_ready)
	def _random_on_ready(self):
		self._fill()
	@property
	def requests(self):
		return reversed(self.list)
	def shift(self):
		if len(self.list) == 0:
			raise EmptyQueueException
		ret = self.list.pop()
		self._grow()
		return ret
	def _grow(self):
		if self.random.ready:
			self.list.insert(0, Request(self, {
				'media': self.random.pick()}))
	def request(self, media, user):
		assert False # shouldn't do that
	def cancel(self, request):
		self.list.remove(request)
		self.list._grow()
	def move(self, request, amount):
		assert False # shouldn't do that
	def osc_length(self):
		self._fill()
	def _fill(self):
		if not self.random.ready:
			return
		if len(self.list) < self.length:
			for i in xrange(self.length - len(self.list)):
				self._grow()
		else:
			self.list = self.list[:self.length]

class AmalgamatedQueue(Module):
	def __init__(self, settings, logger):
		super(AmalgamatedQueue, self).__init__(settings, logger)
	def request(self, media, user):
		self.first.request(media, user)
	@property
	def requests(self):
		return (tuple(self.first.requests) +
			tuple(self.second.requests))
	def shift(self):
		assert False # shouldn't do that
	def cancel(self, request):
		if request in self.first.requests:
			self.first.cancel(request)
		else:
			self.second.cancel(request)
	def move(self, request, amount):
		if request in self.first.requests:
			self.first.move(request, amount)
		else:
			self.second.move(request, amount)

class Queue(Module):
	def __init__(self, settings, logger):
		super(Queue, self).__init__(settings, logger)
		self.list = list()
		self.lock = threading.Lock()
	def request(self, media, user):
		with self.lock:
			self.list.insert(0, Request(self, media, user))
	@property
	def requests(self):
		with self.lock:
			return reversed(self.list)
	def shift(self):
		with self.lock:
			if not self.list:
				raise EmptyQueueException
			return self.list.pop()
	def cancel(self, request):
		with self.lock:
			self.list.remove(request)
	def move(self, request, amount):
		aa = abs(amount)
		with self.lock:
			o = self.list if amount == aa else reversed(self.list) 
			idx = o.index(request)
			n = (self.list[:idx] + 
			     self.list[idx+1:idx+aa+1] +
			     [self.list[idx]] +
			     self.list[idx+aa+1:])
			self.list = n if amount == aa else reversed(n)

class Orchestrator(Module):
	def __init__(self, settings, logger):
		super(Orchestrator, self).__init__(settings, logger)
		self.on_playing_changed = Event()
		self.lock = threading.Lock()
		self.playing_media = None
		self.satisfied_request = None
		self.player.endTime = None
	def get_playing(self):
		with self.lock:
			return (self.playing_media,
				self.satisfied_request,
				self.player.endTime)
	def stop(self):
		with self.lock:
			self.running = False

	def run(self):
		self.running = True
		while self.running:
			self.lock.acquire()
			previous_playing = (self.playing_media,
					    self.satisfied_request,
					    self.player.endTime)
			try:
				if not self.running: break
				req = None
				try:
					req = self.queue.shift()
					media = req.media
					assert not media is None
				except EmptyQueueException:
					try:
						media = self.randomQueue.shift(
								).media
					except EmptyQueueException:
						self.lock.release()
						self.wait_for_media()
						self.lock.acquire()
						continue
				self.playing_media = media
				self.satisfied_request = req
			finally:
				self.lock.release()
			startTime = datetime.datetime.now()
			self.on_playing_changed(previous_playing)
			try:
				self.player.play(media)
			except Stopped:
				# TODO let the orchestrator wait on a new player
				self.l.warn("Player raised Stopped.  Quitting")
				break
			self.history.record(self.playing_media,
					    self.satisfied_request,
					    startTime)
	
	def wait_for_media(self):
		self.l.info("Randomqueue couldn't return media -- collection "+
			    "is assumed to be empty -- waiting for media.")
		self.randomQueue.random.collection.got_media_event.wait()
		self.l.info("Woke!")

class Random(Module):
	def __init__(self, settings, logger):
		super(Random, self).__init__(settings, logger)
		self.cond = threading.Condition()
		self.running = True
		# used to push new PastRequest s to the worker thread
		# None is used in the case of "history.on_pretty_changed"
		self.recordStack = list()
		self.on_ready = Event()
		self.history.on_pretty_changed.register(
				self._on_history_pretty_changed)
		self.history.on_record.register(
				self._on_history_record)

	def _on_history_pretty_changed(self):
		with self.cond:
			self.recordStack = [None]
			self.cond.notify()
	def _on_history_record(self, pr):
		with self.cond:
			self.recordStack.append(pr)
			self.cond.notify()

	def pick(self):
		raise NotImplementedError

	def run(self):
		while True:
			with self.cond:
				self.cond.wait()
			if not self.running:
				break
			if len(self.recordStack) == 0:
				continue
			for pr in reversed(self.recordStack):
				if pr is None:
					self._handle_history_pretty_changed()
				else:
					self._handle_history_record(pr)

	def stop(self):
		self.running = False
		with self.cond:
			self.cond.notify()
	
	def _handle_history_record(self, pr):
		raise NotImplementedError
	def _handle_history_pretty_changed(self):
		raise NotImplementedError

class SimpleRandom(Random):
	def __init__(self, settings, logger):
		super(SimpleRandom, self).__init__(settings, logger)
		self.collection.on_keys_changed.register(
				self.on_collection_keys_changed)
		self.on_collection_keys_changed()
	
	def on_collection_keys_changed(self):
		self.keys = self.collection.media_keys
		if len(self.keys) > 0:
			self.on_ready()

	def pick(self):
		if len(self.keys) == 0:
			return None
		key = self.keys[random.randint(0, len(self.keys) - 1)]
		return self.collection.by_key(key)

	def _handle_history_record(self, pr):
		pass
	def _handle_history_pretty_changed(self):
		pass
	@property
	def ready(self):
		return len(self.keys) > 0

class MediaInfo(Module):
	def get_info(self, stream):
		pass
	def get_info_by_path(self, path):
		with open(path) as f:
			return self.get_info(f)

class MediaStore(Module):
	def create(self, stream):
		raise NotImplementedError
	def by_key(self, key):
		raise NotImplementedError
	@property
	def keys(self):
		raise NotImplementedError

class Player(Module):
	def __init__(self, settings, logger):
		super(Player, self).__init__(settings, logger)
		self.endTime = None
	def stop(self):
		raise NotImplementedError
	def play(self, media):
		raise NotImplementedError

class Collection(Module):
	def __init__(self, settings, logger):
		super(Collection, self).__init__(settings, logger)
		self.on_keys_changed = Event()
		self.on_changed = Event()
		# got_media_event is set when the Collection isn't
		# empty.
		self.got_media_event = threading.Event()
	def add(self, mediaFile, user, extraInfo=None):
		raise NotImplementedError
	@property
	def media(self):
		raise NotImplementedError
	@property
	def media_keys(self):
		raise NotImplementedError
	def by_key(self, key):
		raise NotImplementedError
	def save_media(self, media):
		raise NotImplementedError
	def unlink_media(self, media):
		raise NotImplementedError


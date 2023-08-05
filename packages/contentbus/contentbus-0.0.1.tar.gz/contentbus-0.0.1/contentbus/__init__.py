#
# This file is part Contentbus

# Contentbus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Contentbus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Contentbus.  If not, see <http://www.gnu.org/licenses/>.

'''Content-based Bus'''

from collections import namedtuple
from threading import Lock

from .version import *
from .exceptions import *
from .match import *

class InvalidCallback(Exception):
    pass


# the Message object just holds sender and object
Message = namedtuple('Message', ('sender', 'object'))

class NotifyCallback(object):
    '''Holds a cliaent callback function for an ObjectMatcher.

    The object can be called with a Message and runs the callback if
    the the ObjectMatcher matches the object in the message.
    '''

    def __init__(self, matcher, callback, client):
        assert isinstance(matcher, ObjectMatcher), "not an ObjectMatcher"

        if not callable(callback):
            raise InvalidCallback("Callback is not a callable")

        self.matcher = matcher
        self.callback = callback
        self.client = client

    def __call__(self, message):
        if self.matcher.matches(message.object):
            self.callback(message)

    def __eq__(self, other):
        return (self.matcher, self.callback, self.client) == (other.matcher, other.callback, other.client)


class Bus(object):
    '''Content-based Bus'''

    __callbacks = {} # maps type -> [NotifyCallback...]
    __clients = set() # the registered client names

    __callbacks_lock = Lock()
    __clients_lock = Lock()

    @staticmethod
    def _add_client(client):
        with Bus.__clients_lock:
            if client in Bus.__clients:
                raise AlreadyRegistered("Client already subscribed")
            Bus.__clients.add(client)

    @staticmethod
    def _remove_client(client):
        with Bus.__clients_lock:
            if client in Bus.__clients:
                Bus.__clients.remove(client)

    @staticmethod
    def _add_callback(callback):
        assert isinstance(callback, NotifyCallback), "not a NotifyCallback"

        obj_type = callback.matcher.object_type

        with Bus.__callbacks_lock:
            if obj_type not in Bus.__callbacks:
                Bus.__callbacks[obj_type] = set()
            Bus.__callbacks[obj_type].add(callback)

    @staticmethod
    def _remove_callback(callback):
        assert isinstance(callback, NotifyCallback), "not a NotifyCallback"

        obj_type = callback.matcher.object_type

        with Bus.__callbacks_lock:
            try:
                Bus.__callbacks[obj_type].remove(callback)
            except (KeyError, ValueError):
                raise NotRegistered("NotifyCallback not registered")

            # remove empty lists for object types
            if not Bus.__callbacks[obj_type]:
                del Bus.__callbacks[obj_type]

    def __init__(self, client=""):
        '''Get a bus access point.

        If client name is provided, must be unique;
        it not provided, a unique one is provided by the Bus.
        '''

        self.__client = client or "Client-%d" % hash(self)
        self.callbacks = set() # keep reference to client callbacks

        Bus._add_client(self.client)

    @property
    def client(self):
        return self.__client

    def __del__(self):
        for c in self.callbacks:
            Bus._remove_callback(c)
        Bus._remove_client(self.client)

    def subscribe(self, callback, object_type, match_fun=None, **match_params):
        '''Subscribe a callback to get a notification for an object type.

        If match_fun is provided, it will be called with the object
        instance as parameter and must return a boolean value to
        indicate the match.

        If no function is provided, match parameters can be provided
        as keyworkd args.

        Returns a NotifyCallback.
        '''

        assert isinstance(object_type, type), "not a type"

        matcher = ObjectMatcher(object_type, match_fun, **match_params)
        notify_callback = NotifyCallback(matcher, callback, self)

        self.callbacks.add(notify_callback)
        Bus._add_callback(notify_callback)

        return notify_callback

    def unsubscribe(self, notify_callback):
        '''Unsubscribe a callback'''

        try:
            self.callbacks.remove(notify_callback)
        except ValueError:
            raise NotRegistered("NotifyCallback not registered")

        Bus._remove_callback(notify_callback)

    def send(self, obj):
        '''Send an object on the Bus'''

        message = Message(self.client, obj)

        with Bus.__callbacks_lock:
            for callback in Bus.__callbacks.get(type(obj), []):
                callback(message)


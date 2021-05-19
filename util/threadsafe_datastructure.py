import pickle
from queue import Queue
from threading import Lock
import os


class threadsafe_set:

    def __init__(self, dump_file=None):
        self.lock = Lock()
        self.scrips = set()
        self.location = dump_file
        if dump_file:
            self.__load()

    def __load(self):
        with self.lock:
            with open(self.location, 'rb') as file_load:
                try:
                    self.scrips = pickle.load(file_load)
                except EOFError:
                    self.scrips = set()

    def insert(self, scrip):
        with self.lock:
            if scrip not in self.scrips:
                self.scrips.add(scrip)
                if self.location:
                    with open(self.location, 'wb') as file_dump:
                        pickle.dump(self.scrips, file_dump)

    def remove(self, scrip):
        with self.lock:
            if scrip in self.scrips:
                self.scrips.discard(scrip)
                if self.location:
                    with open(self.location, 'wb') as file_dump:
                        pickle.dump(self.scrips, file_dump)

    def exist(self, scrip):
        with self.lock:
            return scrip in self.scrips

    def items(self):
        self.lock.acquire()
        try:
            for item in self.scrips:
                yield item
        finally:
            self.lock.release()

    def to_list(self):
        with self.lock:
            return list(self.scrips)

    def clear(self):
        with self.lock:
            self.scrips.clear()

    def empty(self):
        with self.lock:
            return not bool(self.scrips)


class ImprovedQueue(Queue):

    def to_list(self):
        """
        Returns a copy of all items in the queue without removing them.
        """

        with self.mutex:
            return list(self.queue)


class AtomicFloat():
    def __init__(self, location: str, value=None):
        if not os.path.exists(location):
            if not value:
                raise Exception("Atomic Float: Init value not passed")
            with open(location, 'w') as fh:
                fh.write(str(value))
        with open(location, 'r') as fh:
            self._value = float(fh.readline())
        self.location = location
        self._lock = Lock()

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v
            with open(self.location, 'w') as fh:
                fh.write(str(v))
            return self._value

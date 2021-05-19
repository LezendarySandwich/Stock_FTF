import pickle
from threading import Lock


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

    def clear(self):
        with self.lock:
            self.scrips.clear()

    def empty(self):
        with self.lock:
            return not bool(self.scrips)

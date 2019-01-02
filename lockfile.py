from json import dumps, loads
from os.path import exists, getsize, isdir


class LockFileError(Exception):
    pass


class LockFile:

    def __init__(self, filename, initialize=True):
        self.filename = filename
        if initialize is True:
            with open(self.filename, 'w') as f:
                    f.write(dumps({"lock": False, "id": 0}))

    def __read__(self):
        with open(self.filename, 'r') as f:
            return loads(f.read())

    def __write__(self, status, id):
        with open(self.filename, 'w') as f:
            f.write(dumps({"lock": status, "id": id}))

    def __lock__(self, id):
        self.__write__(True, id)

    def __unlock__(self, id):
        self.__write__(False, id)

    @property
    def is_locked(self):
        return self.__read__().get('lock')

    @property
    def id(self):
        return self.__read__().get('id')

    def unlock(self, id):
        if self.id == id:
            self.__unlock__(id)
        else:
            raise ValueError("Invalid lock id.")

    def lock(self, id):
        if not self.is_locked:
            self.__lock__(id)
        else:
            raise LockFileError('Resource already locked')

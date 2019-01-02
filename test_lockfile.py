import os
import pytest

from lockfile import LockFile, LockFileError


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        LockFile('/path/to/inexistent/file')

def test_diretory_as_filename():
    with pytest.raises(IsADirectoryError):
        LockFile('/')

def test_lock_resource():
    lock = LockFile('/tmp/test_lockfile.lock')
    lock.lock(2)
    assert lock.is_locked

def test_lock_locked_resource():
    lock = LockFile('/tmp/test_lockfile.lock')
    lock.lock(2)

    with pytest.raises(LockFileError):
        lock.lock(2)

def test_unlock_resource():
    lock = LockFile('/tmp/test_lockfile.lock')
    lock.lock(2)
    lock.unlock(2)
    assert not lock.is_locked

def test_unlock_with_wrong_resource():
    lock = LockFile('/tmp/test_lockfile.lock')
    lock.lock(2)

    with pytest.raises(ValueError):
        lock.unlock(1)

def test_lock_already_initialized_resource():
    with open('/tmp/test_lockfile.lock', 'w') as f:
        f.write('{"lock": false, "id": 0}')

    lock = LockFile('/tmp/test_lockfile.lock', False)
    lock.lock(2)
    assert lock.is_locked

def test_lock_already_initialized_and_locked_resource():
    with open('/tmp/test_lockfile.lock', 'w') as f:
        f.write('{"lock": true, "id": 0}')

    lock = LockFile('/tmp/test_lockfile.lock', False)

    with pytest.raises(LockFileError):
        lock.lock(2)

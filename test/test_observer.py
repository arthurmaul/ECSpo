import unittest
from unittest import TestCase

from ecspo import Observer, Storage

class TestObserver:
    def setUp(self):
        self.storage = Storage()
        self.storage.spawn()
        self.observer = Observer(self.storage)
    def test_select(self):
        ...
    def test_where(self):
        ...
    def test_unless(self):
        ...
    def test_accept(self):
        ...
    def test_reject(self):
        ...
    def test_check(self):
        ...
    def test_build(self):
        ...
    def test_scan(self):
        ...

if __name__ == "__main__":
    unittest.main()

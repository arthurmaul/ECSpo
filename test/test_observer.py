import unittest
from unittest import TestCase

from ecspo import Observer, Storage


class TestObserver(TestCase):
    def setUp(self):
        self.storage = Storage()
        self.e1 = self.storage.handle()
        self.e2 = self.storage.handle()
        self.c1 = self.storage.pool()
        self.c2 = self.storage.pool()
        self.c3 = self.storage.tag()
        self.c4 = self.storage.tag()
        self.e1.set(self.c1, "c1e1")
        self.e2.set(self.c1, "c1e2")
        self.e1.set(self.c2, "c2e1")
        self.e2.set(self.c2, "c2e2")

    def test_select(self):
        observer = Observer(self.storage).where(self.c1, self.c2).build()
        observer.search()
        actual = list(observer.select(self.c1, self.c2))
        self.assertIn(("c1e1", "c2e1"), actual)
        self.assertIn(("c1e2", "c2e2"), actual)
        self.e1.unset(self.c1)
        self.e2.unset(self.c1)
        actual = list(observer.select(self.c1, self.c2))
        self.assertNotIn(("c1e1", "c2e1"), actual)
        self.assertNotIn(("c1e2", "c2e2"), actual)

    def test_where(self):
        observer = (Observer(self.storage)
            .where(self.c1)
            .build())
        observer.search()
        self.assertIn(self.e1.eid, observer)
        self.assertIn(self.e2.eid, observer)
        self.e1.unset(self.c1)
        self.e2.unset(self.c1)
        self.assertNotIn(self.e1.eid, observer)
        self.assertNotIn(self.e2.eid, observer)
    
    def test_unless(self):
        observer = (Observer(self.storage)
            .where(self.c2)
            .unless(self.c1)
            .build())
        observer.search()
        self.assertNotIn(self.e1.eid, observer)
        self.assertNotIn(self.e2.eid, observer)
        self.e1.unset(self.c1)
        self.e2.unset(self.c1)
        self.assertIn(self.e1.eid, observer)
        self.assertIn(self.e2.eid, observer)


if __name__ == "__main__":
    unittest.main()

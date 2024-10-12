import unittest
from unittest import TestCase

from ecspo import Table, EntityDataNotFound


class TestTable(TestCase):
    def setUp(self):
        self.table = Table()

    def test_spawn(self):
        entity = self.table.spawn()
        self.assertIsNotNone(self.table.emap.get(entity))

    def test_despawn(self):
        entity = self.table.spawn()
        self.table.despawn(entity)
        self.assertIsNone(self.table.emap.get(entity))
     
    def test_pool(self):
        pool = self.table.pool()
        self.assertIsNotNone(self.table.cmap.get(pool))
       
    def test_release(self):
        pool = self.table.pool()
        self.table.release(pool)
        self.assertIsNone(self.table.cmap.get(pool))

    def test_set(self):
        pool = self.table.pool()
        entity = self.table.spawn()
        self.table.set(entity, pool, True)
        self.assertTrue(self.table.get(entity, pool))

    def test_unset(self):
        pool = self.table.pool()
        entity = self.table.spawn()
        self.table.set(entity, pool, True)
        self.table.unset(entity, pool)

        with self.assertRaises(EntityDataNotFound):
            self.table.get(entity, pool)

    def test_tag(self):
        tag = self.table.spawn()
        entity = self.table.spawn()
        self.table.tag(entity, tag)
        self.assertIn(tag, self.table.emap[entity])

    def test_untag(self):
        tag = self.table.spawn()
        entity = self.table.spawn()
        self.table.tag(entity, tag)
        self.table.untag(entity, tag)
        self.assertNotIn(tag, self.table.emap[entity])

    def test_copy(self):
        entity1 = self.table.spawn()
        entity2 = self.table.spawn()
        pool1 = self.table.pool()
        pool2 = self.table.pool()
        self.table.set(entity1, pool1, True)
        self.table.set(entity1, pool2, True)
        self.table.copy(entity1, entity2)
        self.assertTrue(self.table.get(entity2, pool1))
        self.assertTrue(self.table.get(entity2, pool2))

    def test_clone(self):
        entity1 = self.table.spawn()
        pool1 = self.table.pool()
        pool2 = self.table.pool()
        self.table.set(entity1, pool1, True)
        self.table.set(entity1, pool2, True)
        entity2 = self.table.clone(entity1)
        self.assertTrue(self.table.get(entity2, pool1))
        self.assertTrue(self.table.get(entity2, pool2))


if __name__ == "__main__":
    unittest.main()

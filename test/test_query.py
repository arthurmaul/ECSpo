import unittest
from unittest import TestCase

from ecspo import Table, Query


class TestQuery(TestCase):
    def setUp(self):
        self.table = Table()
        self.e1 = self.table.spawn()
        self.e2 = self.table.spawn()
        self.c1 = self.table.pool()
        self.c2 = self.table.pool()
        self.table.set(self.e1, self.c1, "c1e1")
        self.table.set(self.e2, self.c1, "c1e2")
        self.table.set(self.e1, self.c2, "c2e1")
        self.table.set(self.e2, self.c2, "c2e2")

    def test_select(self):
        q = (Query(self.table)
            .where(self.c1, self.c2)
            .build())
        actual = list(q.select(self.c1, self.c2))

        with self.subTest("Ensure selection returns valid entities."):
            self.assertIn(("c1e1", "c2e1"), actual)
            self.assertIn(("c1e2", "c2e2"), actual)

        self.table.unset(self.e1, self.c1)
        self.table.unset(self.e2, self.c1)
        q.build()
        actual = list(q.select(self.c1, self.c2))

        with self.subTest("Ensure selection doesnt return invalid entities."):
            self.assertNotIn(("c1e1", "c2e1"), actual)
            self.assertNotIn(("c1e2", "c2e2"), actual)

    def test_where(self):
        q = (Query(self.table)
            .where(self.c1)
            .build())

        with self.subTest("Ensure where collects matching entities."):
            self.assertIn(self.e1, q)
            self.assertIn(self.e2, q)

        self.table.unset(self.e1, self.c1)
        self.table.unset(self.e2, self.c1)
        q.build()

        with self.subTest("Ensure where leaves out non-matching entities."):
            self.assertNotIn(self.e1, q)
            self.assertNotIn(self.e2, q)
    
    def test_unless(self):
        q = (Query(self.table)
            .where(self.c2)
            .unless(self.c1)
            .build())

        with self.subTest("Ensure unless filters invalid entities."):
            self.assertNotIn(self.e1, q)
            self.assertNotIn(self.e2, q)

        self.table.unset(self.e1, self.c1)
        self.table.unset(self.e2, self.c1)
        q.build()

        with self.subTest("Ensure unless query allows valid entities."):
            self.assertIn(self.e1, q)
            self.assertIn(self.e2, q)


if __name__ == "__main__":
    unittest.main()

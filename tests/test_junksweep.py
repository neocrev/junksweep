import os
import sys
import shutil
import tempfile
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from junksweep import scan, sizeof_fmt


class TestJunksweep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # create junk directories
        os.makedirs(os.path.join(self.tmp, "proj1", "node_modules"))
        os.makedirs(os.path.join(self.tmp, "proj1", "src"))
        os.makedirs(os.path.join(self.tmp, "proj2", "__pycache__"))
        os.makedirs(os.path.join(self.tmp, "proj2", ".git"))

        # put some files in junk dirs to give them size
        for d in ["proj1/node_modules", "proj2/__pycache__", "proj2/.git"]:
            f = os.path.join(self.tmp, d, "dummy.bin")
            with open(f, "wb") as fp:
                fp.write(b"x" * 1024 * 1024 * 2)  # 2MB each

        # create a legit dir that should not be matched
        os.makedirs(os.path.join(self.tmp, "proj1", "src", "components"))
        with open(os.path.join(self.tmp, "proj1", "src", "app.py"), "w") as fp:
            fp.write("print('hello')")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_scan_finds_junk(self):
        results = scan(self.tmp, depth=5, min_size_mb=1)
        names = [r["name"] for r in results]
        self.assertIn("node_modules", names)
        self.assertIn("__pycache__", names)
        self.assertIn(".git", names)
        self.assertEqual(len(results), 3)

    def test_scan_min_size_filters(self):
        results = scan(self.tmp, depth=5, min_size_mb=10)
        self.assertEqual(len(results), 0)

    def test_scan_empty_project(self):
        empty = tempfile.mkdtemp()
        results = scan(empty, depth=3, min_size_mb=0)
        self.assertEqual(len(results), 0)
        shutil.rmtree(empty)

    def test_sizeof_fmt(self):
        self.assertIn("B", sizeof_fmt(0))
        self.assertIn("K", sizeof_fmt(1024))
        self.assertIn("M", sizeof_fmt(1024 * 1024))
        self.assertIn("G", sizeof_fmt(1024 ** 3))


if __name__ == "__main__":
    unittest.main()

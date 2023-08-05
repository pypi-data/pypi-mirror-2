import unittest
import testsuite
import sys
import tempfile
import os
import shlex
import subprocess
import time

from tokyo.tyrant import RTDB as _RTDB, Error
from tokyo.cabinet import TDB, TDBOREADER, INT_MAX, INT_MIN


FILENAME = "tmp_tt_test.{0}"
HOST = "127.0.0.1"
PORT = 1980
TEMPDIR = tempfile.gettempdir()
PIDFILE = os.path.join(TEMPDIR, FILENAME.format("pid"))
DBFILE = os.path.join(TEMPDIR, FILENAME.format("tct"))
START_CMD = "ttserver -host {0} -port {1} -dmn -pid {2} {3}".format(HOST, PORT, PIDFILE, DBFILE)
STOP_CMD = "kill -TERM `cat {0}`".format(PIDFILE)


class RTDB(_RTDB):

    def keys(self):
        return (key for key in self)

    def values(self):
        return (self[key] for key in self)

    def items(self):
        return ((key, self[key]) for key in self)


class RTDBTestSuite(testsuite.TestSuite):

    def setUp(self):
        time.sleep(0.1)
        subprocess.check_call(shlex.split(START_CMD))
        time.sleep(0.1)

    def tearDown(self):
        time.sleep(0.1)
        subprocess.check_call(STOP_CMD, shell=True)
        time.sleep(0.1)
        os.remove(DBFILE)


class RTDBTest(unittest.TestCase):

    def setUp(self):
        self.db = RTDB()
        self.db.open(HOST, PORT)

    def tearDown(self):
        self.db.clear()
        self.db.close()
        self.db = None


class RTDBTestDict(RTDBTest):

    def test_contains(self):
        self.assertRaises(TypeError, self.db.__contains__)
        self.assertRaises(TypeError, self.db.__contains__, 1)
        self.assertTrue(not (b"a" in self.db))
        self.assertTrue(b"a" not in self.db)
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.assertTrue(b"a" in self.db)
        self.assertTrue(b"b" in self.db)
        self.assertTrue(b"c" not in self.db)

    def test_len(self):
        self.assertEqual(len(self.db), 0)
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.assertEqual(len(self.db), 2)

    def test_getitem(self):
        self.assertRaises(TypeError, self.db.__getitem__)
        self.assertRaises(TypeError, self.db.__getitem__, 1)
        self.assertRaises(KeyError, self.db.__getitem__, b"a")
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.assertEqual(self.db[b"a"], {b"test": b"a"})
        self.assertEqual(self.db[b"b"], {b"test": b"b"})
        self.db[b"c"] = {b"test": b"c"}
        self.db[b"a"] = {b"test": b"d"}
        self.assertEqual(self.db[b"c"], {b"test": b"c"})
        self.assertEqual(self.db[b"a"], {b"test": b"d"})

    def test_setitem(self):
        self.assertRaises(TypeError, self.db.__setitem__)
        self.assertRaises(TypeError, self.db.__setitem__, b"a")
        self.assertRaises(TypeError, self.db.__setitem__, b"a", 1)
        self.assertRaises(TypeError, self.db.__setitem__, 1, b"a")
        self.assertRaises(Error, self.db.__setitem__, b"a", {b"": b"a"})
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.assertEqual(len(self.db), 2)
        d = dict(self.db.items())
        self.assertEqual(d, {b"a": {b"test": b"a"}, b"b": {b"test": b"b"}})
        self.db[b"c"] = {b"test": b"c"}
        self.db[b"a"] = {b"test": b"aa"}
        d = dict(self.db.items())
        self.assertEqual(d, {b"a": {b"test": b"aa"}, b"b": {b"test": b"b"}, b"c": {b"test": b"c"}})
        del self.db[b"b"]
        self.assertEqual(len(self.db), 2)
        d = dict(self.db.items())
        self.assertEqual(d, {b"a": {b"test": b"aa"}, b"c": {b"test": b"c"}})

    def test_clear(self):
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.assertEqual(len(self.db), 2)
        self.db.clear()
        self.assertEqual(len(self.db), 0)
        d = dict(self.db.items())
        self.assertEqual(d, {})


class RTDBTestIter(RTDBTest):

    def test_iter(self):
        i = iter(self.db)
        self.assertEqual(len(i), 0)
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        self.db[b"c"] = {b"test": b"c"}
        i = iter(self.db)
        self.assertEqual(len(i), len(self.db))
        self.assertTrue(b"a" in i)
        self.assertEqual([b"a", b"b", b"c"], sorted(i))
        i = iter(self.db)
        a = next(i)
        b = next(i)
        c = next(i)
        self.assertRaises(StopIteration, next, i)
        self.assertEqual([b"a", b"b", b"c"], sorted((a, b, c)))
        i = iter(self.db)
        self.assertEqual(len(i), 3)
        a = next(i)
        del self.db[b"b"]
        self.db[b"d"] = {b"test": b"d"}
        self.assertEqual(len(i), 3)
        self.assertRaises(Error, next, i)


class RTDBTestPut(RTDBTest):

    def test_put(self):
        self.db.put(b"a", {b"test": b"a"})
        self.db.put(b"b", {b"test": b"b"})
        self.assertEqual(self.db[b"a"], {b"test": b"a"})
        self.assertEqual(self.db[b"b"], {b"test": b"b"})
        self.db.put(b"c", {b"test": b"c"})
        self.db.put(b"a", {b"test": b"aa"})
        self.assertEqual(self.db[b"c"], {b"test": b"c"})
        self.assertEqual(self.db[b"a"], {b"test": b"aa"})

    def test_putkeep(self):
        self.db.putkeep(b"a", {b"test": b"a"})
        self.assertRaises(KeyError, self.db.putkeep, b"a", {b"test": b"a"})

    def test_putcat(self):
        self.db.putcat(b"a", {b"test": b"a"})
        self.db.putcat(b"a", {b"test": b"b", b"test2": b"c"})
        self.assertEqual(self.db[b"a"], {b"test": b"a", b"test2": b"c"})


class RTDBTestMisc(RTDBTest):

    def test_status(self):
        self.assertEqual(len(self.db.status), 48)

    def test_size(self):
        self.assertEqual(os.stat(DBFILE).st_size, self.db.size)

    def test_copy(self):
        self.db[b"a"] = {b"test": b"a"}
        self.db[b"b"] = {b"test": b"b"}
        path = os.path.join(tempfile.gettempdir(), "tmp_tt_test2.tct")
        self.db.copy(path)
        db = TDB()
        db.open(path, TDBOREADER)
        self.assertEqual(len(self.db), len(db))
        self.assertEqual(self.db.size, db.size)
        db.close()
        os.remove(path)

    def test_searchkeys(self):
        self.db[b"key1"] = {b"test": b"1"}
        self.db[b"key2"] = {b"test": b"2"}
        self.db[b"key3"] = {b"test": b"3"}
        self.db[b"akey"] = {b"test": b"a"}
        self.assertEqual(self.db.searchkeys(b"k"), frozenset((b"key1", b"key2", b"key3")))
        self.assertEqual(self.db.searchkeys(b"k", 2), frozenset((b"key1", b"key2")))
        self.assertEqual(self.db.searchkeys(b"z"), frozenset())
        self.assertEqual(self.db.searchkeys(b"a"), frozenset((b"akey",)))


all_tests = (
             "RTDBTestDict",
             "RTDBTestIter",
             "RTDBTestPut",
             "RTDBTestMisc",
            )

suite = RTDBTestSuite(unittest.TestLoader().loadTestsFromNames(all_tests,
                                                               sys.modules[__name__]))

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)

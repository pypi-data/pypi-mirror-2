import unittest
import testsuite
import sys
import tempfile
import os
import shlex
import subprocess
import time

from tokyo.tyrant import RDB, Error
from tokyo.cabinet import HDB, HDBOREADER, INT_MAX, INT_MIN


FILENAME = "tmp_tt_test.{0}"
HOST = "127.0.0.1"
PORT = 1979
TEMPDIR = tempfile.gettempdir()
PIDFILE = os.path.join(TEMPDIR, FILENAME.format("pid"))
DBFILE = os.path.join(TEMPDIR, FILENAME.format("tch"))
START_CMD = "ttserver -host {0} -port {1} -dmn -pid {2} {3}".format(HOST, PORT, PIDFILE, DBFILE)
STOP_CMD = "kill -TERM `cat {0}`".format(PIDFILE)


class RDBTestSuite(testsuite.TestSuite):

    def setUp(self):
        time.sleep(0.1)
        subprocess.check_call(shlex.split(START_CMD))
        time.sleep(0.1)

    def tearDown(self):
        time.sleep(0.1)
        subprocess.check_call(STOP_CMD, shell=True)
        time.sleep(0.1)
        os.remove(DBFILE)


class RDBTest(unittest.TestCase):

    def setUp(self):
        self.db = RDB()
        self.db.open(HOST, PORT)

    def tearDown(self):
        self.db.clear()
        self.db.close()
        self.db = None


class RDBTestDict(RDBTest):

    def test_contains(self):
        self.assertRaises(TypeError, self.db.__contains__)
        self.assertRaises(TypeError, self.db.__contains__, 1)
        self.assertTrue(not (b"a" in self.db))
        self.assertTrue(b"a" not in self.db)
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.assertTrue(b"a" in self.db)
        self.assertTrue(b"b" in self.db)
        self.assertTrue(b"c" not in self.db)

    def test_len(self):
        self.assertEqual(len(self.db), 0)
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.assertEqual(len(self.db), 2)

    def test_getitem(self):
        self.assertRaises(TypeError, self.db.__getitem__)
        self.assertRaises(TypeError, self.db.__getitem__, 1)
        self.assertRaises(KeyError, self.db.__getitem__, b"a")
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.assertEqual(self.db[b"a"], b"1")
        self.assertEqual(self.db[b"b"], b"2")
        self.db[b"c"] = b"3"
        self.db[b"a"] = b"4"
        self.assertEqual(self.db[b"c"], b"3")
        self.assertEqual(self.db[b"a"], b"4")

    def test_setitem(self):
        self.assertRaises(TypeError, self.db.__setitem__)
        self.assertRaises(TypeError, self.db.__setitem__, b"a")
        self.assertRaises(TypeError, self.db.__setitem__, b"a", 1)
        self.assertRaises(TypeError, self.db.__setitem__, 1, b"a")
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.assertEqual(len(self.db), 2)
        d = dict(self.db.iteritems())
        self.assertEqual(d, {b"a": b"1", b"b": b"2"})
        self.db[b"c"] = b"3"
        self.db[b"a"] = b"4"
        d = dict(self.db.iteritems())
        self.assertEqual(d, {b"a": b"4", b"b": b"2", b"c": b"3"})
        del self.db[b"b"]
        self.assertEqual(len(self.db), 2)
        d = dict(self.db.iteritems())
        self.assertEqual(d, {b"a": b"4", b"c": b"3"})

    def test_clear(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.assertEqual(len(self.db), 2)
        self.db.clear()
        self.assertEqual(len(self.db), 0)
        d = dict(self.db.iteritems())
        self.assertEqual(d, {})


class RDBTestIter(RDBTest):

    def test_iter(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.db[b"c"] = b"3"
        i = iter(self.db)
        self.assertTrue(b"a" in i)
        i = iter(self.db)
        self.assertEqual([b"a", b"b", b"c"], sorted(i))
        i = iter(self.db)
        a = next(i)
        b = next(i)
        c = next(i)
        self.assertRaises(StopIteration, next, i)
        self.assertEqual([b"a", b"b", b"c"], sorted((a, b, c)))
        i = iter(self.db)
        a = next(i)
        del self.db[b"b"]
        self.assertRaises(Error, next, i)
        i = iter(self.db)
        a = next(i)
        self.db[b"d"] = b"4"
        self.assertRaises(Error, next, i)
        i = iter(self.db)
        a = next(i)
        del self.db[b"d"]
        self.db[b"d"] = b"5"
        self.assertRaises(Error, next, i)

    def test_iterkeys(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.db[b"c"] = b"3"
        self.assertEqual([b"a", b"b", b"c"],
                         sorted(list(self.db.iterkeys())))

    def test_itervalues(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.db[b"c"] = b"3"
        self.assertEqual([b"1", b"2", b"3"],
                         sorted(list(self.db.itervalues())))

    def test_iteritems(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        self.db[b"c"] = b"3"
        self.assertEqual({b"a": b"1", b"b": b"2", b"c": b"3"},
                         dict(self.db.iteritems()))


class RDBTestPut(RDBTest):

    def test_put(self):
        self.db.put(b"a", b"1")
        self.db.put(b"b", b"2")
        self.assertEqual(self.db[b"a"], b"1")
        self.assertEqual(self.db[b"b"], b"2")
        self.db.put(b"c", b"3")
        self.db.put(b"a", b"4")
        self.assertEqual(self.db[b"c"], b"3")
        self.assertEqual(self.db[b"a"], b"4")

    def test_putkeep(self):
        self.db.putkeep(b"a", b"1")
        self.assertRaises(KeyError, self.db.putkeep, b"a", b"1")

    def test_putcat(self):
        self.db.putcat(b"a", b"1")
        self.db.putcat(b"a", b"2")
        self.assertEqual(self.db[b"a"], b"12")


class RDBTestMisc(RDBTest):

    def test_status(self):
        self.assertEqual(len(self.db.status), 48)

    def test_size(self):
        self.assertEqual(os.stat(DBFILE).st_size, self.db.size)

    def test_copy(self):
        self.db[b"a"] = b"1"
        self.db[b"b"] = b"2"
        path = os.path.join(tempfile.gettempdir(), "tmp_tt_test2.tch")
        self.db.copy(path)
        db = HDB()
        db.open(path, HDBOREADER)
        self.assertEqual(len(self.db), len(db))
        self.assertEqual(self.db.size, db.size)
        db.close()
        os.remove(path)

    def test_searchkeys(self):
        self.db[b"key1"] = b"1"
        self.db[b"key2"] = b"2"
        self.db[b"key3"] = b"3"
        self.db[b"akey"] = b"4"
        self.assertEqual(self.db.searchkeys(b"k"), frozenset((b"key1", b"key2", b"key3")))
        self.assertEqual(self.db.searchkeys(b"k", 2), frozenset((b"key1", b"key2")))
        self.assertEqual(self.db.searchkeys(b"z"), frozenset())
        self.assertEqual(self.db.searchkeys(b"a"), frozenset((b"akey",)))

    def test_addint(self):
        self.assertEqual(self.db.addint(b"kint", 0), 0)
        self.assertEqual(self.db.addint(b"kint", 1), 1)
        self.db[b"kint"] = b"aa"
        self.assertRaises(KeyError, self.db.addint, b"kint", 1)

    def test_addint_max(self):
        self.assertEqual(self.db.addint(b"kint", INT_MAX), INT_MAX)
        self.assertEqual(self.db.addint(b"kint", 1), INT_MIN)
        self.assertEqual(self.db.addint(b"kint", 1), INT_MIN + 1)

    def test_adddouble(self):
        self.assertEqual(self.db.adddouble(b"kfloat", 1.0), 1.0)
        self.assertEqual(self.db.adddouble(b"kfloat", -1.5), -0.5)
        self.db[b"kfloat"] = b"aa"
        self.assertRaises(KeyError, self.db.adddouble, b"kfloat", 1.0)


class RDBTestNullBytes(RDBTest):

    def test_iterkeys(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual([b"a\0b", b"cd"], sorted(list(self.db.iterkeys())))

    def test_itervalues(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual([b"ab", b"c\0d"], sorted(list(self.db.itervalues())))

    def test_iteritems(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual({b"a\0b": b"ab", b"cd": b"c\0d"},
                         dict(self.db.iteritems()))

    def test_contains(self):
        self.db[b"a\0b"] = b"ab"
        self.assertTrue(self.db.__contains__(b"a\0b"))
        self.assertTrue(b"a\0b" in self.db)

    def test_getitem(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual(b"ab", self.db.__getitem__(b"a\0b"))
        self.assertEqual(b"ab", self.db[b"a\0b"])
        self.assertEqual(b"c\0d", self.db.__getitem__(b"cd"))
        self.assertEqual(b"c\0d", self.db[b"cd"])

    def test_setitem(self):
        self.db.__setitem__(b"a\0b", b"ab")
        self.db.__setitem__(b"cd", b"c\0d")
        self.assertEqual(b"ab", self.db[b"a\0b"])
        self.assertEqual(b"c\0d", self.db[b"cd"])

    def test_get(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual(b"ab", self.db.get(b"a\0b"))
        self.assertEqual(b"c\0d", self.db.get(b"cd"))

    def test_remove(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual(len(self.db), 2)
        self.db.remove(b"a\0b")
        self.assertEqual(len(self.db), 1)

    def test_put(self):
        self.db.put(b"a\0b", b"ab")
        self.db.put(b"cd", b"c\0d")
        self.assertEqual(b"ab", self.db[b"a\0b"])
        self.assertEqual(b"c\0d", self.db[b"cd"])

    def test_putkeep(self):
        self.db.putkeep(b"a\0b", b"ab")
        self.db.putkeep(b"cd", b"c\0d")
        self.assertRaises(KeyError, self.db.putkeep, b"a\0b", b"g\0h")

    def test_putcat(self):
        self.db.putcat(b"a\0b", b"ab")
        self.db.putcat(b"a\0b", b"c\0d")
        self.assertEqual(self.db[b"a\0b"], b"abc\0d")

    def test_putnb(self):
        self.db.putnb(b"a\0b", b"ab")
        self.db.putnb(b"cd", b"c\0d")
        self.db.sync()
        self.assertEqual(b"ab", self.db[b"a\0b"])
        self.assertEqual(b"c\0d", self.db[b"cd"])

    def test_searchkeys(self):
        self.db[b"a\0b"] = b"ab"
        self.db[b"cd"] = b"c\0d"
        self.assertEqual(self.db.searchkeys(b"a"), frozenset((b"a\0b",)))
        self.assertEqual(self.db.searchkeys(b"a\0"), frozenset((b"a\0b",)))

    def test_addint(self):
        self.assertEqual(self.db.addint(b"a\0b", 1), 1)

    def test_adddouble(self):
        self.assertEqual(self.db.adddouble(b"a\0b", 1.0), 1.0)


all_tests = (
             "RDBTestDict",
             "RDBTestIter",
             "RDBTestPut",
             "RDBTestMisc",
             "RDBTestNullBytes",
            )

suite = RDBTestSuite(unittest.TestLoader().loadTestsFromNames(all_tests,
                                                              sys.modules[__name__]))

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)

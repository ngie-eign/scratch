#!/usr/bin/env python
"""
A complex-ish mox test example.

.. moduleauthor: Enji Cooper
.. date: April 2014
"""

import sqlite3
import unittest

import mox

from nose.tools import (
    assert_raises,
)

tmp_database = None


def setup():
    """Initialize an sqlite3 object in memory with a dummy table"""

    global tmp_database

    tmp_database = sqlite3.connect(':memory:')
    table_create_sql = \
        'CREATE TABLE ' \
        'perple_table(name STRING, age INTEGER, PRIMARY KEY(name ASC));'
    tmp_database.execute(table_create_sql)


def teardown():
    """Not strictly required, but close the db object when the test is done"""

    try:
        cursor = tmp_database.cursor()
        cursor.execute('SELECT * FROM perple_table')
        print(cursor.fetchall())
    finally:
        tmp_database.close()


class BadInsert(Exception):
    """Exception raised on failed PerpleDb.insert's"""


class RegistrationFailed(Exception):
    """Exception raised on failed PerpleManager.registers's"""


class PerpleManager(object):

    def __init__(self, db):
        self._db = db

    def register(self, perple):
        try:
            self._db.insert(perple)
        except BadInsert:
            raise RegistrationFailed


class PerpleDb(object):
    """Ermah-person class!"""

    def __init__(self, db):
        self._cursor = db.cursor()

    def insert(self, perple):
        try:
            data = (perple.name, perple.age, )
            insert_sql = 'INSERT INTO perple_table(name,age) VALUES (?,?);'

            self._cursor.execute(insert_sql, data)
            if self._cursor.rowcount == 0:
                raise Exception('The insert failed')
        except:
            raise BadInsert


class Perple(object):

    age = None
    name = None

    def __init__(self, name, age):
        self.age = age
        self.name = name


class TestPerpleManager(object):

    def setUp(self):
        self.mox = mox.Mox()
        self.dao = self.mox.CreateMock(PerpleDb)
        self.manager = PerpleManager(self.dao)
        self.perple = Perple('Kate', 42)

    def test_register_successful_insert(self):
        self.dao.insert(self.perple)
        self.mox.ReplayAll()
        self.manager.register(self.perple)
        self.mox.VerifyAll()

    def test_failed_insert(self):
        self.dao.insert(self.perple).AndRaise(BadInsert("I don't like Kate!"))
        self.mox.ReplayAll()
        assert_raises(RegistrationFailed, self.manager.register, self.perple)
        self.mox.VerifyAll()

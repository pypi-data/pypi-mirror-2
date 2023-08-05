# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import time

from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from trac.db import Table, Column, Index
from datetime import datetime
from trac.util.datefmt import utc, to_timestamp


class TestManagerModelProvider(Component):
    implements(IEnvironmentSetupParticipant)

    SCHEMA = [
        Table('testconfig', key = ('propname'))[
              Column('propname'),
              Column('value'),
              Index(['propname']),],
        Table('testcases', key = ('id'))[
              Column('id'),
              Column('status'),
              Index(['id']),],
        Table('testcasehistory', key = ('id', 'time'))[
              Column('id'),
              Column('time', type='int'),
              Column('author'),
              Column('status'),
              Index(['id', 'time']),]
        ]

    # IEnvironmentSetupParticipant methods
    def environment_created(self):
        self._create_db(self.env.get_db_cnx())

    def environment_needs_upgrade(self, db):
        if self._need_initialization(db):
            return True

        return False

    def upgrade_environment(self, db):
        # Create db
        if self._need_initialization(db):
            self._upgrade_db(db)

    def _need_initialization(self, db):
        cursor = db.cursor()
        try:
            cursor.execute("select count(*) from testconfig")
            cursor.fetchone()
            cursor.execute("select count(*) from testcases")
            cursor.fetchone()
            cursor.execute("select count(*) from testcasehistory")
            cursor.fetchone()
            return False
        except:
            db.rollback()
            print("testmanager needs to create the db")
            return True
        
    def _create_db(self, db):
        self._upgrade_db(db)
        
    def _upgrade_db(self, db):
        try:
            try:
                from trac.db import DatabaseManager
                db_backend, _ = DatabaseManager(self.env)._get_connector()
            except ImportError:
                db_backend = self.env.get_db_cnx()

            cursor = db.cursor()
            for table in self.SCHEMA:
                for stmt in db_backend.to_sql(table):
                    self.env.log.debug(stmt)
                    cursor.execute(stmt)
                    
            db.commit()

            # Create default values for configuration properties and initialize counters
            cursor.execute("INSERT INTO testconfig (propname, value) VALUES ('NEXT_CATALOG_ID', '0')")
            cursor.execute("INSERT INTO testconfig (propname, value) VALUES ('NEXT_TESTCASE_ID', '0')")
            db.commit()

            # Create the basic "TC" Wiki page, used as the root test catalog
            cursor = db.cursor()
            cursor.execute("INSERT INTO wiki (name,version,time,author,ipnr,"
                           "text,comment,readonly) VALUES (%s,%s,%s,%s,%s,%s,"
                           "%s,%s)", ('TC', 1,
                                      to_timestamp(datetime.now(utc)), 'System', '127.0.0.1',
                                      ' ', '', 0))
                    
            db.commit()

        except:
            db.rollback()
            print("exception during upgrade")
            raise

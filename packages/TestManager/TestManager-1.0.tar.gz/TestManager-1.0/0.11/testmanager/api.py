# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import re
import time
import sys
import traceback

from datetime import datetime
from trac.core import *
from trac.perm import IPermissionRequestor, PermissionError
from trac.util import get_reporter_id
from trac.util.datefmt import utc, to_timestamp
from trac.web.api import IRequestHandler

from testmanager.util import formatExceptionInfo


# Public methods

def get_status_description(status):    
    if status == 'SUCCESSFUL':
        return "Successful"
    
    if status == 'TO_BE_TESTED':
        return "Untested"
    
    if status == 'FAILED':
        return "Failed"
    
    return "Unknown"
    

class TestManagerSystem(Component):
    """Test Manager system for Trac."""

    implements(IPermissionRequestor, IRequestHandler)

    # Public methods
    def get_next_id(self, type):
        propname = ''
    
        if type == 'catalog':
            propname = 'NEXT_CATALOG_ID'
        else:
            propname = 'NEXT_TESTCASE_ID'
        
        try:
            # Get next ID
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            sql = "SELECT value FROM testconfig WHERE propname='"+propname+"'"
            
            cursor.execute(sql)
            row = cursor.fetchone()
            
            id = int(row[0])

            # Increment next ID
            cursor = db.cursor()
            cursor.execute("UPDATE testconfig SET value='" + str(id+1) + "' WHERE propname='"+propname+"'")
            
            db.commit()
        except:
            db.rollback()
            raise

        return id
    
    def set_next_id(self, type, value):
        propname = ''
    
        if type == 'catalog':
            propname = 'NEXT_CATALOG_ID'
        else:
            propname = 'NEXT_TESTCASE_ID'
        
        try:
            # Set next ID to the input value
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            cursor.execute("UPDATE testconfig SET value='" + str(value) + "' WHERE propname='"+propname+"'")
           
            db.commit()
        except:
            db.rollback()
            raise
    
    def add_testcase(self, id, author="System", status='TO_BE_TESTED'):
        """Add a test case."""
        
        try:
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            sql = "INSERT INTO testcases (id, status) VALUES ('"+str(id)+"', '"+status+"')"
            cursor.execute(sql)

            cursor = db.cursor()
            sql = 'INSERT INTO testcasehistory (id, time, author, status) VALUES (%s, '+str(to_timestamp(datetime.now(utc)))+', %s, %s)'
            cursor.execute(sql, (str(id), author, status))

            db.commit()
        except:
            db.rollback()
            raise

    def delete_testcase(self, id):
        """Delete a test case."""

        try:
            db = self.env.get_db_cnx()
            cursor = db.cursor()

            sql = "DELETE FROM testcases WHERE id='"+str(id)+"'"
            
            cursor.execute(sql)
            db.commit()

            cursor = db.cursor()

            sql = "DELETE FROM testcasehistory WHERE id='"+str(id)+"'"
            
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            raise

    def get_testcase_status(self, id):
        """Returns a test case status."""

        db = self.env.get_db_cnx()
        cursor = db.cursor()

        sql = "SELECT status FROM testcases WHERE id='"+str(id)+"'"
        
        cursor.execute(sql)
        row = cursor.fetchone()
        
        status = 'TO_BE_TESTED'
        if row:
            status = row[0]
        
        return status

    def set_testcase_status(self, id, status, author="Unknown"):
        """Set a test case status."""

        try:
            db = self.env.get_db_cnx()

            cursor = db.cursor()
            sql = 'UPDATE testcases SET status=%s WHERE id=%s'
            cursor.execute(sql, (status, str(id)))

            cursor = db.cursor()
            sql = 'INSERT INTO testcasehistory (id, time, author, status) VALUES (%s, '+str(to_timestamp(datetime.now(utc)))+', %s, %s)'
            cursor.execute(sql, (str(id), author, status))
            
            db.commit()

        except:
            print self._formatExceptionInfo()
            db.rollback()
            
            raise

    def report_testcase_status(self):
        """Returns a test case status."""

        db = self.env.get_db_cnx()
        cursor = db.cursor()

        sql = "SELECT id, status FROM testcases"
        
        cursor.execute(sql)

        print "-- BEGIN"
        
        for id, status in cursor:
            print "Test Case: "+id+", status="+status

        print "-- END"

    def get_testcase_status_history_markup(self, id):
        """Returns a test case status audit trail."""

        result = '<table class="listing"><thead>'
        result += "<tr><th>Timestamp</th><th>Author</th><th>Stato</th></tr>"
        result += '</thead><tbody>'
        
        db = self.env.get_db_cnx()
        cursor = db.cursor()

        sql = "SELECT time, author, status FROM testcasehistory WHERE id='"+str(id)+"' ORDER BY id, time"
        
        cursor.execute(sql)
        for ts, author, status  in cursor:
            result += '<tr>'
            result += '<td>'+str(datetime.fromtimestamp(ts, utc))+'</td>'
            result += '<td>'+author+'</td>'
            result += '<td>'+get_status_description(status)+'</td>'
            result += '</tr>'

        result += '</tbody></table>'
         
        return result

            
    # IPermissionRequestor methods
    def get_permission_actions(self):
        return ['TEST_VIEW', 'TEST_MODIFY', 'TEST_EXECUTE', 'TEST_DELETE']

        
    # IRequestHandler methods

    def match_request(self, req):
        return req.path_info.startswith('/teststatusupdate')

    def process_request(self, req):
        """Handles Ajax requests to set the test case status."""

        # Print the status of all test cases
        #self.report_testcase_status()
    
        id = req.args.get('id')
        status = req.args.get('status')
        author = get_reporter_id(req, 'author')

        self.set_testcase_status(id, status, author)
        
        return 'empty.html', {}, None

        
    # Internal methods
        
    def _formatExceptionInfo(maxTBlevel=5):
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        
        try:
            excArgs = exc.__dict__["args"]
        except KeyError:
            excArgs = "<no args>"
        
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)


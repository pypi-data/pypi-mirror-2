# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import re
import sys
import time
import traceback

from datetime import datetime
from trac.core import *
from trac.perm import IPermissionRequestor, PermissionError
from trac.resource import IResourceManager
from trac.util import get_reporter_id
from trac.util.datefmt import utc
from trac.util.translation import _, N_, gettext
from trac.web.api import IRequestHandler

from testmanager.util import *
from testmanager.labels import *
from testmanager.model import TestCatalog, TestCase, TestCaseInPlan, TestPlan, TestManagerModelProvider


class ITestObjectChangeListener(Interface):
    """Extension point interface for components that require notification
    when test objects, e.g. test cases, catalogs, plans etc, are created, 
    modified, or deleted."""

    def object_created(testobject):
        """Called when a test object is created."""

    def object_changed(testobject, comment, author, old_values):
        """Called when a test object is modified.
        
        `old_values` is a dictionary containing the previous values of the
        fields that have changed.
        """

    def object_deleted(testobject):
        """Called when a test object is deleted."""


class TestManagerSystem(Component):
    """Test Manager system for Trac."""

    implements(IPermissionRequestor, IRequestHandler, IResourceManager)

    change_listeners = ExtensionPoint(ITestObjectChangeListener)

    def get_next_id(self, type):
        propname = _get_next_prop_name(type)
    
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
            self.env.log.debug(self._formatExceptionInfo())
            db.rollback()
            raise

        return str(id)
    
    def set_next_id(self, type, value):
        propname = _get_next_prop_name(type)
        
        try:
            # Set next ID to the input value
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            cursor.execute("UPDATE testconfig SET value='" + str(value) + "' WHERE propname='"+propname+"'")
           
            db.commit()
        except:
            self.env.log.debug(self._formatExceptionInfo())
            db.rollback()
            raise
    
    def get_testcase_status_history_markup(self, id, planid):
        """Returns a test case status in a plan audit trail."""

        result = '<table class="listing"><thead>'
        result += '<tr><th>'+LABELS['timestamp']+'</th><th>'+LABELS['author']+'</th><th>'+LABELS['status']+'</th></tr>'
        result += '</thead><tbody>'
        
        db = self.env.get_db_cnx()
        cursor = db.cursor()

        sql = "SELECT time, author, status FROM testcasehistory WHERE id='"+str(id)+"' AND planid='"+str(planid)+"' ORDER BY time DESC"
        
        cursor.execute(sql)
        for ts, author, status in cursor:
            result += '<tr>'
            result += '<td>'+str(from_any_timestamp(ts))+'</td>'
            result += '<td>'+author+'</td>'
            result += '<td>'+LABELS[status]+'</td>'
            result += '</tr>'

        result += '</tbody></table>'
         
        return result
        
        
    # Change listeners management

    def object_created(self, testobject):
        for c in self.change_listeners:
            c.object_created(testobject)

    def object_changed(self, testobject, comment, author):
        for c in self.change_listeners:
            c.object_changed(testobject, comment, author, testobject._old)

    def object_deleted(self, testobject):
        for c in self.change_listeners:
            c.object_deleted(testobject)


    # @deprecated
    def list_all_testplans(self):
        """Returns a list of all test plans."""

        db = self.env.get_db_cnx()
        cursor = db.cursor()

        sql = "SELECT id, catid, page_name, name, author, time FROM testplan ORDER BY catid, id"
        
        cursor.execute(sql)
        for id, catid, page_name, name, author, ts  in cursor:
            yield id, catid, page_name, name, author, str(from_any_timestamp(ts))


    # IPermissionRequestor methods
    def get_permission_actions(self):
        return ['TEST_VIEW', 'TEST_MODIFY', 'TEST_EXECUTE', 'TEST_DELETE', 'TEST_PLAN_ADMIN']

        
    # IRequestHandler methods

    def match_request(self, req):
        type = req.args.get('type', '')
        
        match = False
        
        if req.path_info.startswith('/testcreate') and (((type == 'catalog' or type == 'testcase') and ('TEST_MODIFY' in req.perm)) or 
             (type == 'testplan' and ('TEST_PLAN_ADMIN' in req.perm))):
            match = True
        elif (req.path_info.startswith('/teststatusupdate') and 'TEST_EXECUTE' in req.perm):
            match = True
        elif (req.path_info.startswith('/testpropertyupdate') and 'TEST_MODIFY' in req.perm):
            match = True
        
        return match

    def process_request(self, req):
        """
        Handles Ajax requests to set the test case status.
        """
        author = get_reporter_id(req, 'author')

        if req.path_info.startswith('/teststatusupdate'):
            req.perm.require('TEST_EXECUTE')
        
            id = req.args.get('id')
            planid = req.args.get('planid')
            path = req.args.get('path')
            status = req.args.get('status')

            try:
                self.env.log.debug("Setting status %s to test case %s in plan %s" % (status, id, planid))
                tcip = TestCaseInPlan(self.env, id, planid)
                if tcip.exists:
                    tcip.set_status(status, author)
                    tcip.save_changes(author, "Status changed")

                    self.object_changed(tcip, "Status changed", author)
                    
                else:
                    tcip['page_name'] = path
                    tcip['status'] = status
                    tcip.insert()
                    
                    self.object_created(tcip)
                
            except:
                self.env.log.debug(self._formatExceptionInfo())
        
        elif req.path_info.startswith('/testpropertyupdate'):
            req.perm.require('TEST_MODIFY')

            realm = req.args.get('realm')
            key_str = req.args.get('key')
            name = req.args.get('name')
            value = req.args.get('value')

            key = get_dictionary_from_string(key_str)

            try:
                self.env.log.debug("Setting property %s to %s, in %s with key %s" % (name, value, realm, key))
                
                tmmodelprovider = TestManagerModelProvider(self.env)
                obj = tmmodelprovider.get_object(realm, key)
                
                obj[name] = value
                obj.author = author
                obj.remote_addr = req.remote_addr
                if obj is not None and obj.exists:
                    obj.save_changes(author, "Custom property changed")
 
                    self.object_changed(obj, "Custom property changed", author)
                    
                else:
                    self.env.log.debug("Object to update not found. Creating it.")
                    props_str = req.args.get('props')
                    if props_str is not None and not props_str == '':
                        props = get_dictionary_from_string(props_str)
                        obj.set_values(props)
                    obj.insert()

                    self.object_created(obj)

            except:
                self.env.log.debug(self._formatExceptionInfo())

        elif req.path_info.startswith('/testcreate'):
            type = req.args.get('type')
            path = req.args.get('path')
            title = req.args.get('title')
            author = get_reporter_id(req, 'author')

            autosave = req.args.get('autosave', 'false')
            duplicate = req.args.get('duplicate')
            paste = req.args.get('paste')
            tcId = req.args.get('tcId')

            id = self.get_next_id(type)

            pagename = path
            
            if type == 'catalog':
                req.perm.require('TEST_MODIFY')
                pagename += '_TT'+str(id)

                try:
                    new_tc = TestCatalog(self.env, id, pagename, title, '')
                    new_tc.author = author
                    new_tc.remote_addr = req.remote_addr
                    # This also creates the Wiki page
                    new_tc.insert()
                    
                    self.object_created(new_tc)
                    
                except:
                    print "Error adding test catalog!"
                    print self._formatExceptionInfo()
                    req.redirect(req.path_info)

                # Redirect to see the new wiki page.
                req.redirect(req.href.wiki(pagename))
                
            elif type == 'testplan':
                req.perm.require('TEST_PLAN_ADMIN')
                
                catid = path.rpartition('_TT')[2]

                try:
                    # Add the new test plan in the database
                    new_tc = TestPlan(self.env, id, catid, pagename, title, author)
                    new_tc.insert()

                    self.object_created(new_tc)

                except:
                    print "Error adding test plan!"
                    print self._formatExceptionInfo()
                    # Back to the catalog
                    req.redirect(req.href.wiki(path))

                # Display the new test plan
                req.redirect(req.href.wiki(path, planid=str(id)))
                    
            elif type == 'testcase':
                req.perm.require('TEST_MODIFY')
                
                pagename += '_TC'+str(id)
                
                if paste and paste != '':
                    # Handle move/paste of the test case into another catalog

                    req.perm.require('TEST_PLAN_ADMIN')

                    try:
                        catid = path.rpartition('_TT')[2]
                        tcat = TestCatalog(self.env, catid)
                        
                        old_pagename = tcId
                        tc_id = tcId.rpartition('_TC')[2]
                        tc = TestCase(self.env, tc_id, tcId)
                        if tc.exists:
                            tc.move_to(tcat)

                            self.object_changed(tc, "Moved to new catalog.", author)
                            
                        else:
                            self.env.log.debug("Test case not found")
                    except:
                        self.env.log.debug("Error pasting test case!")
                        self.env.log.debug(self._formatExceptionInfo())
                        req.redirect(req.path_info)
                
                    # Redirect to test catalog, forcing a page refresh by means of a random request parameter
                    req.redirect(req.href.wiki(pagename.rpartition('_TC')[0], random=str(datetime.now(utc).microsecond)))
                    
                elif duplicate and duplicate != '':
                    # Duplicate test case
                    old_id = tcId.rpartition('_TC')[2]
                    old_pagename = tcId
                    try:
                        old_tc = TestCase(self.env, old_id, old_pagename)
                        
                        # New test case name will be the old catalog name + the newly generated test case ID
                        author = get_reporter_id(req, 'author')
                        
                        # Create new test case wiki page as a copy of the old one, but change its page path
                        new_tc = old_tc
                        new_tc['page_name'] = pagename
                        new_tc.remote_addr = req.remote_addr
                        # And save it under the new id
                        new_tc.save_as({'id': id})

                        self.object_created(new_tc)
                        
                    except:
                        self.env.log.debug("Error duplicating test case!")
                        self.env.log.debug(self._formatExceptionInfo())
                        req.redirect(req.path_info)

                    # Redirect tp allow for editing the copy test case
                    req.redirect(req.href.wiki(pagename, action='edit'))
                    
                else:
                    # Normal creation of a new test case
                    try:
                        new_tc = TestCase(self.env, id, pagename, title, '')
                        new_tc.author = author
                        new_tc.remote_addr = req.remote_addr
                        # This also creates the Wiki page
                        new_tc.insert()

                        self.object_created(new_tc)
                        
                    except:
                        self.env.log.debug("Error adding test case!")
                        self.env.log.debug(self._formatExceptionInfo())
                        req.redirect(req.path_info)

                    # Redirect to edit the test case description
                    req.redirect(req.href.wiki(pagename, action='edit'))
        
        return 'empty.html', {}, None


    # IResourceManager methods
    
    def get_resource_realms(self):
        yield 'testcatalog'
        yield 'testcase'
        yield 'testcaseinplan'
        yield 'testplan'

    def get_resource_url(self, resource, href, **kwargs):
        tmmodelprovider = TestManagerModelProvider(self.env)
        obj = tmmodelprovider.get_object(resource.realm, get_dictionary_from_string(resource.id))
        
        if obj.exists:
            args = {}
            
            if resource.realm == 'testcaseinplan':
                args = {'planid': obj['planid']}
            elif resource.realm == 'testplan':
                args = {'planid': obj['id']}

            args.update(kwargs)
                 
            return href('wiki', obj['page_name'], **args)
        else:
            return href('wiki', 'TC', **kwargs)

    def get_resource_description(self, resource, format='default', context=None,
                                 **kwargs):
        return resource.id

    def resource_exists(self, resource):
        tmmodelprovider = TestManagerModelProvider(self.env)
        obj = tmmodelprovider.get_object(resource.realm, get_dictionary_from_string(resource.id))
        
        return obj.exists

        
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

def _get_next_prop_name(type):
    propname = ''

    if type == 'catalog':
        propname = 'NEXT_CATALOG_ID'
    elif type == 'testcase':
        propname = 'NEXT_TESTCASE_ID'
    elif type == 'testplan':
        propname = 'NEXT_PLAN_ID'

    return propname
        

# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import re
import sys
import traceback

import time
from datetime import datetime

from trac.core import *
from trac.web.chrome import add_stylesheet, add_script, ITemplateProvider #, INavigationContributor
from trac.wiki.api import IWikiSyntaxProvider
from trac.resource import Resource, render_resource_link, get_resource_url
from trac.mimeview.api import Context
from trac.web.api import ITemplateStreamFilter, IRequestHandler
from trac.wiki.api import WikiSystem, IWikiPageManipulator, IWikiChangeListener
from trac.wiki.model import WikiPage
from trac.wiki.formatter import Formatter
from trac.util.compat import sorted
from trac.util.datefmt import utc, to_timestamp
from genshi.builder import tag
from genshi.filters.transform import Transformer
from genshi.core import Markup
from genshi import HTML
from testmanager.api import TestManagerSystem
from testmanager.macros import TestCaseBreadcrumbMacro, TestCaseTreeMacro, TestCaseStatusMacro, TestCaseChangeStatusMacro, TestCaseStatusHistoryMacro


class WikiTestManagerInterface(Component):
    """Implement generic template provider."""
    
    implements(ITemplateProvider)
    
    # ITemplateProvider
    def get_templates_dirs(self):
        """
            Return the absolute path of the directory containing the provided
            templates
        """
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        """
            Return a list of directories with static resources (such as style
            sheets, images, etc.)
    
            Each item in the list must be a '(prefix, abspath)' tuple. The
            'prefix' part defines the path in the URL that requests to these
            resources are prefixed with.
            
            The 'abspath' is the absolute path to the directory containing the
            resources on the local file system.
        """
        from pkg_resources import resource_filename
        return [('testmanager', resource_filename(__name__, 'htdocs'))]


class WikiTestCatalogInterface(Component):
    """Implement the user interface for test catalogs."""
    
    implements(ITemplateStreamFilter, IRequestHandler, IWikiChangeListener)

    # ITemplateStreamFilter methods
    
    def filter_stream(self, req, method, filename, stream, data):
        page_name = req.args.get('page', 'WikiStart')

        formatter = Formatter(
            self.env, Context.from_request(req, Resource('testmanager'))
            )
        
        if page_name.startswith('TC'):
            if page_name.find('_TC') >= 0:
                if filename == 'wiki_view.html':
                    return self._testcase_wiki_view(req, formatter, page_name, stream)
            else:
                if filename == 'wiki_view.html':
                    return self._catalog_wiki_view(req, formatter, page_name, stream)
                
        return stream

    # IRequestHandler methods

    def match_request(self, req):
        return req.path_info.startswith('/testcreate')

    def process_request(self, req):
        type = req.args.get('type')
        path = req.args.get('path')
        title = req.args.get('title')

        paste = req.args.get('paste')
        tcId = req.args.get('tcId')
        
        test_manager_system = TestManagerSystem(self.env)
        id = test_manager_system.get_next_id(type)

        pagename = path
        if type == 'catalog':
            pagename += '_TT'+str(id)
            req.redirect(req.href.wiki(pagename, action='edit', text='== '+title+' =='))
            
        else:
            pagename += '_TC'+str(id)
            
            if paste and paste != '':
                # Handle move/paste of the test case into another catalog
                old_pagename = tcId
                old_id = tcId.rpartition('_TC')[2]
                
                old_page = WikiPage(self.env, old_pagename)
                old_state = test_manager_system.get_testcase_status(old_id)

                try:
                    db = self.env.get_db_cnx()
            
                    cursor = db.cursor()
                    
                    # Create a new test case, copy contents from original one
                    cursor.execute("INSERT INTO wiki (name,version,time,author,ipnr,"
                                   "text,comment,readonly) VALUES (%s,%s,%s,%s,%s,%s,"
                                   "%s,%s)", (pagename, 1,
                                              to_timestamp(datetime.now(utc)), old_page.author, '127.0.0.1',
                                              old_page.text, '', 0))
                    db.commit()
                    
                    # Add the test case status information into custom table
                    test_manager_system.add_testcase(id, old_page.author, old_state)
                    
                    # Delete the original test case
                    old_page.delete()

                    # Redirect to test catalog, forcing a page refresh by means of a random request parameter
                    req.redirect(req.href.wiki(pagename.rpartition('_TC')[0], random=str(datetime.now(utc).microsecond)))
                    
                except:
                    db.rollback()
                    
                    print self._formatExceptionInfo()
            
            else:
                # Normal creation of a new test case
                req.redirect(req.href.wiki(pagename, action='edit', text='== '+title+' =='))
        
        
    # IWikiChangeListener methods
    
    def wiki_page_added(self, page):
        page_on_db = WikiPage(self.env, page.name)
        
        if page.name.find('_TC') >= 0:
            test_manager_system = TestManagerSystem(self.env)
            test_manager_system.add_testcase(page.name.rpartition('_TC')[2], page_on_db.author)

    def wiki_page_changed(self, page, version, t, comment, author, ipnr):
        pass

    def wiki_page_deleted(self, page):
        if page.name.find('_TC') >= 0:
            test_manager_system = TestManagerSystem(self.env)
            test_manager_system.delete_testcase(page.name.rpartition('_TC')[2])

    def wiki_page_version_deleted(self, page):
        pass

        
    # Internal methods

    def _catalog_wiki_view(self, req, formatter, page_name, stream):
        path_name = req.path_info
        cat_name = path_name.rpartition('/')[2]
    
        add_stylesheet(req, 'testmanager/css/testmanager.css')

        add_script(req, 'testmanager/js/cookies.js')
        add_script(req, 'testmanager/js/testmanager.js')

        breadcrumb_macro = TestCaseBreadcrumbMacro(self.env)
        tree_macro = TestCaseTreeMacro(self.env)

        if page_name == 'TC':
            insert1 = tag.div()(
                        tag.div(id='pasteTCHereMessage', class_='messageBox', style='display: none;')("Select the catalog into which to paste the Test Case and click on 'Move the copied Test Case here'. ",
                            tag.a(href='javascript:void(0);', onclick='cancelTCMove()')("Cancel")
                            ),
                        tag.h1("Test Catalogs List"),
                        tag.br(), tag.br()
                        )
            fieldLabel = "New Catalog:"
            buttonLabel = "Add a Catalog"
        else:
            insert1 = tag.div()(
                        HTML(breadcrumb_macro.expand_macro(formatter, None, page_name)),
                        tag.br(), 
                        tag.div(id='pasteTCHereMessage', class_='messageBox', style='display: none;')(
                            "Select the catalog (even this one) into which to paste the Test Case and click on 'Move the copied Test Case here'. ",
                            tag.a(href='javascript:void(0);', onclick='cancelTCMove()')("Cancel")
                            ),
                        tag.br(),
                        tag.h1("Test Catalog")
                        )
            fieldLabel = "New Sub-Catalog:"
            buttonLabel = "Add a Sub-Catalog"

        insert2 = tag.div()(
                    HTML(tree_macro.expand_macro(formatter, None, page_name)),
                    tag.div(class_='testCaseList')(
                    tag.br(), tag.br(),
                    tag.div(class_='field')(
                        tag.script('var baseLocation="'+req.href()+'";', type='text/javascript'),
                        tag.br(), tag.br(), tag.br(), tag.br(),
                        tag.label(
                            fieldLabel,
                            tag.span(id='catErrorMsgSpan', style='color: red;'),
                            tag.br(),
                            tag.input(id='catName', type='text', name='catName', size='50'),
                            tag.input(type='button', value=buttonLabel, onclick='creaTestCatalog("'+cat_name+'")')
                            )
                        )
                    ))
        
        if not page_name == 'TC':
            insert2.append(tag.div(class_='field')(
                        tag.script('var baseLocation="'+req.href()+'";', type='text/javascript'),
                        tag.label(
                            "New Test Case:",
                            tag.span(id='errorMsgSpan', style='color: red;'),
                            tag.br(),
                            tag.input(id='tcName', type='text', name='tcName', size='50'),
                            tag.input(type='button', value="Add a Test Case", onclick='creaTestCase("'+cat_name+'")')
                            ),
                        tag.br(), tag.br(),
                        tag.input(type='button', id='pasteTCHereButton', value="Move the copied Test Case here", onclick='pasteTestCaseIntoCatalog("'+cat_name+'")')
                        ))
                    
        insert2.append(tag.div()(tag.br(), tag.br(), tag.br(), tag.br()))
        
        return stream | Transformer('//div[contains(@class,"wikipage")]').after(insert2) | Transformer('//div[contains(@class,"wikipage")]').before(insert1)


    def _testcase_wiki_view(self, req, formatter, page_name, stream):
        path_name = req.path_info
        tc_name = path_name.rpartition('/')[2]
        cat_name = path_name.rpartition('/')[2].partition('_TC')[0]
    
        add_stylesheet(req, 'testmanager/css/testmanager.css')
        add_stylesheet(req, 'common/css/report.css')

        add_script(req, 'testmanager/js/cookies.js')
        add_script(req, 'testmanager/js/testmanager.js')
        
        breadcrumb_macro = TestCaseBreadcrumbMacro(self.env)
        testcase_status_macro = TestCaseStatusMacro(self.env)
        testcase_change_status_macro = TestCaseChangeStatusMacro(self.env)
        testcase_status_history_macro = TestCaseStatusHistoryMacro(self.env)
        
        insert1 = tag.div()(
                    HTML(breadcrumb_macro.expand_macro(formatter, None, page_name)),
                    tag.br(), 
                    tag.div(id='copiedTCMessage', class_='messageBox', style='display: none;')(
                        "The Test Case has been copied. Now select the catalog into which to move the Test Case and click on 'Move the copied Test Case here'. ",
                        tag.a(href='javascript:void(0);', onclick='cancelTCMove()')("Cancel")
                        ),
                    tag.br(),
                    tag.span(style='font-size: large; font-weight: bold;')(
                        tag.span(style='float: left; padding-top: 4px; padding-right: 5px;')(
                            HTML(testcase_status_macro.expand_macro(formatter, None, page_name))
                            ),
                        tag.span()(                            
                            "Test Case"
                            )
                        )
                    )
        
        insert2 = tag.div(class_='field', style='marging-top: 60px;')(
                    tag.br(), tag.br(), tag.br(), tag.br(),
                    tag.script('var baseLocation="'+req.href()+'";', type='text/javascript'),
                    HTML(testcase_change_status_macro.expand_macro(formatter, None, page_name)),
                    tag.br(), tag.br(),
                    tag.input(type='button', value="Open a Ticket on this Test Case", onclick='creaTicket("'+tc_name+'")'),
                    HTML('&nbsp;&nbsp;'), 
                    tag.input(type='button', id='moveTCButton', value="Move the Test Case into another catalog", onclick='copyTestCaseToClipboard("'+tc_name+'")'),
                    tag.br(), tag.br(), 
                    HTML(testcase_status_history_macro.expand_macro(formatter, None, page_name)),
                    tag.br(), tag.br()
                    )
                    
        return stream | Transformer('//div[contains(@class,"wikipage")]').after(insert2) | Transformer('//div[contains(@class,"wikipage")]').before(insert1)

    def _formatExceptionInfo(maxTBlevel=5):
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        
        try:
            excArgs = exc.__dict__["args"]
        except KeyError:
            excArgs = "<no args>"
        
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)

        
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Roberto Longobardi, Marco Cipriani
#

import re

from genshi.builder import tag

from trac.resource import Resource, get_resource_url
from trac.core import *
from trac.wiki.macros import WikiMacroBase
from trac.wiki.api import WikiSystem
from trac.wiki.model import WikiPage
from testmanager.api import TestManagerSystem
from testmanager.util import get_page_title


# Macros

class TestCaseBreadcrumbMacro(WikiMacroBase):
    """Display a breadcrumb with the path to the current catalog or test case.

    Usage:

    {{{
    [[TestCaseBreadcrumb()]]
    }}}
    """
    
    def expand_macro(self, formatter, name, content):
        if not content:
            content = formatter.resource.id
        
        req = formatter.req

        return _build_testcases_breadcrumb(self.env, req, content)

        

class TestCaseTreeMacro(WikiMacroBase):
    """Display a tree with catalogs and test cases.

    Usage:

    {{{
    [[TestCaseTree()]]
    }}}
    """
    
    def expand_macro(self, formatter, name, content):
        if not content:
            content = formatter.resource.id
        
        req = formatter.req

        return _build_testcases_tree(self.env, req, content)


class TestCaseStatusMacro(WikiMacroBase):
    """Display a colored icon according to the test case status.

    Usage:

    {{{
    [[TestCaseStatus()]]
    }}}
    """
    
    def expand_macro(self, formatter, name, content):
        if not content:
            content = formatter.resource.id
        
        req = formatter.req

        return _build_testcase_status(self.env, req, content)

        
class TestCaseChangeStatusMacro(WikiMacroBase):
    """Display a semaphore to set the test case status.

    Usage:

    {{{
    [[TestCaseChangeStatus()]]
    }}}
    """
    
    def expand_macro(self, formatter, name, content):
        if not content:
            content = formatter.resource.id
        
        req = formatter.req

        return _build_testcase_change_status(self.env, req, content)

        
class TestCaseStatusHistoryMacro(WikiMacroBase):
    """Display the history of status changes of a test case.

    Usage:

    {{{
    [[TestCaseStatusHistory()]]
    }}}
    """
    
    def expand_macro(self, formatter, name, content):
        if not content:
            content = formatter.resource.id
        
        req = formatter.req

        return _build_testcase_status_history(self.env, req, content)

        

# Internal methods

def _build_testcases_breadcrumb(env,req,curpage):
    test_manager_system = TestManagerSystem(env)

    # Determine current catalog name
    cat_name = 'TC'
    if curpage.find('_TC') >= 0:
        cat_name = curpage.rpartition('_TC')[0].rpartition('_')[2]
    elif not curpage == 'TC':
        cat_name = curpage.rpartition('_')[2]
    
    # Create the breadcrumb model
    path_name = curpage.partition('TC_')[2]
    tokens = path_name.split("_")
    curr_path = 'TC'
    
    breadcrumb = [{'name': 'TC', 'title': "All Catalogs", 'id': 'TC'}]

    for i, tc in enumerate(tokens):
        curr_path += '_'+tc
        page = WikiPage(env, curr_path)
        page_title = get_page_title(page.text)
        
        breadcrumb[(i+1):] = [{'name': tc, 'title': page_title, 'id': curr_path}]

        if tc == cat_name:
            break

    text = ''

    text +='<div>'
    text += _render_breadcrumb(breadcrumb)
    text +='</div>'

    return text    
            

def _build_testcases_tree(env,req,curpage):
    test_manager_system = TestManagerSystem(env)

    # Determine current catalog name
    cat_name = 'TC'
    if curpage.find('_TC') >= 0:
        cat_name = curpage.rpartition('_TC')[0].rpartition('_')[2]
    elif not curpage == 'TC':
        cat_name = curpage.rpartition('_')[2]
    # Create the catalog subtree model
    components = {'name': curpage, 'childrenC': {},'childrenT': {}, 'tot': 0}

    for subpage_name in sorted(WikiSystem(env).get_pages(curpage+'_')):
        subpage = WikiPage(env, subpage_name)
        subpage_title = get_page_title(subpage.text)

        path_name = subpage_name.partition(curpage+'_')[2]
        tokens = path_name.split("_")
        parent = components
        ltok = len(tokens)
        count = 1
        curr_path = curpage
        for tc in tokens:
            curr_path += '_'+tc
            
            if tc == '':
                break

            if not tc.startswith('TC'):
                comp = {}
                if (tc not in parent['childrenC']):
                    comp = {'id': curr_path, 'name': tc, 'title': subpage_title, 'childrenC': {},'childrenT': {}, 'tot': 0, 'parent': parent}
                    parent['childrenC'][tc]=comp
                else:
                    comp = parent['childrenC'][tc]
                parent = comp

            else:
                # It is a test case page
                status = test_manager_system.get_testcase_status(tc.partition('TC')[2])
                parent['childrenT'][tc]={'id':curr_path, 'title': subpage_title, 'status': status}
                compLoop = parent
                while (True):
                    compLoop['tot']+=1
                    if ('parent' in compLoop):
                        compLoop = compLoop['parent']
                    else:
                        break
            count+=1

    # Generate the markup
    ind = {'count': 0}
    text = ''

    text +='<div style="padding: 0px 0px 10px 10px">Filter: <input id="tcFilter" title="Type the test to search for, even more than one word. You can also filter on the test case status (untested, successful, failed)." type="text" size="40" onkeyup="starthighlight(this.value)"/>&nbsp;&nbsp;<span id="searchResultsNumberId" style="font-weight: bold;"></span></div>'
    text +='<div style="font-size: 0.8em;padding-left: 10px"><a style="margin-right: 10px" onclick="toggleAll(true)" href="javascript:void(0)">Expand all</a><a onclick="toggleAll(false)" href="javascript:void(0)">Collapse all</a></div>';
    text +='<div id="ticketContainer">'

    text += _render_subtree(components, ind, 0)
    
    text +='</div>'
    return text
  
# Render the breadcrumb
def _render_breadcrumb(breadcrumb):
    text = ''
    path_len = len(breadcrumb)
    for i, x in enumerate(breadcrumb):
        text += '<span name="breadcrumb" style="cursor: pointer; color: #BB0000; margin-left: 10px; margin-right: 10px; font-size: 0.8em;" '
        text += ' onclick="window.location=\''+x['id']+'\'">'+x['title']
        
        if i < path_len-1:
            text += '&nbsp;&nbsp;->'
        
        text += '</span>'
        
    return text
 
# Render the subtree
def _render_subtree(component, ind, level, path=''):
    data = component
    text = ''
    if (level == 0):
        data = component['childrenC']
        text +='<ul style="list-style: none;">';        
    keyList = data.keys()
    sortedList = sorted(keyList)
    for x in sortedList:
        ind["count"]+=1
        text+='<li style="font-weight: normal">'
        comp = data[x]
        fullpath = path+x+" - "
        if ('childrenC' in comp):
            subcData=comp['childrenC']
            
            toggle_icon = '../chrome/testmanager/images/plus.png'
            toggable = 'toggable'
            if (len(comp['childrenC']) + len(comp['childrenT'])) == 0:
                toggable = 'nope'
                toggle_icon = '../chrome/testmanager/images/empty.png'
                
            text+='<span name="'+toggable+'" style="cursor: pointer" id="b_'+str(ind["count"])+'"><span onclick="toggle(\'b_'+str(ind["count"])+'\')"><img class="iconElement" src="'+toggle_icon+'" /></span><span id="l_'+str(ind["count"])+'" onmouseover="underlineLink(\'l_'+str(ind["count"])+'\')" onmouseout="removeUnderlineLink(\'l_'+str(ind["count"])+'\')" onclick="window.location=\''+comp["id"]+'\'" title="Apri">'+comp["title"]+'</span></span><span style="color: gray;">&nbsp;('+str(comp["tot"])+')</span>'
            text +='<ul id="b_'+str(ind["count"])+'_list" style="display:none;list-style: none;">';
            ind["count"]+=1
            text+=_render_subtree(subcData,ind,level+1,fullpath)
            if ('childrenT' in comp):            
                mtData=comp['childrenT']
                text+=_render_testcases(mtData)
        text+='</ul>'
        text+='</li>'
    if (level == 0):
        if ('childrenT' in component):            
            cmtData=component['childrenT']
            text+=_render_testcases(cmtData)
        text+='</ul>'        
    return text


def _render_testcases(data): 
    text=''
    keyList = data.keys()
    sortedList = sorted(keyList)
    for x in sortedList:
        tick = data[x]
        if tick["status"] == 'SUCCESSFUL':
            statusIcon='../chrome/testmanager/images/green.png'
            statusLabel = "Successful"
        elif tick["status"] == 'FAILED':
            statusIcon='../chrome/testmanager/images/red.png'
            statusLabel = "Failed"
        else:
            statusIcon='../chrome/testmanager/images/yellow.png'
            statusLabel = "Untested"
        
        text+="<li style='font-weight: normal;'><img class='iconElement' src='"+statusIcon+"' title='"+statusLabel+"'></img><a href='"+tick['id']+"' target='_blank'>"+tick['title']+"&nbsp;</a><span style='display: none;'>"+statusLabel+"</span></li>"
    return text
    
    
def _build_testcase_status(env,req,curpage):
    test_manager_system = TestManagerSystem(env)

    tc = curpage.rpartition('_TC')[2]
    status = test_manager_system.get_testcase_status(tc)
    
    display = {'SUCCESSFUL': 'none', 'TO_BE_TESTED': 'none', 'FAILED': 'none'}
    display[status] = 'block'
    
    text = ''
    text += '<img style="display: '+display['TO_BE_TESTED']+';" id="tcTitleStatusIconTO_BE_TESTED" src="../chrome/testmanager/images/yellow.png" title="Da Testare"></img></span>'
    text += '<img style="display: '+display['FAILED']+';" id="tcTitleStatusIconFAILED" src="../chrome/testmanager/images/red.png" title="Fallito"></img></span>'
    text += '<img style="display: '+display['SUCCESSFUL']+';" id="tcTitleStatusIconSUCCESSFUL" src="../chrome/testmanager/images/green.png" title="Passato"></img></span>'
        
    return text

    
def _build_testcase_change_status(env,req,curpage):
    test_manager_system = TestManagerSystem(env)

    tc = curpage.rpartition('_TC')[2]
    status = test_manager_system.get_testcase_status(tc)
    
    text = ''
    
    text += '<script type="text/javascript">var currStatus = "'+status+'";</script>'

    text += 'Change the status:'
    
    text += '<span style="margin-left: 15px;">'

    border = ''
    if status == 'SUCCESSFUL':
        border = 'border: 2px solid black;'

    text += '<span id="tcStatusSUCCESSFUL" style="padding: 3px; cursor: pointer;'+border+'" onclick="changestate(\''+tc+'\', \'SUCCESSFUL\')">'
    text += '<img src="../chrome/testmanager/images/green.png" title="Successful"></img></span>'

    border = ''
    if status == 'TO_BE_TESTED':
        border = 'border: 2px solid black;'

    text += '<span id="tcStatusTO_BE_TESTED" style="padding: 3px; cursor: pointer;'+border+'" onclick="changestate(\''+tc+'\', \'TO_BE_TESTED\')">'
    text += '<img src="../chrome/testmanager/images/yellow.png" title="Untested"></img></span>'

    border = ''
    if status == 'FAILED':
        border = 'border: 2px solid black;'

    text += '<span id="tcStatusFAILED" style="padding: 3px; cursor: pointer;'+border+'" onclick="changestate(\''+tc+'\', \'FAILED\')">'
    text += '<img src="../chrome/testmanager/images/red.png" title="Failed"></img></span>'

    text += '</span>'
    
    return text

    
def _build_testcase_status_history(env,req,curpage):
    test_manager_system = TestManagerSystem(env)

    tc = curpage.rpartition('_TC')[2]
    
    text = '<form id="testCaseHistory"><fieldset id="testCaseHistoryFields" class="collapsed"><legend class="foldable" style="cursor: pointer;"><a href="#no3"  onclick="expandCollapseSection(\'testCaseHistoryFields\')">Status change history</a></legend>'
    text += test_manager_system.get_testcase_status_history_markup(tc)
    text += '</fieldset></form>'

    return text
    

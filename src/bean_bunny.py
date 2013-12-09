#!/usr/bin/python

__author__ = "ccheever"
__doc__ = """
Bean Bunny - The Puppet Labs social bookmark service.
"""
__date__ = "Thu Feb 12 09:05:40 PST 2009"

import re
import urlparse

import bunny1
from bunny1 import cherrypy
from bunny1 import Content
from bunny1 import q
from bunny1 import qp
from bunny1 import expose
from bunny1 import dont_expose
from bunny1 import escape
from bunny1 import HTML

class BeanCommands(bunny1.Bunny1Commands):
    def jira(self, arg):
        """Jira quick search https://confluence.atlassian.com/display/JIRA061/Using+Quick+Search"""
        return "https://tickets.puppetlabs.com/secure/QuickSearch.jspa?searchString=%s" % arg
    j = jira

    def confluence_page(self, arg):
        """Jump to Confluence wiki page"""
        return "https://confluence.puppetlabs.com/display/%s" % q(arg) 
    cp = confluence_page

    def confluence_search(self, arg):
        """Search Confluence wiki"""
        return "https://confluence.puppetlabs.com/dosearchsite.action?queryString=%s" % qp(arg) 
    c = confluence_search

    def map(self,arg):
        """Show office map"""
        return "http://officemap.ops.puppetlabs.net/index"
    m = map

    def google_site(self, arg):
        """Search Puppetlabs Google sites"""
        return "https://sites.google.com/a/puppetlabs.com/main/system/app/pages/search?scope=search-site&q=%s" % qp(arg)
    gs = google_site

    def info(self, arg):
        """Company info page"""
        return "https://sites.google.com/a/puppetlabs.com/main/company-information"

    def supplies(self, arg):
        """Office supplies provider. Send link to supplies to Char (char@puppetlabs.com)"""
        return "http://www.jthayer.com/"

    def library(self, arg):
        """Puppet Library search"""
        if len(arg) > 0:
           return "http://www.librarything.com/catalog/puppetlabs&deepsearch=%s" % qp(arg) 
        else:
            return "http://www.librarything.com/catalog/puppetlabs"

    def meeting(self, arg):
        """Book a meeting room"""
        return "http://meat.ops.puppetlabs.net/"
    meat = meeting
    meet = meeting

    def okr(self, arg):
        """Company Objectives and Key Results"""
        return "https://sites.google.com/a/puppetlabs.com/okr/home"

    def org(self, arg):
        """Company Org Chart"""
        return "https://docs.google.com/a/puppetlabs.com/spreadsheet/ccc?key=0Ah_PiMXjsxASdHhLS0NuZnRfb0pXZzVqUWpJMGJMT2c#gid=0"

    def redmine(self, arg):
        """Redmine issue tracking (migrating to Jira)"""
        if len(arg) > 0:
            return "https://projects.puppetlabs.com/search?q=%s" % qp(arg)
        else:    
            return "https://projects.puppetlabs.com"
    r = redmine

    def printing(self, arg):
        """How to print"""
        return "https://puppetlabs.atlassian.net/wiki/display/OPS/Printer+Setup"

    def phone(self, arg):
        """How to phones"""
        return "https://puppetlabs.atlassian.net/wiki/display/OPS/ShoreTel+Phone"
    phones = phone

    def github(self, arg):
        """Open/search github"""
        if len(arg) > 0:
            return "https://github.com/search?q=%s" % qp(arg)
        else:
            return "https://github.com/"
    gh = github

    def hipchat(self, arg):
        """Open hipchat client or search hipchat logs"""
        if len(arg) > 0:
            return "https://puppetlabs.hipchat.com/search?q=%s" % qp(arg)
        else:
            return "https://puppetlabs.hipchat.com/chat"
    h = hipchat
    hc = hipchat

    def fax(self, arg):
         """How to fax"""
         return "https://sites.google.com/a/puppetlabs.com/main/home/basic-business-practices/howto-send-and-get-a-fax"

    def gmail(self, arg):
        """Open/search gmail"""
        if len(arg) > 0:
            return "https://mail.google.com/mail/u/0/#apps/%s" % qp(arg)
        else:
            return "https://mail.google.com/mail/u/0/#inbox"
    gm = gmail

    def gcal(self, arg):
        """Open calendar"""
        return "https://www.google.com/calendar/render?tab=mc"
    gc = gcal

    def gdrive(self, arg):
        """Open/search Google Drive"""
        if len(arg) > 0:
            return "https://drive.google.com/a/puppetlabs.com/?tab=mo#search/%s" % qp(arg)
        else:
            return "https://drive.google.com/a/puppetlabs.com/?tab=mo#my-drive"
    gd = gdrive

    # ... and you can add other commands by just defining more methods
    # in this class here

class BeanBunny(bunny1.Bunny1):
    def __init__(self):
        bunny1.Bunny1.__init__(self, BeanCommands(), bunny1.Bunny1Decorators())

    @cherrypy.expose
    def header_gif(self):
        """the banner GIF for the bunny1 homepage"""
        cherrypy.response.headers["Content-Type"] = "image/gif"
        return bunny1.bunny1_file("header.gif")

if __name__ == "__main__":
    bunny1.main(BeanBunny())



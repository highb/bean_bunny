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
        """HOW-TO print"""
        return "https://puppetlabs.atlassian.net/wiki/display/OPS/Printer+Setup"

    def phone(self, arg):
        """HOW-TO phone"""
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
         """HOW-TO fax"""
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

    def trello(self, arg):
        """Open/Search Trello board"""
        if len(arg) > 0:
            return "https://trello.com/search?q=%s" % arg
        else:
            return "https://trello.com/puppetlabs"
    tr = trello
    # ... and you can add other commands by just defining more methods
    # in this class here

    def puppet_docs(self, arg):
        """Open/Search Puppet docs"""
        if len(arg) > 0:
            return "https://www.google.com/#q=site:docs.puppetlabs.com+%s" % qp(arg)
        else:
            return "http://docs.puppetlabs.com/"
    pd = puppet_docs

    def puppet_forge(self, arg):
        """Open/Search Puppet forge"""
        if len(arg) > 0:
            return "http://forge.puppetlabs.com/modules?q=%s" % qp(arg)
        else:
            return "http://forge.puppetlabs.com/"
    pf = puppet_forge

    def directory(self, arg):
        """Company directory"""
        return "https://sites.google.com/a/puppetlabs.com/main/company-information/directory"
    d = directory

    @dont_expose
    def _help_html(self, examples=None, name="bean_bunny"):
        """the help page that gets shown if no command or 'help' is entered
        This horrible return would probably be better suited as a template.
        """

        import random

        def bookmarklet(name):
            return """<a href="javascript:bunny1_url='""" + self._base_url() + """?';cmd=prompt('bunny1.  type &quot;help&quot; to get help or &quot;list&quot; to see commands you can use.',window.location);if(cmd){window.location=bunny1_url+escape(cmd);}else{void(0);}">""" + name + """</a>"""

        if not examples:
            examples = [
                    "pd types",
                    "pf mysql",
                    "hc enterprise",
                    "j PE-1234",
                    "gm all@puppetlabs.com",
                    "c onboarding",
                    "gs onboarding",
                    "gh puppetlabs",
                    "g whizbang api reference",
                    ]

        return """
<html>
<head>
<title>bean_bunny</title>
""" + self._opensearch_link() + """
<style>
BODY {
    font-family: Sans-serif;
    width: 800px;
}

code {
    color: darkgreen;
}

A {
    color: #3B5998;
}

small {
    width: 800px;
    text-align: center;
}

.header {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 30px;
}

.test-query-input {
    width: 487px;
    font-size: 20px;
}

.header-placeholder {
    height: 45px;
}

</style>
</head>
<body>
<h1 class="header-placeholder"><img class="header" src="header.png" /></h1>

<p>""" + name + """ is a tool that lets you write smart bookmarks in python and then share them across all your browsers and with a group of people or the whole world.  It was developed at <a href="http://www.facebook.com/">Facebook</a> and is widely used there.</p>

<form method="GET">
<p style="width: 820px; text-align: center;"><input class="test-query-input" id="b1cmd" type="text" name="___" value=""" + '"' + escape(random.choice(examples)) + '"' + """/> <input type="submit" value=" try me "/></p>

<p>Type something like """ + " or ".join(["""<a href="#" onclick="return false;"><code onclick="document.getElementById('b1cmd').value = this.innerHTML; return true;">""" + x + "</code></a>" for x in examples]) + """.</p>

<p>Or you can see <a href="?list">a list of shortcuts you can use</a> with this example server.</p>

<h3>Installing on Google Chrome</h3>
<ul>Choose <code>Settings</code> from the wrench menu to the right of the location bar in Chrome.</ul>
<ul>Under the section <code>Search</code>, click the <code>Manage search engines...</code> button.</ul>
<ul>Click the <code>Add</code> button and then fill in the fields name, keyword, and URL with <code>""" + name + """</code>, <code>bb</code>, and <code>""" + self._base_url() + """?%s</code></ul>
<ul>Hit <code>OK</code> and then select """ + name + """ from the list of search engines and hit the <code>Make Default</code> button to make """ + name + """ your default search engine.</ul>
<ul>Type <code>list</code> into your location bar to see a list of commands you can use.</ul>

<h3>Installing on Firefox</h3>
<ul>Choose <code>Add "bean_bunny"</code> from the search engine dropdown in the upper right.</ul>
<ul>Now, type <code>list</code> or <code>wp FBML</code> into your location bar and hit enter.</ul>
<ul>Also, if you are a Firefox user and find bunny1 useful, you should check out <a href="http://labs.mozilla.com/projects/ubiquity/">Ubiquity</a>.</ul>

<h3>Installing on Safari</h3>
<ul>Drag this bookmarklet [""" + bookmarklet(name) + """] to your bookmarks bar.</ul>
<ul>Now, visit the bookmarklet, and in the box that pops up, type <code>list</code> or <code>g facebook comments widget video</code> and hit enter.</ul>
<ul>In Safari, one thing you can do is make the bookmarklet the leftmost bookmark in your bookmarks bar, and then use <code>Command-1</code> to get to it.</ul>
<ul>Alternatively, you can get the location bar behavior of Firefox in Safari 3 by using the <a href="http://purefiction.net/keywurl/">keywurl</a> extension.</ul>

<h3>Installing on Internet Explorer</h3>
<ul>There aren't any great solutions for installing """ + name + """ on IE, but two OK solutions are:</ul>
<ul>You can use this bookmarklet [""" + bookmarklet(name) + """] by dragging into your bookmarks bar and then clicking on it when you want to use """ + name + """.</ul>
<ul>Or, in IE7+, you can click the down arrow on the search bar to the right of your location bar and choose the starred """ + name + """ option there.  This will install the bunny OpenSearch plugin in your search bar.</ul>

<h3>Running Your Own bunny1 Server</h3>
<ul>Download the <a href="http://github.com/ccheever/bunny1/">source code</a> for the project.  Or if you use setuptools, you can just <code>easy_install bunny1</code>.</ul>

<ul>To run an example server, just run <code>b1_example.py --port=8080</code>.</ul>

<ul>More detailed instructions for configuring and running your own server can be found in the <a href=""" + '"' + self._base_url() + """?readme">README</a>.  You can add your own commands with just a few lines of python.</ul>

<hr />
<small>bunny1 was originally written by <a href="http://www.facebook.com/people/Charlie-Cheever/1160">Charlie Cheever</a> at <a href="http://developers.facebook.com/opensource.php">Facebook</a> and is maintained by him, <a href="http://www.facebook.com/people/David-Reiss/626221207">David Reiss</a>, Eugene Letuchy, and <a href="http://www.facebook.com/people/Daniel-Corson/708561">Dan Corson</a>.  Julie Zhuo drew the bunny logo.</small>


</body>
</html>
        """

class BeanBunny(bunny1.Bunny1):
    def __init__(self):
        bunny1.Bunny1.__init__(self, BeanCommands(), bunny1.Bunny1Decorators())

    @cherrypy.expose
    def header_png(self):
        """the banner PNG for the bunny1 homepage"""
        cherrypy.response.headers["Content-Type"] = "image/png"
        return bunny1.bunny1_file("header.png")

if __name__ == "__main__":
    bunny1.main(BeanBunny())



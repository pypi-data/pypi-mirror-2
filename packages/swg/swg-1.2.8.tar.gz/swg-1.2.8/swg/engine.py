# -*- coding: utf-8 -*-
# This file is part of SWG (Static Website Generator).
#
# Copyright(c) 2010-2011 Simone Margaritelli
# evilsocket@gmail.com
# http://www.evilsocket.net
# http://www.backbox.org
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import sys
import os.path
import re
import shutil
import SimpleHTTPServer
import SocketServer

from swg.core.config      import Config
from swg.core.pageparser  import PageParser
from swg.entities.page    import Page

class Engine:
  __instance = None

  def __init__(self):
    self.config  = Config.getInstance()
    self.dbdir   = os.path.join( self.config.dbpath, 'pages' )
    self.files   = os.listdir( self.dbdir ) if os.path.exists( self.dbdir ) else []
    self.path    = os.path.dirname( os.path.realpath( __file__ ) )
    self.pages   = []
    self.statics = None
    self.index   = None
    self.e404    = None
    self.sitemap = None
    self.feed    = None

  def getPageByTitle( self, title, caseSensitive = True ):
    lwr_title = title.lower() if caseSensitive is False else None
    for page in self.pages:
      if page.title == title or (caseSensitive is False and page.title.lower() == lwr_title):
        return page

    return None

  def getStaticPages( self ):
    if self.statics is None:
      self.statics = filter( lambda page: page.static is True, self.pages )

    return self.statics

  def new( self ):
    maxid = 0
    for file in self.files:
      ( id, ext ) = file.split('.')
      if int(id) > maxid:
        maxid = int(id)
    
    newitem = os.path.join( self.dbdir, "%d.%s" % (maxid + 1, self.config.dbitem_ext) )
    fd      = open( newitem, 'w+t' )

    fd.write( """\
Date: %s
Author:
Categories:
Tags:
Title:

""" % self.config.now.strftime("%Y-%m-%d %H:%M:%S") )

    fd.close()
    
    os.system( "%s %s" % ( self.config.editor, newitem ) )

    if os.path.exists( newitem ):
      print "@ Item '%s' created, you can now regenerate the website ." % newitem
    else:
      print "@ Item was not saved, quitting ."

  def create( self, destfolder ):
    if os.path.exists(destfolder):
      sys.exit( "@ The folder '%s' already exists, operation interrupted for security reasons." % destfolder )  
    else:
      print "@ Creating SWG basic website structure inside the '%s' folder ..." % destfolder

      shutil.copytree( os.path.join( self.path, 'basic' ), destfolder )

      print """\
@ Basic website initialized, now run:

  cd %s
  swg --generate

To generate the html contents or:

  cd %s
  swg --serve

To test the website locally.""" % (destfolder,destfolder)

  def serve( self ):

    class SWGServer(SocketServer.TCPServer):
      allow_reuse_address = True

    self.config.siteurl = 'http://localhost:8080'
    self.generate()

    os.chdir( self.config.outputpath )

    print "\n@ Serving the site on http://localhost:8080/ press ctrl+c to exit ..."
    
    try:
      SWGServer( ("",8080), SimpleHTTPServer.SimpleHTTPRequestHandler ).serve_forever()
    except KeyboardInterrupt:
      print "\n@ Bye :)"

  def generate( self ):
    parser = PageParser( )
    
    print "@ Parsing pages ..."
    for file in self.files:
      if re.match( '^.+\.' + self.config.dbitem_ext + '$', file ):
        filename = os.path.join( self.dbdir, file )
        page     = parser.parse( filename )
        self.pages.append(page)

    print "@ Sorting pages by date ..."
    self.pages.sort( reverse=True, key=lambda p: p.datetime )

    # delete output directory and recreate it
    if os.path.exists(self.config.outputpath ):
      print "@ Removing old '%s' path ..."  % self.config.outputpath
      shutil.rmtree( self.config.outputpath )

    print "@ Creating '%s' path ..." % self.config.outputpath
    os.mkdir( self.config.outputpath )

    for source, destination in self.config.copypaths.items():
      print "@ Importing '%s' to '%s' ..." % (source, destination)
      if os.path.isfile(source):
        shutil.copy( source, destination )
      elif os.path.isdir(source):
        shutil.copytree( source, destination )
      else:
        raise Exception("Unexpected type of '%s' ." % source )

    if os.path.exists( os.path.join( self.config.tplpath, 'index.tpl' ) ):
      print "@ Creating index file ..."
      self.index = Page( 'index', 'index.tpl' )
      self.index.addObjects( { 'pages' : self.pages, 'swg' : self } )
      self.index.create()
    else:
      raise Exception( "No index template found." )

    if os.path.exists( os.path.join( self.config.tplpath, '404.tpl' ) ):
      print "@ Creating 404 file ..."
      self.e404 = Page( '404', '404.tpl' )
      self.e404.addObjects( { 'pages' : self.pages, 'swg' : self } )
      self.e404.create()

    if os.path.exists( os.path.join( self.config.tplpath, 'feed.tpl' ) ):
      print "@ Creating feed.xml file ..."
      self.feed = Page( 'feed', 'feed.tpl' )
      self.feed.addObjects( { 'pages' : self.pages, 'swg' : self } )
      self.feed.extension = 'xml'
      self.feed.create()

    print "@ Rendering %d pages ..." % len(self.pages)
    for page in self.pages:
      page.addObjects( { 'pages' : self.pages, 'swg' : self } ).create()

    if os.path.exists( os.path.join( self.config.tplpath, 'sitemap.tpl' ) ):
      print "@ Creating sitemap.xml file ..."
      self.sitemap = Page( 'sitemap', 'sitemap.tpl' )
      self.sitemap.addObjects( { 'index' : self.index, 'pages' : self.pages, 'swg' : self } )
      self.sitemap.extension = 'xml'
      self.sitemap.create()

    if self.config.gzip is True:
      htaccess = os.path.join( self.config.outputpath, '.htaccess' ) 
      if os.path.exists( htaccess ):
        fd = open( htaccess, "a+t" )
        fd.write( """
  # SWG Generated Code
  AddEncoding gzip .gz
  DirectoryIndex index.html index.htm index.shtml index.php index.php4 index.php3 index.phtml index.cgi index.html.gz

  <Files *.""" + self.config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + self.config.page_ext + """)>
    RewriteEngine on
    RewriteCond %{REQUEST_FILENAME}.gz -f
    RewriteRule ^(.*)$ $1.gz [L]
  </FilesMatch>""" )
        fd.close()
      else:
        fd = open( htaccess, "w+t" )
        fd.write( """
  # SWG Generated Code
  Options +FollowSymlinks
  RewriteEngine on

  AddEncoding gzip .gz
  DirectoryIndex index.html index.htm index.shtml index.php index.php4 index.php3 index.phtml index.cgi index.html.gz

  <Files *.""" + self.config.page_ext + """.gz>
    ForceType text/html
  </Files>

  <FilesMatch .*\.(""" + self.config.page_ext + """)>
    RewriteEngine on
    RewriteCond %{REQUEST_FILENAME}.gz -f
    RewriteRule ^(.*)$ $1.gz [L]
  </FilesMatch>""" )
        fd.close()

    print "@ DONE\n"

    if self.config.transfer is not None:
      os.system( self.config.transfer.encode( "UTF-8" ) )
    
  @classmethod
  def getInstance(cls):
    if cls.__instance is None:
      cls.__instance = Engine()
    return cls.__instance

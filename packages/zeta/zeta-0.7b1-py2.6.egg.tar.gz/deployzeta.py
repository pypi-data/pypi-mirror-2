#! /usr/bin/env python

# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2009 SKR Farms (P) LTD.

# Gotcha : 
#   1. --no-site-packages is not included as option, since 'python-xapian' is
#      not properly installed.
#
# Notes  :
#   1. An alternate thought was to do deployment via setup-tools framework.
#      But, we will be most of the time, deploying the application in virtual
#      environment, on which easy_install itself will be depending on. Also,
#      we have decided to leave the installation part seperated from the
#      deployment part.

import sys
import getopt
from   optparse     import OptionParser
import os
from   os.path      import basename, abspath, dirname, isdir, isfile, join
import shutil       as sh

progname = basename( __file__ )
usage    = "usage: %prog [options] <name> <zetaegg> <zwikiegg>"
pyver    = "%s.%s" % sys.version_info[:2]
python   = 'python%s' % pyver

try :
    import pysvn
    import xapian
    import MySQLdb
    localpysvn   = dirname( pysvn.__file__ )
    localmysqldb = dirname( MySQLdb.__file__ )
    localxapian  = xapian.__file__
except :
    print "Failed %s ..." % sys.exc_info()[1]

def _cmdexecute( cmd, log=True ) :
    if log :
        print "  %s" % cmd
    rc = os.system( cmd )
    if rc != 0 :
        raise Exception( "Command failed `%s`" % cmd )


def _virtualenv( name ) :
    """Create a virtual environment for the deployment"""

    print "...... Creating Virtual environment for %s ... " % name
    _cmdexecute(
        "virtualenv --python=python%s --no-site-packages %s" % ( pyver, name ),
        log=True
    )
    print "\n"


def _installz( name, zetaegg, zwikiegg, depeggs=[], options=None ) :
    """Install zeta and zwiki packages, make sure that easy_install is
    executed in the virtual environment.

    If `findlinks` option is specified, then egg files will be fetched from
    that directory

    If `noindex` option
        is to make sure that easy_install looks for egg packages only in
        directories specified with -f option.
    similar to -H None
    """

    ei_opts = ''
    if options and options.noindex :
        ei_opts += ' -H None '
    if options and options.findlinks :
        ei_opts += '-f %s' % options.findlinks

    for depegg in depeggs :
        cmds = []
        cmds.append( 'source %s/bin/activate' % name )
        print "...... Activating Virtual environment and installing %s ... " % \
              depegg
        cmds.append( 'easy_install-%s %s %s' % (pyver, ei_opts, depegg) )
        cmd = '; '.join( cmds )
        _cmdexecute( 'bash -c "%s"' % cmd )
        print "\n"

    print "...... Activating Virtual environment and installing Zeta, Zwiki  ... "
    cmds = []
    cmds.append( 'source %s/bin/activate' % name )
    cmds.append( 'easy_install-%s %s %s' % (pyver, ei_opts, zwikiegg) )
    cmds.append( 'easy_install-%s %s %s' % (pyver, ei_opts, zetaegg) )
    cmd  = '; '.join( cmds )
    _cmdexecute( 'bash -c "%s"' % cmd )
    print "\n"


def _linksitepkgs( name ) :
    """Since --no-site-packages option was used with virtual environment,
    packages that are not available via easy_install will be referenced back
    to systems (OS specific) site-packages
        pysvn      -> <sysdir>/lib/python../site-packages/pysvn
        xapian     -> <sysdir>/lib/python../site-packages/xapian
        _xapian.so -> <sysdir>/lib/python../site-packages/_xapian.so
    """

    print "...... Linking pysvn into the virtual environment ..."
    _cmdexecute( 
        "ln -sf %s %s/lib/python%s/site-packages" % (localpysvn, name, pyver)
    )
    print "\n"

    print "...... Linking python-xapian into the virtual environment ... "
    xapdir = dirname( localxapian )
    _cmdexecute(
        "ln -sf %s %s/lib/python%s/site-packages" % (localxapian, name, pyver)
    )
    _cmdexecute(
        "ln -sf %s/_xapian.so %s/lib/python%s/site-packages" % ( xapdir, name, pyver )
    )
    print "\n"


virtzsh = """
#! /usr/bin/env bash
source %s/bin/activate
"""
def _configapp( name ) :
    """
    * Create script to load the virtual environement from shell
    * Under the virtual environment, config-app
    * Create egg-cache/ directory
    """

    print "...... Creating script to enter into virtual environment ..."
    open( 'virtz-%s.sh' % name, 'w' ).write( virtzsh % name )
    _cmdexecute( 'chmod +x virtz-%s.sh' % name )
    print "\n"

    print "...... Creating production.ini ... "
    cmds = []
    cmds.append( 'source %s/bin/activate' % name )
    cmds.append( 'paster make-config "zeta" production.ini' )
    cmd  = '; '.join( cmds )
    _cmdexecute( 'bash -c "%s"' % cmd )
    print "\n"

    print "...... Creating egg-cache/ directory ... "
    os.mkdir( 'egg-cache' )
    print "\n"

    print "Follow the deployment manual to complete the rest of the deployment !\n"


def _fetcheggs( destdir, zetaegg, zwikiegg, depeggs=[] ) :
    """Just fetch the egg files in zipped format and save in under
    `destdir`"""

    pathdir = join( destdir, 'lib', 'python%s'%pyver, 'site-packages' )
    print "...... Creating the egg source directory %s ..." % pathdir
    not os.path.isdir(pathdir) and os.makedirs(pathdir)
    pypath = 'PYTHONPATH=%s' % pathdir

    for depegg in depeggs :
        print "...... Egg setup for %s ..." % depegg
        _cmdexecute(
            "%s; easy_install -U -z --prefix %s %s" % ( pypath, destdir, depegg )
        )

    print "...... Egg setup for %s ..." % zwikiegg
    _cmdexecute(
        "%s; easy_install -U -z --prefix %s %s" % ( pypath, destdir, zwikiegg )
    )

    print "...... Egg setup for %s ..." % zetaegg
    _cmdexecute(
        "%s; easy_install -U -z --prefix %s %s" % ( pypath, destdir, zetaegg )
    )
    print "\n"


def _upgradepkgs( name, zetaegg, zwikiegg ) :
    """Upgrade ZWiki and Zeta packages"""
    _installz( name, zetaegg, zwikiegg )


def _upgradewiki( name ) :
    """Upgrading database wiki translations to latest wiki version"""

    print "...... Upgrading wiki  ... "
    cmds = []
    cmds.append( 'source %s/bin/activate' % name )
    cmds.append( 'paster request production.ini /pasteradmin/upgradewiki' )
    cmd  = '; '.join( cmds )
    _cmdexecute( 'bash -c "%s"' % cmd )
    print "\n"


def _upgradeenv( name ) :
    """Upgrade environment directory"""

    print "...... Upgrading environment directory ... "
    cmds = []
    cmds.append( 'source %s/bin/activate' % name )
    cmds.append( 'paster request production.ini /pasteradmin/upgradeenv' )
    cmd  = '; '.join( cmds )
    _cmdexecute( 'bash -c "%s"' % cmd )
    print "\n"


def _upgradedb( name ) :
    """Upgrade database to latest version"""

    print "...... Upgrading database  ... "
    cmds = []
    cmds.append( 'source %s/bin/activate' % name )
    cmds.append( 'paster request production.ini /pasteradmin/upgradedb' )
    cmd  = '; '.join( cmds )
    _cmdexecute( 'bash -c "%s"' % cmd )
    print "\n"


def _upgrade( name, zetaegg, zwikiegg, options ) :
    """UPGRADE"""
    if options.upgradepkgs :
        _upgradepkgs( name, zetaegg, zwikiegg )
    if options.upgradewiki :
        _upgradewiki( name )
    if options.upgradeenv :
        _upgradeenv( name )
    if options.upgradedb :
        _upgradedb( name )


def cmdoptions() :
    op = OptionParser( usage=usage )
    op.add_option( "--eggs", dest="fetcheggs", default="",
                   help="Fetch all the egg files to the <fetcheggs> directory" )

    op.add_option( "-H", dest="noindex", action="store_true", default=False,
                   help="Do not look up into python package index" )

    op.add_option( "-f", dest="findlinks", default="",
                   help="Use the directory to search for egg files" )

    op.add_option( '--upgrade-pkgs', dest='upgradepkgs', action='store_true', default=False,
                   help='Upgrade Zeta and zwiki pkgs' )

    op.add_option( '--upgrade-wiki', dest='upgradewiki', action='store_true', default=False,
                   help='Upgrade wiki translations' )

    op.add_option( '--upgrade-db', dest='upgradedb', action='store_true', default=False,
                   help='Upgrade Database' )

    op.add_option( '--upgrade-env', dest='upgradeenv', action='store_true', default=False,
                   help='Upgrade Environment directory' )

    op.add_option( '--upgrade', dest='upgradeall', action='store_true', default=False,
                   help='Upgrade entire deployment' )

    options, args = op.parse_args()

    if options.upgradeall :
        options.upgradepkgs = True
        options.upgradewiki = True
        options.upgradedb   = True
        options.upgradeenv  = True

    options.upgrade = options.upgradepkgs or options.upgradewiki or \
                      options.upgradedb or options.upgradeenv

    return op, options, args


if __name__ == '__main__' :
    op, options, args = cmdoptions()
    if len(args) >= 3 :
        options.name     = args[0]
        options.zetaegg  = abspath( args[-2] )
        options.zwikiegg = abspath( args[-1] )
        options.depeggs  = []
        if len(args) > 3 :
            options.depeggs = [ abspath(depegg) for depegg in args[1:-2] ]
        if options.fetcheggs :
            _fetcheggs( options.fetcheggs, options.zetaegg, options.zwikiegg,
                        depeggs=options.depeggs )
        elif options.upgrade :
            _upgrade( options.name, options.zetaegg, options.zwikiegg, options )
        elif len(args) >= 3 :
            _virtualenv( options.name )
            _installz( options.name, options.zetaegg, options.zwikiegg,
                       depeggs=options.depeggs,
                       options=options )
            _linksitepkgs( options.name )
            _configapp( options.name )
    else :
        op.print_help()

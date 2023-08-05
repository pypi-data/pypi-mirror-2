#!/usr/bin/python 
import os
import sys

lib_dir = os.path.abspath(os.path.dirname(__file__) + '/../lib')
if os.path.exists(os.path.join(lib_dir, 'mozilla')):
  sys.path.append(lib_dir)

from optparse import OptionParser
from time import clock
from mozilla.core.comparelocales import *
import silme.format
import mozilla

silme.format.Manager.register('dtd', 'properties', 'ini', 'inc')

if __name__ == '__main__':
  usage = 'usage: %prog [options] l10n.ini l10n_base_dir language1'
  usage += ' [language2 ...]\n'
  usage += 'language1 may be \'all\' - in that case the \'alllocales\' '+ \
           'file will be used'
  parser = OptionParser(usage, version='%prog '+mozilla.get_short_version())
  parser.add_option('-i', '--input', default='source', dest='inputtype',
                  metavar='MODE', help='Set the input type [default: source] '+
                  'Valid input types:\n' +
                  'source, xpi, xpis, jar, dir, file')
  parser.add_option('-r', '--reference', default='en-US', dest='reference',
                  metavar='LOCALE', help='Explicitly set the reference '+
                  'localization. [default: en-US]')
  parser.add_option('-o', '--output', type='int', default=0, dest='output',
                  metavar='MODE', help='Output style: 0 = tree; 1 = full '+
                  'tree; 2 = full relative paths')
  parser.add_option('-l', '--forcelocaledir', dest='forcelocaledir', default=False,
                  action='store_true',
                  help='Look for en-US in the locale dir instead of app dir')
  parser.add_option('-f', '--compareeverydir', dest='force', default=False,
                  action='store_true',
                  help='Compare every dir, even optional dirs that are not ' +
                  'included in the all-locales file.')
  parser.add_option('-e', '--testref',
                  action='store_true', dest='testreference', default=False,
                  help='Test the reference files itself for problems. '+
                  'Needs the \'-a\' option to be activated!')
  parser.add_option('-t', '--turbo',
                  action='store_true', dest='turbo', default=False,
                  help='Skip the comparison of strings - '+
                  'look only for added / removed entities or files')
  parser.add_option('-a', '--accesskeys',
                  type='int', dest='accesskeys', default=0,
                  metavar='AKEYS',
                  help='Basic acceskeys check - '+
                  'checks if the accesskeys are matching the labels.\n' +
                  'Available levels:\n' +
                  '1 - show just errors\n' +
                  '2 - show errors and important warnings\n' +
                  '3 - show all errors and warnings')
  parser.add_option('-c', '--checkvalidity',
                  action='store_true', dest='checkvalidity', default=False,
                  help='Basic label tests')
  parser.add_option('-d', '--download',
                  action='store_true', dest='mercurial', default=False,
                  help='EXPERIMENTAL: read Mercurial repositories - '+
                  'automatically (clone or pull && update -C)')
  parser.add_option('--debug',
                  action='store_true', dest='debug', default=False,
                  help='Small helper to see where we are loosing time...')
  parser.add_option('-p', '--compatibility',
                  action='store_true', dest='compatibility', default=False,
                  help='Activate compare-locales 0.5/0.6 compatibility mode')
  parser.add_option('-j', '--json', default='full', dest='returnvalue',
                  metavar='JSON', help='Uses JSON for output '+
                  'parameter "full_json". [default: "full"]')
  parser.add_option('-m', '--merge', dest='merge', default=None, metavar='PATH',
                  help='Use this directory to stage merged files')
  parser.add_option('--verbose', type='int',
                  dest='verbose', default=5,
                  metavar='LEVEL', help='Sets the verbose level:\n' +
                  '0 - quiet, 5 - show all')
  (options, args) = parser.parse_args()
  if options.inputtype == 'source':
    if len(args) < 3:
      parser.error('At least one language required')
    inipath, l10nbase = args[:2]
    locales = args[2:]
  elif options.inputtype == 'xpi':
    if len(args) < 1:
      parser.error('Path to the XPI-file required')
    inipath = args[:1][0]
    l10nbase = None
    locales = args[1:]
  elif options.inputtype == 'file':
    if len(args) < 2:
      parser.error('Two file paths required')
    l10nbase, inipath = args[:2]
    if len(args) == 3:
      locales = args[2:]
    else:
      if len(os.path.basename(args[1])) > 0:
          locales = [os.path.basename(args[1])]
      else:
          locales = [args[1]]
  elif options.inputtype == 'dir':
    if len(args) < 2:
      parser.error('Two dir paths required')
    l10nbase, inipath = args[:2]
    if len(args) == 3:
      locales = args[2:]
    else:
      if len(os.path.basename(args[1])) > 0:
          locales = [os.path.basename(args[1])]
      else:
          locales = [os.path.dirname(args[1])]
  elif options.inputtype == 'jar':
    if len(args) < 2:
      parser.error('Two jar paths required')
    inipath, l10nbase = args[:2]
    if len(args) == 3:
      locales = args[2:]
    else:
      locales = [args[1]]
  elif options.inputtype == 'xpis':
    if len(args) < 4:
      parser.error('Two xpi and two jar paths required')
    inipath = args[:2]
    l10nbase = args[2:4]
    if len(args) == 5:
      locales = args[4:]
    else:
      locales = [os.path.basename(args[1])]
  else:
    inipath = None
    l10nbase = None
    locales = None
  
  optionpack = CompareInit(reference = options.reference,
                           inipath = inipath, 
                           l10nbase = l10nbase,
                           locales = locales,
                           turbo = options.turbo,
                           accesskeys = options.accesskeys,
                           mercurial = options.mercurial,
                           merge = options.merge,
                           testreference = options.testreference,
                           output = options.output,
                           inputtype = options.inputtype,
                           checkvalidity = options.checkvalidity,
                           verbose = options.verbose,
                           compatibility = options.compatibility,
                           returnvalue = options.returnvalue,
                           force = options.force,
                           forcelocaledir = options.forcelocaledir)
  
  starttime = clock()
  
  if not options.debug:
    try:
      import psyco
      psyco.full()
    except ImportError:
      print 'INFO: psyco not available. L10n Completeness Check will still work ' + \
            'correctly, but much slower.\n'
    # Start the main-method
    compareLocales(optionpack)
  else:
    import profile
    profile.run('compareLocales(optionpack)')
    
  endtime = clock()
  print 'We needed ' + str(endtime-starttime) + ' seconds to compare ' + \
        str(len(optionpack.locales)) + ' locale(s) with ' + \
        optionpack.reference + ' as the reference.\n'

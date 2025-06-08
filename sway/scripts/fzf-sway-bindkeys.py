#!/bin/env python
# vim:autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:
"""
Copyright 2025 iZoom

"""
# {{{ import block
import sys
import re
from   argparse   import ArgumentParser     #, RawTextHelpFormatter
from   pathlib    import Path
from   subprocess import run                #, Popen, PIPE
# }}}

##
## main code
##
# {{{ setting of global variables
__doc__    = "La programo serchas ed prizentas kun-liguri dil komandi exekutata kun klavo-kombini"

ore_set    = re.compile(r'set\s')
ore_bind   = re.compile(r'bind')
ore_incl   = re.compile(r'include\s+(.*)$')
ore_mode   = re.compile(r'mode\s.*\{$')
ore_rbrace = re.compile(r'^}$')

pconf      = Path.home() / '.config/sway/config'

# pp         = pprint.PrettyPrinter( indent=2 )
# }}}

##
## {{{ function's definitions
##

def mk_cfg_array( f, aconf ):
    # {{{ korpo
    # global includes
    in_mode = False
    indent = ''
    try:
        for l in f:
            stmp = l.strip()
            if  len(stmp) > 0 and stmp[0] != '#':
                for ore in ( ore_set, ore_bind, ore_mode, ore_rbrace, ore_incl ):
                    if  ore.match( stmp ):
                        if  ore is ore_incl:
                            inc_file = ore.match( stmp ).group(1)
                            if  args.debug:
                                dbg_print( f"inc_file: {inc_file}. ore_incl: ", ore )
                            try:
                                with Path( inc_file ).expanduser().absolute().open('rt') as incf:
                                    aconf += mk_cfg_array( incf, [] )
                            except:
                                if  args.debug:
                                    dbg_print(f'Opening include file "{inc_file}" failed.')
                                pass
                            break
                        if  ore is ore_mode:
                            in_mode = True
                        if  ore is ore_rbrace:
                            if  in_mode:
                                in_mode = False
                                indent = ''
                            else:
                                break
                        aconf.append( indent + stmp )
                        if  in_mode:
                            indent = '  '
                        break
    except:
        raise Exception( f"Can't read {f.name}" )

    return aconf
    # }}}
## }}}

# {{{ argument's definition
# parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
parser = ArgumentParser(description=__doc__)
parser.add_argument("-f", "--file", metavar='CFG', type=str,
    help="config file for open")
# parser.add_argument("-v", "--verbose", action="store_true", 
#         help="programo esos maxime multevorta")
parser.add_argument("--debug", action="store_true", 
        help="ekpozar debug-informi")
# parser.add_argument("pattern", nargs='?', 
#         help="pattern for searching")

# }}}

args = parser.parse_args()

if  args.debug:
    import pprint
    pp = pprint.PrettyPrinter( indent=2 )

    def dbg_print( msg='Debug info:', obj=None ):
        """print debug info"""
        # {{{ korpo
        print(file=sys.stderr)
        print(msg, file=sys.stderr)
        if  obj:
            print(pp.pformat(obj), file=sys.stderr)
        # }}}

    dbg_print('Argumentes:', args)

if  args.file:
    pconf = Path(args.file).expanduser().absolute()

if  pconf.is_file():
    aconf = []
    # includes = []
    with pconf.open( mode='r' ) as f:
        aconf = mk_cfg_array( f, aconf )
    if  args.debug:
        dbg_print("aconf:", aconf)
    else:
        for l in aconf:
            print( l )
else:
    raise Exception( f"Can't open {pconf.name}" )

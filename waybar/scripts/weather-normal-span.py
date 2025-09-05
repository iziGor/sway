#!/usr/bin/env python3
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker :

import sys
import re

sreSpanStyle = r'<span style="([^>"]*?)">(.*?)</span>'

def parse(s):
    sRet = ''
    sFW  = 'font-weight:'
    sClr = 'color:'
    # aWgt = ( 'bold', 'normal' )
    last_pos = 0

    # print(f's = "{s.strip('\n')}"', file=sys.stderr)
    for mo in re.finditer(sreSpanStyle, s):
        # sRet = ''
        aTmp = []
        sStyle = mo.group(1)
        # print(f'sStyle = "{sStyle.strip('\n')}"', file=sys.stderr)
        for e in sStyle.split(';'):
            # print(f'e = "{e}"', file=sys.stderr)
            # if  sFW in e:
            if  sFW in e and 'bold' in e:
                aTmp.append('font_weight="bold"')
            elif sClr in e:
                aTmp.append('color="{}"'.format(e.replace(sClr, '').strip()))
        # print(aTmp, file=sys.stderr)
        sRet += ''.join(
            ( s[last_pos:mo.start(0)]
            , '<span '
            , ' '.join(aTmp)
            , '>'
            , mo.group(2)
            , '</span>'))
        last_pos = mo.end(0)
    sRet += s[last_pos:]
    return sRet


bfr = sys.stdin
aRes = []
if  not bfr.isatty() and bfr.readable():
    for s in bfr:
        aRes.append(parse(s.rstrip('\n')).replace('\\', r"\\" ).replace(r'"', r'\"'))
        # aRes.append(parse(s.strip()))

    print(r'\n'.join(aRes), end='')
else:
    print('Input string do not exist', file=sys.stderr)

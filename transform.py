#!/usr/bin/env python3

import html
from glob import glob
import re

for fn in glob('*.htm') + glob('de/*.htm') + ['index.html', 'de/index.html']:
    with open(fn, 'r') as f:
        content = f.read()
        ncontent = content
        for k, v in html.entities.html5.items():
            if not k.endswith(';'):
                k = k + ';'
            if k not in ['nbsp;', 'gt;', 'lt;', 'amp;']:
                ncontent = ncontent.replace('&'+k, v)
        ncontent = ncontent.replace('(c) L', '© L')
        ncontent = ncontent.replace('(C) L', '© L')

        if 'de' not in fn:
            ncontent = ncontent.replace(
                'view on github</a>',
                f'''view on github</a>
                <a href="https://braesicke.de/{fn}">view original German</a>''',
            )

        colormap = {
            '000000': 'black',
            '0000FF': 'brightblue',
            '006600': 'darkgreen',
            '009900': 'lightgreen',
            '3333FF': 'blue',
            '3366FF': 'lightblue',
            '808000': 'mustard',
            '990000': 'darkred',
            '990033': 'burgundy',
            '999999': 'darkgrey',
            '9C9C9C': 'darkgrey',
            'C0C0C0': 'lightgrey',
            'CFCFCF': 'lightgrey',
            'CC0000': 'red',
            'CC000': 'red',
            'CC33CC': 'lilac',
            'CC6600': 'tangerine',
            'CC66CC': 'lilac',
            'CCCC00': 'olive',
            'FF0000': 'red',
            'FF00FF': 'neon',
            'FF6666': 'pink',
            'FFCC00': 'yellow',
            'FFCC99': 'peach',
            'FFFFCC': 'lightyellow',
            'FFFFFC': 'offwhite'
        }
        for k, v in colormap.items():
            ncontent = re.sub(f'<td><b><font color="#?{k}">([^<]+)</font></b></td>', f'<td class="{v} bold">\\1</td>', ncontent, flags=re.I)
            ncontent = re.sub(f'<td><font color="#?{k}"><b>([^<]+)</b></font></td>', f'<td class="{v} bold">\\1</td>', ncontent, flags=re.I)
            ncontent = re.sub(f'<b> *<font color="#?{k}">([^<]+)</font> *</b>', f'<b class="{v}">\\1</b>', ncontent, flags=re.I)
            ncontent = re.sub(f'<i> *<font color="#?{k}">([^<]+)</font> *</i>', f'<i class="{v}">\\1</i>', ncontent, flags=re.I)
            ncontent = re.sub(f'<font color="#?{k}"> *<b>([^<]+)</b> *</font>', f'<b class="{v}">\\1</b>', ncontent, flags=re.I)
            ncontent = re.sub(f'<font color="#?{k}"> *<i>([^<]+)</i> *</font>', f'<i class="{v}">\\1</i>', ncontent, flags=re.I)
            ncontent = re.sub(f'<h1> *<font color="#?{k}">([^<]+)</font></h1>', f'<h1 class="{v}">\\1</h1>', ncontent, flags=re.I)
            ncontent = re.sub(f'<h2> *<font color="#?{k}">([^<]+)</font></h2>', f'<h2 class="{v}">\\1</h2>', ncontent, flags=re.I)
            ncontent = re.sub(f'<h3> *<font color="#?{k}">([^<]+)</font></h3>', f'<h3 class="{v}">\\1</h3>', ncontent, flags=re.I)
            ncontent = re.sub(f'<font color="#?{k}">(.*?)</font>', f'<span class="{v}">\\1</span>', ncontent, flags=re.I)

        ncontent = re.sub(f'<(\w+)> *<a name="(.*?)"></a>', f'<\\1 id="\\2">', ncontent, flags=re.I)
        ncontent = re.sub(f'<a name="(.*?)"></a><b', f'<b id="\\1"', ncontent, flags=re.I)
        ncontent = re.sub(f'<a name="(.*?)"></a><i', f'<i id="\\1"', ncontent, flags=re.I)
        ncontent = re.sub(f'<h2>\n *<i id="(.*?)"', f'<h2 id="\\1"><i', ncontent, flags=re.M)
        # todo: see git grep '<a name'
        ncontent = re.sub(f'<h2><a name="(.*?)">(.*?)</a></h2>', f'<h2 id="\\1">\\2</h2>', ncontent, flags=re.M)
        ncontent = re.sub(f'<h1><a name="(.*?)">(.*?)</a></h1>', f'<h1 id="\\1">\\2</h1>', ncontent, flags=re.M)
        ncontent = re.sub(f'<h3><a name="(.*?)">(.*?)</a></h3>', f'<h3 id="\\1">\\2</h3>', ncontent, flags=re.M)
        ncontent = re.sub(f'<h2><i><span class="lightgreen"><a name="(.*?)">(.*?)</a></span></i></h2>', f'<h2 id="\\1" class="lightgreen"><i>\\2</i></h3>', ncontent, flags=re.M)

        # https://stackoverflow.com/a/21014546/6691
        # will be bettter to transform these using <q>
        # ncontent = ncontent.replace('“', '"')
        # ncontent = ncontent.replace('”', '"')
        if content != ncontent:
            with open(fn, 'w') as fw:
                fw.write(ncontent)

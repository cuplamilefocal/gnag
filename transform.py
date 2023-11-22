import html
from glob import glob

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

        # https://stackoverflow.com/a/21014546/6691
        # will be bettter to transform these using <q>
        # ncontent = ncontent.replace('“', '"')
        # ncontent = ncontent.replace('”', '"')
        if content != ncontent:
            with open(fn, 'w') as fw:
                fw.write(ncontent)

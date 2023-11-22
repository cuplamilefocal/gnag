import html
from glob import glob

for fn in glob('*.htm') + ['index.html']:
    with open(fn, 'r') as f:
        content = f.read()
        ncontent = content
        ncontent = ncontent.replace('&quot;', '"')
        ncontent = ncontent.replace('&copy;', '©')
        if content != ncontent:
            with open(fn, 'w') as fw:
                fw.write(ncontent)

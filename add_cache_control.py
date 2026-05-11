with open('learning-adventure.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Add cache control meta tags after viewport meta
old = '<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">'
new = old + '\n<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n<meta http-equiv="Pragma" content="no-cache">\n<meta http-equiv="Expires" content="0">'

if old in h and 'Cache-Control' not in h:
    h = h.replace(old, new)
    with open('learning-adventure.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print('Added cache control, saved', len(h), 'bytes')
else:
    print('Cache control already present or viewport not found')

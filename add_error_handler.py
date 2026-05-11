with open('learning-adventure.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Add error display div and handler after <body> tag
old_body = '<body>'
new_body = '''<body>
<div id="errorDisplay" style="display:none;background:#ff4444;color:white;padding:10px;margin:10px;border-radius:8px;font-size:14px;z-index:9999;position:relative;"></div>
<script>
window.onerror = function(msg, url, line, col, err) {
  var d = document.getElementById('errorDisplay');
  if(d) { d.style.display='block'; d.innerHTML = '<b>JS Error:</b> ' + msg + ' (line ' + line + ')'; }
  console.error('Error:', msg, 'at line', line);
};
</script>'''

if old_body in h and 'errorDisplay' not in h:
    h = h.replace(old_body, new_body)
    with open('learning-adventure.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print('Added error handler, saved', len(h), 'bytes')
else:
    print('Error handler already present or body tag not found')

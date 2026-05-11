with open('learning-adventure.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Add diagnostic display after the title
old_title = '<div class="title">学习大冒险</div>'
new_title = old_title + '\n<div id="diagStatus" style="text-align:center;font-size:12px;color:#666;margin:5px 0;">Loading...</div>'

if old_title in h and 'diagStatus' not in h:
    h = h.replace(old_title, new_title)
    
    # Add status update in init function
    old_init = 'function init(){'
    new_init = 'function init(){\n  var ds = document.getElementById("diagStatus");\n  if(ds) ds.textContent = "QB: " + (typeof QUESTION_BANK === "undefined" ? "MISSING" : QUESTION_BANK.length) + " questions, Grade: " + currentGrade;'
    
    if old_init in h:
        h = h.replace(old_init, new_init)
        print('Added diag status')
    
    with open('learning-adventure.html', 'w', encoding='utf-8') as f:
        f.write(h)
    print('Saved', len(h), 'bytes')
else:
    print('Diag already present or title not found')

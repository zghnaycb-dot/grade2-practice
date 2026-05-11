with open('learning-adventure.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find and replace the problematic line in renderMap
old_line = '''    html += '<div class="map-node '+cls+'" onclick="'+((i<unlockedRegions)?'startQuizByRegion(''+r.replace(/'/g,"\\'")+'')':'')+'"><div class="mn-emoji">'+(i<unlockedRegions?'🗺️':'🔒')+'</div><div class="mn-name">'+r+'</div></div>';'''

new_line = '''    html += '<div class="map-node '+cls+'" data-region="'+r.replace(/"/g, '&quot;')+'" data-unlocked="'+(i<unlockedRegions)+'"><div class="mn-emoji">'+(i<unlockedRegions?'🗺️':'🔒')+'</div><div class="mn-name">'+r+'</div></div>';'''

if old_line in h:
    h = h.replace(old_line, new_line)
    print('Replaced problematic onclick line')
else:
    print('Could not find exact line, trying partial match...')
    # Try to find the line with map-node and onclick
    import re
    pattern = r"html \+= '<div class=\"map-node .*?onclick=.*?map-name>\"\+r\+'</div></div>';"
    match = re.search(pattern, h)
    if match:
        print('Found with regex at position:', match.start())
        print('Matched text:', match.group()[:100])
    else:
        print('Could not find with regex either')

# Now add event delegation after map.innerHTML = html
old_innerhtml = "  map.innerHTML = html;\n}"
new_innerhtml = '''  map.innerHTML = html;
  map.querySelectorAll('.map-node[data-unlocked="true"]').forEach(node => {
    node.onclick = () => startQuizByRegion(node.dataset.region);
  });
}'''

if old_innerhtml in h:
    h = h.replace(old_innerhtml, new_innerhtml)
    print('Added event delegation')
else:
    print('Could not find map.innerHTML line')

with open('learning-adventure.html', 'w', encoding='utf-8') as f:
    f.write(h)

print('Final size:', len(h), 'bytes')
print('Done!')

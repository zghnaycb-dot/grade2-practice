with open('learning-adventure.html', 'r', encoding='utf-8') as f:
    h = f.read()

print("Original:", len(h), "bytes")

# Fix 1: grade comparison (7 occurrences)
count = h.count('q.grade===currentGrade')
if count > 0:
    h = h.replace('q.grade===currentGrade', 'parseInt(q.grade)===parseInt(currentGrade)')
    print("Fixed", count, "grade comparisons")

# Fix 2: setGrade parseInt
if 'currentGrade = g;' in h:
    h = h.replace('currentGrade = g;', 'currentGrade = parseInt(g)||2;')
    print("Fixed setGrade")

# Fix 3: add debug logging
old = 'function renderSubjects(){'
new = 'function renderSubjects(){console.log("DEBUG", {currentGrade, qbLen: QUESTION_BANK?.length, sampleGrade: QUESTION_BANK?.[0]?.grade});'
if old in h:
    h = h.replace(old, new)
    print("Added debug logging")

with open('learning-adventure.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Final:", len(h), "bytes")
print("Done!")

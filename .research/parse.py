import re, json, collections
lines = open('.research/us2026.txt', encoding='utf-8').read().replace('\r','').split('\n')
MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
MON = re.compile(r'^!.*<span[^>]*>(.*?)</span>')
DAY = re.compile(r"^\|.*?'''(\d{1,2})'''\s*$")
TITLE = re.compile(r"^\|\s*''\[\[([^\]|]+)(?:\|([^\]]+))?\]\]''|^\|\s*''([^'|]+)''")

def month_of(raw):
    letters = re.sub(r'<[^>]+>', '', raw).strip().upper()
    ups = [m.upper() for m in MONTHS]
    if letters in ups:
        return MONTHS[ups.index(letters)]
    import difflib
    g = difflib.get_close_matches(letters, ups, n=1, cutoff=0.6)
    return MONTHS[ups.index(g[0])] if g else None

def clean(x):
    x = re.sub(r'<ref.*', '', x)
    x = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', x)
    x = re.sub(r'\[\[([^\]]+)\]\]', r'\1', x)
    x = re.sub(r'style="[^"]*"', '', x)
    return x.strip(' |').strip()

cur_m = cur_d = None
out = []
for ln in lines:
    m = MON.match(ln)
    if m and month_of(m.group(1)):
        cur_m, cur_d = month_of(m.group(1)), None
        continue
    d = DAY.match(ln)
    if d and '||' not in ln:
        cur_d = d.group(1)
        continue
    t = TITLE.match(ln)
    if t and '||' in ln:
        title = (t.group(2) or t.group(1) or t.group(3)).strip()
        page = t.group(1).strip() if t.group(1) else None
        parts = ln.split('||')
        out.append({
            'date': '%s %s, 2026' % (cur_m, cur_d),
            'title': title,
            'page': page,
            'studio': clean(parts[1]) if len(parts) > 1 else '',
            'crew': clean(parts[2]) if len(parts) > 2 else '',
        })
json.dump(out, open('.research/films.json','w',encoding='utf-8'), indent=1)
print(len(out), 'films;', sum(1 for f in out if 'None' in f['date']), 'missing a day')
print(collections.Counter(f['date'].split()[0] for f in out))

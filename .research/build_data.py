# -*- coding: utf-8 -*-
"""Emit data/films.json — the 43-film reference list the site renders from.

This is the only generated file in the repo. data/watched.json is yours to
edit (by hand, or through the site), and index.html is a plain static app.
"""
import json, io, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

movies = json.load(open('.research/movies.json', encoding='utf-8'))
STATUS_LABEL = {'out': 'Released', 'upcoming': 'Coming soon', 'unknown': 'Unidentified'}


def norm(s):
    return ''.join(ch for ch in s.lower() if ch.isalnum())


def slug(s):
    out = ''.join(ch if ch.isalnum() else '-' for ch in s.lower())
    while '--' in out:
        out = out.replace('--', '-')
    return out.strip('-')


def split_credits(c):
    if not c:
        return '', '', ''
    parts = [p.strip() for p in c.split(';')]
    crew = [p for p in parts if '(' in p]
    cast = [p for p in parts if '(' not in p]
    names = [n.strip() for n in ', '.join(cast).split(',') if n.strip()]
    shown = ', '.join(names[:5]) + (f' + {len(names) - 5} more' if len(names) > 5 else '')
    director = re.sub(r'\s*\([^)]*\)\s*$', '', parts[0]).strip() if parts else ''
    return '; '.join(crew), shown, director


films = []
for m in movies:
    crew, cast, director = split_credits(m['credits'])
    note = m['card'] if norm(m['card']) != norm(m['title']) else ''
    day = m['day'] if 'day' in m else (m['date'].split(' ')[1].rstrip(',') if m['date'] else None)
    films.append({
        'id': slug(m['title']),
        'title': m['title'],
        'month': m['date'].split(' ')[0] if m['date'] else None,
        'day': day,
        'release': m['date'],
        'status': m['status'],
        'statusLabel': STATUS_LABEL[m['status']],
        'director': director,
        'crew': crew,
        'cast': cast,
        'desc': m['desc'],
        'url': m['url'],
        'list': m['list'],
        'note': note,
        'search': ' '.join([m['title'], m['desc'], crew, cast, note]).lower(),
    })

# Films added through the site live only in data/films.json, so carry them
# across a rebuild instead of dropping them.
try:
    existing = json.load(open('data/films.json', encoding='utf-8'))
except (OSError, ValueError):
    existing = []
kept = [f for f in existing if f.get('addedHere')]
if kept:
    have = {f['id'] for f in films}
    for f in kept:
        if f['id'] not in have:
            films.append(f)
    print('carried over %d hand-added film(s): %s'
          % (len(kept), ', '.join(f['title'] for f in kept)))

MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
films.sort(key=lambda f: (MONTHS.index(f['month']) if f['month'] else 99,
                          int(f['day']) if f['day'] else 99))

ids = [f['id'] for f in films]
dupes = sorted({i for i in ids if ids.count(i) > 1})
if dupes:
    raise SystemExit('duplicate film ids: %s' % dupes)

# Cross-check that every filmId in watched.json still resolves.
watched = json.load(open('data/watched.json', encoding='utf-8'))
known = set(ids)
for w in watched['films']:
    if w.get('filmId') and w['filmId'] not in known:
        raise SystemExit('watched.json references unknown filmId %r (%s)'
                         % (w['filmId'], w['title']))

# Byte-for-byte the same shape the site writes (JSON.stringify(FILMS, null, 1)
# plus a trailing newline), so a CI rebuild and a save from the page do not
# produce spurious whitespace diffs against each other.
with open('data/films.json', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(json.dumps(films, ensure_ascii=False, indent=1) + '\n')
print('wrote data/films.json —', len(films), 'films')
print('watched.json cross-check: %d entries, %d linked to the board'
      % (len(watched['films']), sum(1 for w in watched['films'] if w.get('filmId'))))

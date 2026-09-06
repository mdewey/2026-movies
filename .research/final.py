# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

films = {f['title']: f for f in json.load(open('.research/films.json', encoding='utf-8'))}
full  = json.load(open('.research/full.json', encoding='utf-8'))
mp    = json.load(open('.research/map.json', encoding='utf-8'))
cards = json.load(open('.research/trello-export.json', encoding='utf-8'))['cards']
LISTS = {'6a8c807ae87c471dce5a749a': '2026 movies', '6a8c9eb9ef8d9385ccd44e21': 'Not out yet'}

# Release dates / credits for the five films absent from the US-releases table.
OFF = {
 'The AI Doc: Or How I Became an Apocaloptimist':
   ('March 27, 2026', 'Daniel Roher, Charlie Tyrell (directors)'),
 'Bucking Fastard':
   ('September 3, 2026', 'Werner Herzog (director/screenplay); Kate Mara, Rooney Mara, Orlando Bloom, Domhnall Gleeson'),
 'Everyone Is Lying to You for Money':
   ('April 17, 2026', 'Ben McKenzie (director/screenplay)'),
 'Rich Flu':
   ('May 29, 2026', 'Galder Gaztelu-Urrutia (director/screenplay); Mary Elizabeth Winstead, Rafe Spall, Timothy Spall, Lorraine Bracco'),
 'Hope':
   ('September 9, 2026', 'Na Hong-jin (director/screenplay); Hwang Jung-min, Zo In-sung, Hoyeon, Alicia Vikander, Michael Fassbender'),
}

D = {
 '28 Years Later: The Bone Temple': "Nia DaCosta directs Alex Garland's script for the second chapter of the new trilogy: Spike is taken in by the cult of “Sir Lord” Jimmy Crystal while Dr. Kelson forms an unexpected bond with an Alpha Infected.",
 'The AI Doc: Or How I Became an Apocaloptimist': "Daniel Roher, about to become a father, interviews AI's doomsayers, its evangelists and the executives racing to build it, trying to work out what world his child will inherit.",
 'Avatar Aang: The Last Airbender': "Animated continuation of the Avatar saga, in which Aang and his friends find Tagah, a surviving airbender, and go looking for a staff that could bring the Air Nomads back.",
 'Backrooms': "Kane Parsons's feature debut, expanded from his viral web series: in 1990 a researcher is separated from his team and lost inside the Backrooms, an endless extradimensional maze.",
 'Bucking Fastard': "Werner Herzog's fable, loosely based on the Yorkshire twins Freda and Greta Chaplin. Kate and Rooney Mara play sisters so inseparable they speak in unison, digging a tunnel through a mountain toward an imagined land where love is possible.",
 'The Dog Stars': "Ridley Scott's adaptation of Peter Heller's novel. Years after a flu pandemic emptied the world, a pilot living on a Colorado airfield with his dog and a volatile survivalist follows a radio signal into the unknown.",
 'Buddy': "Children trapped inside a surreal 1990s kids' TV show try to escape their malevolent unicorn host. Cristin Milioti stars; Keegan-Michael Key voices Buddy.",
 'The Drama': "Zendaya and Robert Pattinson play a happily engaged couple whose relationship is upended by an unexpected revelation in the week before their wedding.",
 'Everyone Is Lying to You for Money': "Ben McKenzie's documentary takedown of the cryptocurrency industry — the hype, the celebrity endorsements and the fraud that powered its rise.",
 'Hoppers': "Pixar's sci-fi comedy about an animal-loving college student who transfers her consciousness into a robotic beaver to talk to animals and save their habitat — accidentally starting an uprising.",
 'Rich Flu': "A disease starts killing the world's wealthiest — billionaires first, then millionaires, then anyone with assets — and the rich scramble to give their fortunes away.",
 'I Love Boosters': "Boots Riley's absurdist crime comedy about the “Velvet Gang,” a Bay Area crew who shoplift designer clothes and resell them. With Keke Palmer and Naomi Ackie.",
 'I Want Your Sex': "Gregg Araki's erotic thriller, in which a young man working for a provocative contemporary artist (Olivia Wilde) is pulled deep into her orbit.",
 'It Ends': "Four recent graduates on a late-night drive turn onto a two-lane highway that simply never ends.",
 'Jackass: Best and Last': "A final Jackass outing, mixing new stunts with classic footage and on-set interviews with the cast.",
 "Lee Cronin's The Mummy": "A family is reunited with their long-missing, partially mummified daughter, and slowly realizes she is possessed.",
 'Mother Mary': "David Lowery's drama with Anne Hathaway as a pop star whose reunion with her former costume designer (Michaela Coel) forces her to face her past.",
 'Obsession': "A music-store clerk buys a supernatural toy and wishes for his friend to fall in love with him. She does — catastrophically.",
 'Project Hail Mary': "Ryan Gosling wakes aboard an interstellar spacecraft with no memory of how he got there, and gradually realizes he is humanity's last hope. From Lord & Miller, adapting Andy Weir.",
 'Ready or Not 2: Here I Come': "Grace survived the Le Domas family's deadly wedding-night ritual, and finds that surviving was only the beginning. Samara Weaving returns, with Kathryn Newton and Sarah Michelle Gellar.",
 'The Death of Robin Hood': "Hugh Jackman as an aged, wounded Robin Hood in self-imposed exile, tormented by the killings of his outlaw years. Jodie Comer co-stars.",
 'Send Help': "Sam Raimi's survival horror: a passed-over corporate strategist and the boss who humiliated her wash up together on a deserted island. With Rachel McAdams and Dylan O'Brien.",
 'Teenage Sex and Death at Camp Miasma': "Jane Schoenbrun's meta-slasher, in which a filmmaker hired to reboot a horror franchise becomes fixated on casting the original final girl. Hannah Einbinder and Gillian Anderson star.",
 'The End of Oak Street': "David Robert Mitchell's survival film: in 1982 an entire Michigan suburb is transported into the age of dinosaurs. With Anne Hathaway and Ewan McGregor.",
 'The Invite': "Olivia Wilde's sex comedy about a San Francisco couple whose evening gets complicated when the wife invites their upstairs neighbors over. With Seth Rogen.",
 'The Yeti': "When an oil tycoon and an adventurer vanish in northern Alaska, their children go looking for them — and something prehistoric starts stalking the search party.",
 'Tony': "Dominic Sessa plays a 19-year-old Anthony Bourdain who, in the summer of 1975, stumbles into a Provincetown restaurant kitchen and finds the life that will define him. With Antonio Banderas.",
 'Hope': "Na Hong-jin's epic creature thriller. In a village near the DMZ, a police chief and a band of hunters track a mysterious beast, and misjudgment spirals into tragedy.",
 'The Musical': "A frustrated playwright and middle-school theater teacher mounts a spiteful production after his ex starts dating the school principal.",
 'Primetime': "Robert Pattinson plays Chris Hansen at the height of To Catch a Predator, in Lance Oppenheim's first narrative feature.",
 'The Social Reckoning': "Aaron Sorkin's companion piece to The Social Network, dramatizing the 2021 Facebook leak by whistleblower Frances Haugen and reporter Jeff Horwitz. With Mikey Madison and Jeremy Strong.",
 'Clayface': "DC body horror from a Mike Flanagan script: disfigured movie star Matt Hagen volunteers for a treatment to restore his face, with monstrous side effects.",
 'Wild Horse Nine': "Martin McDonagh sends two CIA officers to Easter Island on the eve of the 1973 Chilean coup. With Sam Rockwell, John Malkovich and Steve Buscemi.",
 'How to Rob a Bank': "A crew of bank robbers documents its heists on social media, and the police close in. David Leitch directs Nicholas Hoult and Zoë Kravitz.",
 'Paper Tiger': "James Gray's crime drama about two brothers chasing a business opportunity in 1980s Queens who get tangled up with the Russian mafia. With Adam Driver and Scarlett Johansson.",
 'The Further Mis-Adventures of Cliff Booth': "David Fincher directs Quentin Tarantino's script. It is 1977, eight years after Once Upon a Time in Hollywood, and Cliff Booth now works as a studio fixer. Brad Pitt returns.",
 'Violent Night 2': "Stripped of his magic and stuck on the naughty list, Santa Claus takes on a gangster terrorizing a small town. David Harbour returns.",
 'Avengers: Doomsday': "Heroes from three universes — the Avengers, the Wakandans and the New Avengers, plus the Fantastic Four — converge against Doctor Doom.",
 'Ray Gunn': "Brad Bird's animated noir about the last human private detective in a future city shared by humans and aliens.",
 'Digger': "Alejandro G. Iñárritu's satire with Tom Cruise as the most powerful man in the world, racing to prove he is humanity's savior before the disaster he unleashed destroys everything.",
 'Wildwood': "Laika's stop-motion adaptation of Colin Meloy's novel: two Portland kids cross into a hidden magical forest to rescue a kidnapped baby brother.",
 'Wicker': "In a rigidly patriarchal medieval town, an ostracized fisherwoman sarcastically commissions a husband woven from wicker — and the weaver brings him to life. With Olivia Colman.",
}

MONTHS = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']

def key(d):
    m, rest = d.split(' ', 1)
    return (MONTHS.index(m) + 1, int(rest.split(',')[0]))

TODAY = (9, 5)
out = []
for c in cards:
    if c['idList'] not in LISTS:
        continue
    name = c['name'].strip()
    canon = mp.get(name)
    rec = {'card': name, 'list': LISTS[c['idList']], 'title': canon or name}
    if name == 'The End (short film)':
        # Identified by the user from IMDb (tt42004481); confirmed against the Cannes
        # programme. Festival premiere, so it has a month but no single release day.
        rec.update({
            'date': 'May 2026', 'day': None, 'sortkey': (5, 99), 'status': 'out',
            'credits': 'Niki Lindroth von Bahr (director/screenplay); Jen Silverman (screenplay); '
                       'Alexander Skarsgård, Anna Mouglalis, Noomi Rapace, Denis Lavant',
            'desc': "Niki Lindroth von Bahr's 15-minute stop-motion film — a deadpan tale of death "
                    "and existence set in a vast international airport, where pig employees watch "
                    "reality TV and a dolphin works the smoothie bar. Premiered in the short film "
                    "competition at Cannes.",
            'url': 'https://www.festival-cannes.com/en/f/the-end/'})
    elif canon is None:
        rec.update({'date': None, 'sortkey': (99, 99), 'status': 'unknown', 'credits': '',
                    'desc': "Could not be identified with confidence — several unrelated 2026 "
                            "short films share this title.",
                    'url': None})
    else:
        if canon in films:
            f = films[canon]
            date, credits = f['date'], f['crew']
            page = f['page'] or canon
        else:
            date, credits = OFF[canon]
            page = full[canon]['page']
        k = key(date)
        rec.update({'date': date, 'sortkey': k,
                    'status': 'out' if k <= TODAY else 'upcoming',
                    'credits': credits, 'desc': D[canon],
                    'url': 'https://en.wikipedia.org/wiki/' + page.replace(' ', '_')})
    out.append(rec)

out.sort(key=lambda r: r['sortkey'])
json.dump(out, open('.research/movies.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(out), 'movies |',
      sum(1 for r in out if r['status'] == 'out'), 'out,',
      sum(1 for r in out if r['status'] == 'upcoming'), 'upcoming,',
      sum(1 for r in out if r['status'] == 'unknown'), 'unknown')
print('\nWhere the Trello list disagrees with the actual release status:')
for r in out:
    exp = 'out' if r['list'] == '2026 movies' else 'upcoming'
    if r['status'] not in (exp, 'unknown'):
        print('  %-34s list=%-12s actual=%-9s %s' % (r['card'], r['list'], r['status'], r['date']))

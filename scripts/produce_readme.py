from pathlib import Path
from tabulate import tabulate
import ruamel_yaml as ryaml
HEADERS=['title_time', 'links', 'organization']
SRC_PATH = Path('some-syllabi.yaml')
DEST_PATH = Path('README.md')
DEST_START_STR = '<!--tablehere-->'

data = ryaml.load(SRC_PATH.open())
for d in data:
    d['title_time'] = "{0} <br> {1}".format(d['title'], d['time_period']) if d.get('time_period') else d['title']
    if d.get('homepage') == d.get('syllabus'):
        d['links'] = "[Homepage/Syllabus]({0})".format(d['homepage'])
    else:
        d['links'] = '/'.join(["[{0}]({1})".format(n.capitalize(), d[n]) for n in ('homepage', 'syllabus') if d.get(n)])
    d['organization'] = d.get('org')

tbl = tabulate([[d[h] for h in HEADERS] for d in data], headers=HEADERS, tablefmt="pipe")


readmetxt = DEST_PATH.read_text().splitlines()

try:
    with DEST_PATH.open('w') as f:
        for line in readmetxt:
            if line != DEST_START_STR:
                print(line)
                f.write(line + "\n")
            else:
                print(DEST_START_STR)
                f.write(DEST_START_STR + '\n\n')
                print(tbl)
                f.write(tbl)
                break
# worst error-handling code ever:
except Exception as err:
    print("Aborting...Error:", err)
    lines = '\n'.join(readmetxt)
    print(lines)
    with DEST_PATH.open('w') as f:
        f.writelines(lines)
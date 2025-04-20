import os
import re
from collections import defaultdict

README_PATH = 'README.md'
MD_DIR = '.'
START_MARK = '<!-- START:OFFRES_VILLE_STACK -->'
END_MARK = '<!-- END:OFFRES_VILLE_STACK -->'

def extract_field(md, field):
    match = re.search(rf'##\s*{re.escape(field)}\s*\n([^#\n]*)', md, re.IGNORECASE)
    return match.group(1).strip() if match else 'Autre'

offres = [f for f in os.listdir(MD_DIR) if f.endswith('.md') and f != 'README.md']
offres_par_ville_stack = defaultdict(lambda: defaultdict(list))
for file in offres:
    with open(os.path.join(MD_DIR, file), encoding='utf-8') as f:
        md = f.read()
        ville = extract_field(md, 'Localisation')
        stack_principale = extract_field(md, 'Stack principale')
        offres_par_ville_stack[ville][stack_principale].append(file)

section = '# Offres par Ville (mise à jour automatique)\n\n'
for ville in sorted(offres_par_ville_stack):
    section += f'\n## {ville}\n'
    for stack in sorted(offres_par_ville_stack[ville]):
        section += f'**Stack principale : {stack}**\n'
        for file in offres_par_ville_stack[ville][stack]:
            section += f'- [{os.path.splitext(file)[0]}](../blob/main/{file})\n'
        section += '\n'
    section += '\n'

with open(WIKI_PATH, 'w', encoding='utf-8') as f:
    f.write(section)

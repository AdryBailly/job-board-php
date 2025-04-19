import os
import re
from collections import defaultdict

README_PATH = 'README.md'
MD_DIR = '.'

def extract_field(md, field):
    # Recherche insensible à la casse et aux espaces
    match = re.search(rf'##\s*{re.escape(field)}\s*\n([^#\n]*)', md, re.IGNORECASE)
    return match.group(1).strip() if match else 'Autre'

with open(README_PATH, encoding='utf-8') as f:
    content = f.read()

start = content.find('## Les offres classées par ville.')
if start == -1:
    start = len(content)
end = content.find('##', start+1)
if end == -1:
    end = len(content)

offres = [f for f in os.listdir(MD_DIR) if f.endswith('.md') and f != 'README.md']
offres_par_ville_stack = defaultdict(lambda: defaultdict(list))
for file in offres:
    with open(os.path.join(MD_DIR, file), encoding='utf-8') as f:
        md = f.read()
        ville = extract_field(md, 'Localisation')
        stack_principale = extract_field(md, 'Stack principale')
        offres_par_ville_stack[ville][stack_principale].append(file)

section = '## Les offres classées par ville.\n\nFull remote = 🏠\n\n'
for ville in sorted(offres_par_ville_stack):
    section += f'### {ville}\n'
    for stack in sorted(offres_par_ville_stack[ville]):
        section += f'**Stack principale : {stack}**\n'
        for file in offres_par_ville_stack[ville][stack]:
            section += f'- [{os.path.splitext(file)[0]}]({file})\n'
        section += '\n'
    section += '\n'

new_content = content[:start] + section + content[end:]
with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

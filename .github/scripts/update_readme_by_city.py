import os
import re
from collections import defaultdict

README_PATH = 'README.md'
MD_DIR = '.'

# Lire le README existant
with open(README_PATH, encoding='utf-8') as f:
    content = f.read()

# Début/fin de la section à remplacer
start = content.find('## Les offres classées par ville.')
if start == -1:
    start = len(content)
end = content.find('##', start+1)
if end == -1:
    end = len(content)

# Lister les fichiers .md (hors README)
offres = [f for f in os.listdir(MD_DIR) if f.endswith('.md') and f != 'README.md']
offres_par_ville = defaultdict(list)
for file in offres:
    with open(os.path.join(MD_DIR, file), encoding='utf-8') as f:
        md = f.read()
        match = re.search(r'## Localisation\s*\n([\w\s-]+)', md)
        ville = match.group(1).strip() if match else 'Autre'
        offres_par_ville[ville].append(file)

# Générer la section
section = '## Les offres classées par ville.\n\nFull remote = 🏠\n\n'
for ville in sorted(offres_par_ville):
    section += f'### {ville}\n'
    for file in offres_par_ville[ville]:
        section += f'- [{os.path.splitext(file)[0]}]({file})\n'
    section += '\n'

# Remplacer ou ajouter la section
new_content = content[:start] + section + content[end:]
with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

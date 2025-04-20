
## Les offres classées par ville. (Mise à jour automatique via scripts & workflow)

for ville in sorted(offres_par_ville_stack):
    section += f'\n### {ville}\n'
    for stack in sorted(offres_par_ville_stack[ville]):
        section += f'**Stack principale : {stack}**\n'
        for file in offres_par_ville_stack[ville][stack]:
            section += f'- [{os.path.splitext(file)[0]}]({file})\n'
        section += '\n'
    section += '\n'

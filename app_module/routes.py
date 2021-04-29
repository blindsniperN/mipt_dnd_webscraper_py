from app_module import app
from flask import render_template, request
from webscraper import *
from helping_functions import *
from random import randint, choice


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/spells/', methods=['post', 'get'])
def spells():
    if request.method == 'POST':
        spellname = request.form.get('name')
        f = open('app_module/text_databases/spells_res.txt', "r")
        contents = f.read().splitlines()
        f.close()
        f = open('app_module/text_databases/spells_not_found.txt', "r")
        not_found = set(f.read().splitlines())
        f.close()
        if spellname in contents and spellname not in not_found:
            r = Retriever()
            search_eb = r.get_result_obj(spellname)
            p = Parser(search_eb)
            p.gather_attributes()
            return render_template('card_template_test.html', spell=spellname, ct=p.details['Casting Time'],
                                   rg=p.details['Range'], cmp=p.details['Components'], dr=p.details['Duration'])
    return render_template('spell.html')


@app.route('/random_monster/')
def random_monster():
    adjectives = get_list('adjectives')
    nouns = get_list('nouns')
    nm = choice(adjectives) + ' ' + choice(nouns)
    d, s = generate_stats()
    return render_template('monster_card.html', AC=randint(10, 25), name=nm, sz=choice(get_list('sizes')),
                           hp=generate_dice(0, 0, 10, 15, 20), tp=choice(get_list('types')),
                           al=choice(get_list('alignments')), spd=randint(4, 8) * 5, d=d, s=s, pp=10+int(s[4]),
                           im=generate_immunities(), cd=generate_conditions(), lng=generate_languages(),
                           att1=choice(get_list('attacks')), att2=choice(get_list('attacks')),
                           mod1=randint(4, 14), mod2=randint(4, 14), tp1=choice(get_list('damages')),
                           tp2=choice(get_list('damages')), dmg1=generate_dice(randint(0, 1), randint(0, 1), randint(0, 4), randint(1, 5),
                           randint(1, 20)), dmg2=generate_dice(randint(0, 1), randint(0, 1), randint(0, 4), randint(1, 5),
                           randint(1, 20)),
                           txt=generate_text(nm))

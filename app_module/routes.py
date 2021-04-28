from app_module import app
from flask import render_template, request
from webscraper import *


@app.route('/', methods=['post', 'get'])
@app.route('/index/', methods=['post', 'get'])
def index():
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
    return render_template('index.html')

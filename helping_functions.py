from random import randint, choice
from dice_lib import *
import markovify


def get_list(s):
    f = open('app_module/text_databases/monster_gen/' + s + '.txt', "r")
    x = f.read().splitlines()
    f.close()
    return x


def generate_dice(d12, d10, d8, d6, modifier):
    d = DiceRoll('')
    d.add(str(randint(0, d12)) + 'd12')
    d.add(str(randint(0, d10)) + 'd10')
    d.add(str(randint(0, d8)) + 'd8')
    d.add(str(randint(0, d6)) + 'd6')
    d.add(str(randint(1, modifier)))
    return str(round(rolling_dice(d, 'xpv sum'))) + ' (' + d.print() + ')'


def generate_sentence(first_word, text_model):
    return text_model.make_sentence(init_state=tuple(["___BEGIN__"] + [first_word]))


def generate_text(name):
    with open("app_module/text_databases/monster_gen/monsters.txt", encoding='utf-8') as f:
        text = f.read()
    text_model = markovify.Text(text)

    if randint(0, 1):
        word = "It"
        txt = ""
        for i in range(randint(1, 5)):
            txt += generate_sentence(word, text_model) + '\n'
        return name + txt[2:]
    else:
        word = "They"
        txt = ""
        for i in range(randint(1, 5)):
            txt += generate_sentence(word, text_model) + '\n'
        return name + 's' + txt[4:]


def generate_stats():
    d = [0 for i in range(6)]
    s = ['0' for i in range(6)]
    for i in range(6):
        d[i] = randint(1, 20)
        x = round(d[i] / 2) - 5
        s[i] = '+' * (x >= 0) + str(x)
    return d, s


def generate_immunities():
    dmgs = get_list('damages')
    res = set()
    x = randint(0, 1)
    while x:
        x = randint(0, 1)
        res.add(choice(dmgs))
    if len(res) == 0:
        return '-'
    else:
        s = ''
        for el in res:
            s += el + ', '
        return s[:len(s) - 2]


def generate_conditions():
    dmgs = get_list('conditions')
    res = set()
    x = randint(0, 7)
    while x != 0:
        x = randint(0, 7 - round(len(res) / 2))
        res.add(choice(dmgs))
    if len(res) == 0:
        return '-'
    else:
        s = ''
        for el in res:
            s += el + ', '
        return s[:len(s) - 2]


def generate_languages():
    dmgs = get_list('languages')
    res = set()
    x = randint(0, 5)
    while x != 0:
        x = randint(0, 5 - len(res))
        res.add(choice(dmgs))
    if len(res) == 0:
        return '-'
    else:
        s = ''
        for el in res:
            s += el + ', '
        return s[:len(s) - 2]

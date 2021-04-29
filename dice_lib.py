import matplotlib.pyplot as plt
from random import randint

accuracy = 3


def expected_value(x):  # подсчёт мат ожидания
    if x is not None:
        summa = 0
        for i in range(len(x)):
            summa += i * x[i]
        return summa / sum(x)


def turn_to_probability(y, acc):
    if y is not None:
        sm = sum(y)
        x = [round(number / sm, acc) for number in y]
        return x


def plt_probability(y):  # построение графика
    if y is not None:
        plt.bar(range(len(y)), y)
        plt.show()


def geqslant(arr, modif, x):
    if arr is not None:
        if x < modif:
            return 1
        elif x > len(arr) - 1:
            return 0
        else:
            return sum(arr[x:]) / sum(arr)


def leqslant(arr, modif, x):
    if arr is not None:
        if x < modif:
            return 0
        elif x >= len(arr) - 1:
            return 1
        else:
            return sum(arr[:x+1]) / sum(arr)


def eq(arr, modif, x):
    if arr is not None:
        if x < modif or x > len(arr) - 1:
            return 0
        else:
            return arr[x] / sum(arr)


def roll(arr):  # механика броска такая же, как в проекте по тп
    if arr is not None:
        x = randint(1, sum(arr))
        i = 0
        while x > 0:
            x -= arr[i]
            i += 1
        return i - 1


class DiceRoll:
    def __init__(self, s):  # инициализируется через словарь
        self.diceN_ = {}
        self.modifier_ = 0  # модификатор броска
        self.add(s)

    def add(self, s):
        if s != '':
            s += ' + '
            while s != '':
                if (s[:s.find(' ')]).find('d') != -1:
                    amount = int(s[:s.find('d')])
                    s = s[s.find('d') + 1:]
                    cap = int(s[:s.find(' ')])
                    if cap in self.diceN_:
                        self.diceN_[cap] += amount
                    else:
                        self.diceN_[cap] = amount
                elif s != ' ':
                    self.modifier_ += int(s[:s.find(' ')])
                s = s[s.find('+') + 2:]

    def minus(self, s):
        s += ' + '
        while s != '':
            if s[:s.find(' ')].find('d') != -1:
                amount = int(s[:s.find('d')])
                s = s[s.find('d') + 1:]
                cap = int(s[:s.find(' ')])
                s = s[s.find('+') + 2:]
                if cap in self.diceN_:
                    if self.diceN_[cap] <= amount:
                        self.diceN_[cap] = 0
                    else:
                        self.diceN_[cap] -= amount
            elif s != ' ':
                self.modifier_ -= int(s[:s.find(' ')])
            s = s[s.find('+') + 2:]

    def print(self):
        s = ''
        for el in sorted(self.diceN_.items()):
            if el[1] != 0:
                s += str(el[1]) + 'd' + str(el[0]) + ' + '
        if self.modifier_ != 0:
            s += str(self.modifier_)
        else:
            s = s[:len(s)-2]
        if s != '':
            return s
        else:
            return '0 dice added'

    def return_dict(self):
        return self.diceN_

    def max_res(self):
        sum_d = 0
        for el in self.diceN_.items():
            sum_d += el[1]*el[0]
        return sum_d + self.modifier_

    def arr_sum(self):  # подсчёт массива всех возможных величин
        x = [0] * (self.max_res() + 1)
        x[self.modifier_] = 1
        for el in self.diceN_.items():
            for i in range(el[1]):
                cpy = [0] * (self.max_res() + 1)
                for j in range(len(x) - el[0]):
                    for k in range(1, el[0] + 1):
                        cpy[j + k] += x[j]
                x = cpy
        return x

    def adv(self):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
            for el in self.diceN_.items():
                x = [0] * (el[0] + self.modifier_ + 1)
                x[self.modifier_] = 1
                for i in range(el[1]):
                    cpy = [0] * (el[0] + self.modifier_ + 1)
                    for j in range(el[0] + self.modifier_ + 1):
                        for k in range(self.modifier_ + 1, el[0] + self.modifier_ + 1):
                            cpy[max(j, k)] += x[j]
                    x = cpy
                return x

    def dis(self):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
            for el in self.diceN_.items():
                x = [0] * (el[0] + self.modifier_ + 1)
                x[el[0] + self.modifier_] = 1
                for i in range(el[1]):
                    cpy = [0] * (el[0] + self.modifier_ + 1)
                    for j in range(el[0] + self.modifier_ + 1):
                        for k in range(self.modifier_ + 1, el[0] + self.modifier_ + 1):
                            cpy[min(j, k)] += x[j]
                    x = cpy
                return x

    def arr_sum_reroll_less(self, least_reroll):  # подсчёт массива всех возможных величин
        x = [0] * (self.max_res() + 1)
        x[self.modifier_] = 1
        for el in self.diceN_.items():
            for i in range(el[1]):
                cpy = [0] * (self.max_res() + 1)
                for j in range(len(x) - el[0]):
                    for k in range(1, el[0] + 1):
                        if k > least_reroll:
                            cpy[j + k] += x[j] * el[0]
                        else:
                            for reroll in range(1, el[0] + 1):
                                cpy[j + reroll] += x[j]
                x = cpy
        return x

    def bmb(self, depth):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
            for el in self.diceN_.items():
                if el[1] != 1:
                    print('Cannot calculate that')
                    return None
                else:
                    arr = [0] * (self.modifier_ + depth * el[0] + 1)
                    for i in range(depth):
                        for j in range(1, el[0]):
                            arr[self.modifier_ + i * el[0] + j] = el[0] ** (depth - i - 1)
                    arr[len(arr) - 1] = 1
                    return arr


def prob_preparation(d, s):  # предобработка кубов для команд r>=, r==, r<=
    y = 0
    arr = []
    if s[4:7] == 'sum':
        arr = d.arr_sum()
        y = int(s[8:])
    elif s[4:7] == 'adv':
        arr = d.adv()
        y = int(s[8:])
    elif s[4:7] == 'dis':
        arr = d.dis()
        y = int(s[8:])
    elif s[4:7] == 'rrl':
        x, y = map(int, s[8:].split())
        arr = d.arr_sum_reroll_less(x)
    elif s[4:7] == 'bmb':
        x, y = map(int, s[8:].split())
        arr = d.bmb(x)
    return [arr, y]


def preparation(d, s):  # предобработка кубов для прочих команд
    arr = []
    if s[4:7] == 'sum':
        arr = d.arr_sum()
    elif s[4:7] == 'adv':
        arr = d.adv()
    elif s[4:7] == 'dis':
        arr = d.dis()
    elif s[4:7] == 'rrl':
        x = int(s[8:])
        arr = d.arr_sum_reroll_less(x)
    elif s[4:7] == 'bmb':
        arr = d.bmb(int(s[8:]))
    return arr


def rolling_dice(d, s):
    cmd = s[:3]
    if cmd == 'add':  # добавить кубы
        d.add(s[4:])

    elif cmd == 'del':  # удалить кубы
        d.minus(s[4:])

    elif cmd == 'max':
        return 'Max sum on dice: ' + str(d.max_res())

    elif cmd == 'arr':  # массив кубов
        return preparation(d, s)

    elif cmd == 'r>=':
        arr, y = prob_preparation(d, s)
        res = geqslant(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r<=':
        arr, y = prob_preparation(d, s)
        res = leqslant(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r==':
        arr, y = prob_preparation(d, s)
        res = eq(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'xpv':  # мат ожидание
        res = expected_value(preparation(d, s))
        if res is not None:
            return round(res, accuracy)

    elif cmd == 'prb':
        return turn_to_probability(preparation(d, s), accuracy)

    elif cmd == 'plt':
        plt_probability(turn_to_probability(preparation(d, s), accuracy))

    elif cmd == 'rll':
        return roll(preparation(d, s))

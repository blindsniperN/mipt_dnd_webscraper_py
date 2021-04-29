from webscraper import *

if __name__ == '__main__':
    '''
    r = Retriever()
    search_eb = r.get_result_obj("Animal Friendship")
    p = Parser(search_eb)
    p.gather_attributes()
    print(p.details['title'])
    print(p.details['Casting Time'])
    print(p.details['Range'])
    print(p.details['Components'])
    print(p.details['Duration'])
    print(p.details['Classes'])
    '''
    '''
    f = open('spells_res.txt', "r")
    contents = f.read().splitlines()
    f.close()
    f = open('spells_not_found.txt', "r")
    not_found = set(f.read().splitlines())
    f.close()
    f = open('markov_spell_material.txt', "w")
    for i in contents:
        if i not in not_found:
            r = Retriever()
            search_eb = r.get_result_obj(i)
            p = Parser(search_eb)
            p.gather_attributes()
            try:
                f.write(p.details['Material'])
                f.write('.\n')
            except:
                print(i)
    print('Finita La Comedia')
    f.close()
    '''
    r = Retriever()
    search_eb = r.get_result_obj("Acid Arrow")
    p = Parser(search_eb)
    p.gather_attributes()
    print('Finita La Comedia')
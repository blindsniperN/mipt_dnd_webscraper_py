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
    f = open('spells_res.txt', "r")
    contents = f.read().splitlines()
    f.close()
    for i in contents:
        r = Retriever()
        search_eb = r.get_result_obj(i)
        p = Parser(search_eb)
        try:
            p.gather_attributes()
        except:
            print(i)
    print('Finita La Comedia')

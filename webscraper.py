import requests
import urllib.parse
from bs4 import BeautifulSoup


class HyperLink:  # гиперссылка
    def __init__(self, text, link):
        self.text = text
        self.link = link


class Retriever:  # вытаскиваем данные
    def __init__(self):
        self.base_url = 'https://roll20.net'
        self.list_search_url = self.base_url + \
            '/compendium/compendium/globalsearch/dnd5e?terms='
        self.full_search_url = self.base_url + \
            '/compendium/dnd5e/searchbook/?terms='

    def get_list_results(self, search_term):
        url = self.list_search_url + urllib.parse.quote(search_term)
        return [result['value'] for result in requests.get(url).json()]

    def get_result_obj(self, search_term):
        url = self.full_search_url + urllib.parse.quote(search_term)
        response = requests.get(url)
        if not response.status_code == 200:
            raise Exception('(Expected 200 response status code, received '
                            f'{response.status_code} instead.)')
        if response.url != url:  # Если мы получили всё в одной ссылке
            # print(f'(Redirected to {response.url})')
            return response
        else:  # Если выводит список
            return self.get_result_links(response, search_term)

    def get_result_links(self, response, search_term):
        # Find all <li> tags in the body of the response and wrap in list()
        list_items = list(BeautifulSoup(response.content,
                                        features="html.parser").find_all('li'))
        response_links = []
        for li in list_items:
            if self.has_uri(li):  # List item contains a URI
                text = li.contents[1].get_text()
                uri = li.a.get('href')
                # If one of the links matches the search term, return it
                if text.lower() == search_term.lower():
                    return requests.get(li.url)
                # Otherwise, add the resource to a list to return
                response_links.append(HyperLink(text=text, link=uri))
        print(f'(Unable to find an exact match for {search_term}.)')
        return response_links

    @staticmethod
    def has_uri(tag):
        return 'href="/' in tag.decode_contents()


class Parser: # парсим результаты
    def __init__(self, response_obj):
        self.response_obj = response_obj
        self.soup = BeautifulSoup(response_obj.content, features="html.parser")
        self.details = {'title': self.soup.title.string}

    def add_attribute(self, key, value):
        self.details[key] = value

    def gather_attributes(self):
        attribute_soup = self.soup.find(id='pageAttrs')
        all_keys = attribute_soup.find_all('div', class_='col-md-3 attrName')
        all_values = attribute_soup.find_all('div',  class_='value')

        for i in range(len(all_keys)):
            self.add_attribute(all_keys[i].string, all_values[i].string)

    def gather_pagecontent(self):
        #  Проверить как подходит для персонажей/монстров
        pagecontent = self.soup.find(id='pagecontent').text
        self.add_attribute('description', pagecontent)
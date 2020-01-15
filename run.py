import requests
from parsel import Selector


URL = 'https://en.wikipedia.org/wiki/List_of_alternative_country_names'


def get_page_content(url=URL):

    return requests.get(url).text


def extract(html):

    data = {}

    sel = Selector(text=html)

    for table_i in range(7,50,2):
        for tr_i in range(2, 30):
            common_name  = get_common_name_in_description(table_i, tr_i, sel)
            if common_name:
                data[common_name] = get_other_names(table_i, tr_i, sel)
            else:
                continue
    return data


def get_common_name_in_description(table_index, tr_index, sel):

    pattern = '#mw-content-text > div > table:nth-child({}) > tbody > tr:nth-child({}) > td:nth-child(1) > a::text'

    return sel.css(
            pattern.format(table_index, tr_index)
    ).get()


def get_other_names(table_index,tr_index, sel):

    pattern1 = '#mw-content-text > div > table:nth-child({}) > tbody > tr:nth-child({}) > td:nth-child(2) > b::text'
    pattern2 = '#mw-content-text > div > table:nth-child({}) > tbody > tr:nth-child({}) > td:nth-child(2) > b > a::text'

    return sel.css(
            pattern1.format(table_index, tr_index)
    ).getall() + sel.css(
            pattern2.format(table_index, tr_index)
    ).getall()


if __name__ == '__main__':

    html = get_page_content()
    data = extract(html)
    for i in data:
        print(','.join([i, ] + data[i]))

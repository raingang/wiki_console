from bs4 import BeautifulSoup
import requests


search_result_page = ''
query = ''


def get_html(url):
    r = requests.get(url)
    return r.text


def get_search_results(html, number_of_results=10):
    '''
    Получает страницу с результатами запроса, возвращает массив словарей
     с полями: название, ссылка, описание
    '''
    search_results = []
    soup = BeautifulSoup(html, 'lxml')
    search_result_block = soup.find('ul', class_='mw-search-results')
    try:
        search_results_list = search_result_block.find_all('li')
        for item in search_results_list:
            title = item.find(
                'div', class_='mw-search-result-heading').find('a')
            href = title.get('href')
            desc = item.find('div', class_='searchresult')
            search_results.append(
                {'title': title.text.strip(), 'href': href, 'desc': desc.text.strip()})
    except AttributeError:
        print('По вашему запросу нет результатов')
    return search_results


def view_search_results(search_results, results_length=10):
    '''
    Выводит результаты поиска, по умолчанию 10, пользователь выбирает нужную позицию
    '''
    search_results = search_results[0: results_length]
    for i in range(0, results_length):
        print('[{}] : '.format(i) + search_results[i]['title'] + '\n')
        print(search_results[i]['desc'] + '\n')

    position = get_integer('Please, select the desired item:', default = 0, minimum = 0, maximum = results_length -1)
    return position

def get_integer(message, name="integer", default=None, minimum=0,
                maximum=1000, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{0} must be between {1} and {2} "
                        "inclusive{3}".format(name, minimum, maximum,
                        (" (or 0)" if allow_zero else "")))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))


def get_query_url(query):
    return 'https://en.wikipedia.org/w/index.php?search={0}&fulltext=1'.format((query))

if __name__ == '__main__':
    search_url = get_query_url('rain')
    search_page = get_html(search_url)
    search_results = get_search_results(search_page)
    print(view_search_results(search_results))

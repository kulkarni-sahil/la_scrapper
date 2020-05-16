import requests
import bs4 as bs

__author__ = 'Sahil Kulkarni'

# Global variables
la_url = 'https://linuxacademy.com/blog/announcements/free-courses-at-linux-academy/'


def get_response(url):
    response = requests.get(url)
    if response.ok:
        return response.content
    else:
        raise RuntimeError('Unable to get response from Linux Academy')


def scrap_response(response):
    soup = bs.BeautifulSoup(response, 'lxml')
    links_dict_recommended = dict()
    links_dict_maybe_random = dict()
    for link in soup.find_all('a', attrs={'class': None, 'id': None}):
        try:
            bold_element = link.find('b')
            b_text = bold_element.text
            links_dict_recommended[link.text] = link['href']
        except:
            links_dict_maybe_random[link.text] = link['href']

    links = list()
    links.append(links_dict_recommended)
    links.append(links_dict_maybe_random)
    return links


def email_course_list(courses_object):
    pass


def main():
    response_data = get_response(la_url)
    courses_list = scrap_response(response_data)
    print(courses_list)


if __name__ == '__main__':
    main()

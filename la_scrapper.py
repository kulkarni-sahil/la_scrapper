import requests
import bs4 as bs
import smtplib

__author__ = 'Sahil Kulkarni and Apoorva'

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


def create_message_for_email(courses_information):
    subject = "Free Courses on Linux Academy for this month!"
    body = """List of courses: \n\n"""

    for title, link in courses_information[0].items():
        body += f"{title} - {link}\n"

    body += "\nThanks"
    msg = f"Subject: {subject}\n\n{body}"
    msg = msg.replace(u'\u2013', u' ')
    return str(msg)


def email_course_list(message):
    """
    This method takes message to be mailed and sends email to the user
    :param message: the message to be sent
    :return: nothing
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    email = "your email"
    send_to = "email_to_send_to"
    password = "your_password"

    server.login(email, password)

    print(message)
    server.sendmail(email, send_to, message)
    print('Email sent!')

    server.quit()


def main():
    response_data = get_response(la_url)
    courses_list = scrap_response(response_data)
    message = create_message_for_email(courses_list)
    email_course_list(message)


if __name__ == '__main__':
    main()


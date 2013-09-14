#!/usr/bin/python

import codecs
import copy
import ConfigParser
import datetime
import getpass
import locale
import os
import requests
import sys

"""
Paste the original document as a post on our wordpress site.

Then use xpath to extract the contents into variables. And jinja to put
it in a template.
"""

from lxml import etree
from jinja2 import Environment
from jinja2 import FileSystemLoader
# from jinja2.ext import loopcontrols
locale.setlocale(locale.LC_TIME, 'nl_NL.UTF8')


# Get config from local file on filesystem.
configpath = os.path.join(os.environ['HOME'], '.fz')
config = ConfigParser.ConfigParser()
config.read(configpath)

WORDPRESS_USERNAME = config.get('user', 'name')
LOGIN_URL = config.get('login', 'url')
REDIRECT_URL = config.get('redirect', 'url')
POST_URL = config.get('post', 'url')


def read_password():
    """
    Input password
    """
    password = getpass.getpass('Password for wordpress:')
    return password


def get_text(post_id):
    """ Login in wordpress and get the post. """
    # Get login page
    response1 = requests.get(
        url=LOGIN_URL,
    )
    # Post to login, remember the cookies.
    response2 = requests.post(
        url=LOGIN_URL,
        data={
            'log': WORDPRESS_USERNAME,
            'pwd': read_password(),
            'wp-submit': 'Log In',
            'testcookie': '1',
            'redirect_to': REDIRECT_URL,
        },
        cookies=response1.cookies,
    )
    # Get the post
    response3 = requests.get(
        url=POST_URL.format(post_id=post_id),
        cookies=response2.cookies,
    )
    return response3.text


def section_from_element(element):
    section = etree.Element('section')
    section.append(copy.deepcopy(element))
    next_element = element.getnext()
    while next_element is not None and next_element.tag != 'h3':
        section.append(copy.deepcopy(next_element))
        next_element = next_element.getnext()
    return section


def styler(style):
    """
    Return a function that updates the style attribute of an element.
    """
    return lambda el: el.attrib.update({'style': style})


def stringify(element):
    return etree.tostring(element, encoding='unicode', pretty_print=True)


def children_to_string(element):
    """
    Return joined string of children of element.
    """
    return ''.join(map(stringify, element.iterchildren()))


def main():
    """ Get the html and convert a little. """

    post_id = sys.argv[1]

    template_path = '/home/arjan/Dropbox/usr/fz/templates'
    environment = Environment(loader=FileSystemLoader(template_path),
                              extensions=['jinja2.ext.loopcontrols'])
    template_mail = environment.get_template('mail2.html')

    text = get_text(post_id)
    xpath = '//section[@itemprop="articleBody"]'
    html = etree.HTML(text).xpath(xpath)[0]

    fzmail = etree.Element('fzmail')
    fzmail.extend(copy.deepcopy(html.getchildren()))
    heading_elements = fzmail.findall('h3')
    sections = map(section_from_element, heading_elements)

    style_h3 = 'font-family:arial;'
    style_h4 = 'font-family:arial;'
    style_p = 'font-family:arial;text-align:justify;'
    style_a = 'color:#0000ff;font-style:italic;text-decoration:underline;'

    # add attributes to images
    for img in fzmail.xpath('//p/img'):
        img.attrib.update(dict(border='1',
                               hspace='10',
                               vspace='0',
                               align='left'))

    map(styler(style_a), fzmail.xpath('//a'))
    map(styler(style_p), fzmail.xpath('//p'))
    map(styler(style_p), fzmail.xpath('//li'))
    map(styler(style_h3), fzmail.xpath('//h3'))
    map(styler(style_h4), fzmail.xpath('//h4'))

    context = {
        'month': datetime.datetime.now().strftime('%B'),
        'year': datetime.datetime.now().strftime('%Y'),
        'fzmail': children_to_string(fzmail)
    }
    fzmail_str = template_mail.render(context)
    fzmail_file = open('fz_mail.html', 'w')
    fzmail_file.write(fzmail_str.encode('utf-8'))
    fzmail_file.close()

    # Fill out the articles
    style_h3_article = 'color:#135cae;'
    for s in sections:
        map(styler(style_h3_article), s.xpath('//h3'))
        # add attributes to images
        for img in s.xpath('//img'):
            img.attrib.update(dict(border='1',
                                   hspace='10',
                                   vspace='0',
                                   align='left'))
        article_str = children_to_string(s)
        article_file = codecs.open(
            ('article_' +
             s.find('h3').text.lower().replace(' ', '_').replace('/', '_') +
             '.html'),
            'w',
            'utf-8',
        )
        article_file.write(article_str)
        article_file.close()

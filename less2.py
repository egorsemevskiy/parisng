import requests
from bs4 import BeautifulSoup
from database.models import (BlogPost, Tag, Writer)
from database.db import (BlogDb)

domen = 'https://geekbrains.ru/'
start_url = '/posts'
db_url = 'sqlite:///blogpost.sqlite'
db = BlogDb(db_url)


def basic_parse(a_href: str):
    response = requests.get(domen + a_href)
    soap = BeautifulSoup(response.text, 'html.parser')
    return soap


def blog_parse(a_href: str):
    if a_href:
        soap = basic_parse(a_href)
        ul = soap.find('ul', attrs={'class': 'gb__pagination'})
        href = ul.find_all('li', attrs={'class': 'page'})[-1].find('a', attrs={'rel': 'next'})['href']
        post = soap.find('div', attrs={'class': 'post-items-wrapper'})
        title = post.find_all('a', attrs={'class': 'post-item__title'})
        for t in title:
            time, tags, author, author_href = post_parse(t['href'])
            print(t.text + ' ' + t['href'] + ' ' + time + ' ' + author.text + ' ' + author_href + str([tag.text for tag in tags]))
            db_insert(t.text, t['href'], time, str(author.text), str(author_href), tags)
        blog_parse(href)


def post_parse(post_href: str):
    soap = basic_parse(post_href)
    article = soap.find('article', attrs={'class': 'blogpost__article-wrapper'})
    time = article.find('time').text
    tags = article.find_all('a', attrs={'class': 'small'})
    author = article.find('div', attrs={'itemprop': 'author'})
    author_href = author.parent['href']
    return time, tags, author, author_href


def db_insert(title, url, time, author_text, author_href, tags):

    if len(db.session.query(Writer).filter_by(url=author_href).all()) > 0:
        writer = db.session.query(Writer).filter_by(url=author_href)[0]
    else:
        writer = Writer(author_text, author_href)

    tags_list = []
    for i in tags:

        if len(db.session.query(Tag).filter_by(name=i.text).all()) > 0:
            tags_list.extend(db.session.query(Tag).filter_by(name=i.text).all())
        else:
            tags_list.extend([Tag(i.text)])

    blog_post = BlogPost(title, url, time, writer, tags_list)
    db.session.add(blog_post)
    final_commit()


def final_commit():
    try:
        db.session.commit()
        db.session.flush()
        print('All Done')
    except Exception as e:
        db.session.rollback()
        print()
        print(f'Ошибка: {e.__class__.__name__}')

    print('*', end='')


blog_parse(start_url)








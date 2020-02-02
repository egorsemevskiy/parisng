# -*- coding: utf-8 -*-
import json
import re
from copy import deepcopy
import scrapy
from scrapy.http import HtmlResponse
from gbparse.items import FollowersItem
from urllib.parse import urlencode


HASHES = {
    'followers': 'c76146de99bb02f6415203be841dd25a',
    'following': 'd04b0a864b4b54837c0d870b0e77e076',
    'media': '58b6785bea111c67129decbe6a448951',
    'media_comments': '97b41c52301f77ce508f55e66d17620e',
    'likes': 'd5d763b1e2acf209d62d22d184488e57',
    'tags': '174a5243287c5f3a7de741089750ab3b',
}


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login = 'amditech'
    insta_pass = '567Instagram'
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'gefestart'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    user_data_hash = 'c9100bf9110dd6361671f113dd02e7d6'

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'password': self.insta_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.userdata_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def userdata_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            "include_reel": True,
            "include_logged_out_extras": False,
            "first": 100,
        }

        url_folowers = f'{self.graphql_url}query_hash={HASHES["followers"]}&{urlencode(variables)}'

        yield response.follow(
            url_folowers,
            callback=self.user_folowers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'varibles': deepcopy(variables)
                       }
        )

    def user_folowers_parse(self, response: HtmlResponse, username, user_id, varibles):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            varibles['after'] = page_info.get('end_cursor')

            url_folowers = f'{self.graphql_url}query_hash={HASHES["followers"]}&{urlencode(varibles)}'
            yield response.follow(
                url_folowers,
                callback=self.user_folowers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(varibles)
                           }
            )

        for follower in j_data.get('data').get('user').get('edge_followed_by').get('edges'):
            item = FollowersItem(user_name=username,
                                 user_id=user_id,
                                 follower_id=follower['node']['id'],
                                 follower_name=follower['node']['username'],
                                 data=follower['node']
                                 )
            yield item

    def user_data(self, response: HtmlResponse, username):
        j_user_data = json.loads(response.text)

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

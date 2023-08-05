#!/usr/bin/python

import httplib2
import datetime 
from xml.dom import minidom
import urllib

class MDelicious:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def posts_all(self, tag=None, start_date=None, end_date=None):
        base_url = 'https://api.del.icio.us/v1/posts/all?'
        params = {}
        if tag: params["tag"] = tag
        if start_date: params["fromdt"] = start_date.strftime("%Y-%m-%dT%H:%M:%SZ") 
        if end_date: params["todt"] = end_date.strftime("%Y-%m-%dT%H:%M:%SZ") 

        url = base_url + urllib.urlencode(params)

        http = httplib2.Http()
        http.add_credentials(self.username, self.password)
        response, content = http.request(url)
        return self.process_response(content)
        
    def process_response(self, content):
        dom = minidom.parseString(content)
        posts = []

        for node in dom.getElementsByTagName('post'):
            posts.append({
                'href': node.getAttribute('href'),
                'hash': node.getAttribute('hash'),
                'description': node.getAttribute('description'),
                'time': datetime.datetime.strptime(
                    node.getAttribute('time'), "%Y-%m-%dT%H:%M:%SZ"),
                'extended': node.getAttribute('extended'),
                'meta': node.getAttribute('meta'),
                'tags':  node.getAttribute('tag').split(" "),
            })
        return posts
       

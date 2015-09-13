#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytumblr
import urllib
import requests
import time

# initialize parameters
client = pytumblr.TumblrRestClient(
    'phitYQG0biHZxl2Nd4BtNztj3xg6CN46iHuoeig7Vq246CTmdv',
    'YevBIBU6b03ydXOUbEbNsqwLnJErJNCIfXbzexuHggWowK0ody',
    'esmgxaW75bXZG4l4nxso8lwNr06zhMmvDR0MXMCyjQSgDtvBEw',
    'OrszMDh4J4qSqbP18e5NPz6xnWwrNNU6Bcs6mRLwoLSkU7O3Rb'
)

token = 'b9ba254626a6de4540e8c3b59aba0ddb5ff87aabb38d98d5c4fb3a1dcac440ae4ea35827db7d91fd8b630'
gid = '62148300'
album = '183278429'


def post_to_vk(token, gid, album, pic):
    # get upload server url
    server_url = 'https://api.vk.com/method/photos.getWallUploadServer?group_id=' + gid + \
                 '&album_id=' + album + \
                 '&access_token=' + token

    r = requests.get(server_url)
    upload_url = r.json()['response']['upload_url']

    # upload image
    file1 = {'file': open(pic, 'rb')}
    p = requests.post(upload_url, files=file1)

    # save image to album
    save_url = 'https://api.vk.com/method/photos.saveWallPhoto?gid=' + gid + \
               '&photo=' + p.json()['photo'] + \
               '&server=' + str(p.json()['server']) + \
               '&hash=' + p.json()['hash'] + \
               '&access_token=' + token

    save_request = requests.get(save_url)

    # post image
    post_url = 'https://api.vk.com/method/wall.post?owner_id=-' + gid + \
               '&from_group=' + '1' + \
               '&attachments=' + save_request.json()['response'][0]['id'] + \
               '&access_token=' + token

    requests.get(post_url)
    return

# do da shit
count = 0
while True:
    delta = len(client.posts('hotpizzanews')['posts']) - count
    if delta > 0:
        for i in range(0, delta):
            pic_url = client.posts('hotpizzanews')['posts'][i]['photos'][0]['original_size']['url']
            filename = pic_url.split('/')[-1]
            urllib.urlretrieve(pic_url, filename)
            post_to_vk(token, gid, album, filename)
        count += delta
    time.sleep(60)

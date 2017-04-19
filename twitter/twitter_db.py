#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import os.path
import logging
import logging.config
import configparser
import datetime
import string
import random
import urllib.parse
import time
from twitter.models import Twitter


def add_data_to_sql(user, twit):
    insert = Twitter(
        twitter_user=user,
        twitter_text=filter_out_data(twit),
        twitter_date=datetime.datetime.now()
    )
    insert.save()


def read_data_from_sql(user):
    arr = Twitter.objects.filter(twitter_user=user)
    return arr


def take_twit_by_id(id):
    twitObj = Twitter.objects.get(id=id)
    return twitObj


def update_data(twi_id, new_twit):
    twitObj = Twitter.objects.filter(id=twi_id).update(twitter_text=new_twit)


def delete_data_from_sql(user, row_id):
    arr = Twitter.objects.filter(
        twitter_user=user,
        id=row_id).delete()


def filter_out_data(twit):    
    twit = "".join([s for s in twit if ord(s) > 31])
    twit = twit[:100]
    twit = re.sub(r'\s+', ' ', twit)
    twit = re.sub('\s+', ' ', twit)
    twit = re.sub('^ ', '', twit)
    twit = re.sub(' $', '', twit)    
    return twit

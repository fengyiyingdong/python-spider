#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time, uuid

from orm import Model, StringField, IntegerField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class Product(Model):
    '''
        create table product (
            id int not null auto_increment,
            name varchar(256) not null,
            low int,
            high int,
            average int,
            tp varchar(128),
            unit varchar(18),
            publish varchar(64),
            PRIMARY KEY (id)
        )
    '''
    __table__ = 'product'

    id = IntegerField(primary_key=True, default=None)
    name = StringField(ddl='varchar(256)')
    low = IntegerField()
    high = IntegerField()
    average = IntegerField()
    tp = StringField(ddl='varchar(128)')
    unit = StringField(ddl='varchar(18)')
    publish = StringField(ddl='varchar(64)')
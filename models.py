#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
Created on 2017/6/23
@author: Bee
'''

from peewee import *
import os, datetime

db_filepath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'secrepo.db')
database = SqliteDatabase(db_filepath)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    id = IntegerField(primary_key=True)
    email = CharField(unique=True)
    password = CharField()
    uuid = UUIDField()
    enable = BooleanField()

class Repo(BaseModel):
    id = IntegerField(primary_key=True)
    added_by = ForeignKeyField(User, related_name='repos')
    add_time = DateField(default=datetime.datetime.now())
    owner = CharField(null=True)
    repositoriy = CharField(null=True)
    language = CharField(null=True)
    display_name = CharField(null=True)
    description = CharField(null=True)
    tags = CharField(null=True)
    category = CharField(null=True)
    img = CharField(null=True)
    review_time = DateField(default=None,null=True)
    is_reviewed = BooleanField(default=False)

class Tag(BaseModel):
    id = IntegerField(primary_key=True)
    tag = CharField()

class Category(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

if __name__ == '__main__':
    database.create_tables([User, Repo, Category], True)
    # init test user
    User.create(**{'email': 'a@qq.com', 'password': 'admin', 'uuid': 'ff63de92-646a-11e7-8c70-9801a7b3cc87',
                 'enable': True})
    # init categories
    Category.create(**{'name': '信息收集'})
    Category.create(**{'name': '渗透测试'})
    Category.create(**{'name': '暴力破解'})
    Category.create(**{'name': '逆向工程'})
    Category.create(**{'name': '社会工程'})
#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
Created on 2017/6/23
@author: Bee
'''

from flask import Flask
from flask import request, jsonify
from models import User, Repo, Category
from playhouse.shortcuts import model_to_dict
from uuid import uuid1 as getuuid
from utils import *


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/register', methods=['POST'])
def user_register():
    output = {'status': 'OK', 'msg': ''}
    email = request.form.get('email')
    password = request.form.get('password')
    uuid = getuuid()

    if User.select().where(User.email==email).exists():
        output['status'] = 'Err'
        output['msg'] = 'User existed.'
        return jsonify(output)
    else:
        output['email'] = email
        output['uuid'] = uuid
        User.create(email=email, password=password, uuid=uuid, enable=True)

    return jsonify(output)

@app.route('/repo/submit', methods=['POST'])
def repo_submit():
    output = {'status': 'OK', 'msg': ''}
    uuid = request.form.get('uuid')
    url = request.form.get('url')
    description = request.form.get('description')
    category = request.form.get('category')
    user = User.select().where(User.uuid==uuid).exists()
    if user:
        user = User.select().where(User.uuid==uuid).get()
        repo = get_owner_and_repo(url)
        if repo:
            if not Repo.select().where(Repo.owner == repo[0], Repo.repositoriy == repo[1]).exists():
                Repo.create(added_by=user.id, owner=repo[0], repositoriy=repo[1], description=description, category=category)
                return jsonify(output)
            else:
                output['status'] = 'Err'
                output['msg'] = 'Repo exists.'
                return jsonify(output)
        else:
            output['status'] = 'Err'
            output['msg'] = 'Not a github repo url.'
            return jsonify(output)
    else:
        output['status'] = 'Err'
        output['msg'] = 'UUID err.'
        return jsonify(output)

@app.route('/repo/categories')
def repo_categroies():
    output = {'status': 'OK', 'msg': ''}
    try:
        categories = Category.select()
        categories = [model_to_dict(category) for category in categories]
        output['categories'] = categories
        return jsonify(output)
    except Exception:
        output['status'] = 'Err'
        output['msg'] = Exception
        return jsonify(output)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

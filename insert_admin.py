#!/usr/bin/env python3
from pymongo import MongoClient
from bcrypt import hashpw, checkpw, gensalt
import yaml
import os
import argparse

def insert_admin():
    dirs = os.listdir()
    if 'app' in dirs:
        f = open("app/config.cfg", 'r')
    else:
        f = open("./config.cfg", 'r')
    settings = yaml.load(f)
    mongo_client = MongoClient(settings['mongo_ip'], settings['mongo_port'])
    mongo_db = mongo_client['userinfo']
    userinfo = mongo_db['userinfo']
    f.close()

    parser = argparse.ArgumentParser(description = "Add admin user to MongoDB")
    parser.add_argument('-p', '--password', type = str, help = "Admin password", required = True)

    if userinfo.find({'username':'admin'}).count() > 0:
        print("Admin already exists")
    else:
        args = parser.parse_args()
        password = args.password
        hashed = hashpw(password.encode('utf-8'), gensalt())
        userinfo.insert_one({"username":"admin","password":hashed,"user_id":0})
        print("Successfully added an admin user with password {}!".format(password))

if __name__ == "__main__":
    insert_admin()
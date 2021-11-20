from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from random import randint
from db_con import get_db_instance, get_db

global_db_con = get_db()
from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    un = request.form['user']
    #use data here to auth the user
    cur = global_db_con.cursor()
    cur.execute("select * from users where username = '" + un  + "';")
    global_db_con.commit()
    queryRSP = cur.fetchall()
    
    if(len(queryRSP) == 0):
        recvdPSS = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
        usr = str(randint(1, 1000000))
        cur.execute("INSERT INTO users(id, username, salted_pass) VALUES(" + usr  + ",'" + un + "','" + recvdPSS.decode() + "');")
        global_db_con.commit()
        UID = {
                "sub" : usr #sub is used by pyJwt as the owner of the token
              }

    else:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False)

    return json_response(status_=200, token = create_token(UID), authenticated = True)

import jwt
from tools.get_aws_secrets import get_secrets
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from random import randint
from tools.logging import logger
from db_con import get_db_instance, get_db
secrets = get_secrets()

global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    pw = request.form['password']
    line = 35
    usr = 0
    cur = global_db_con.cursor()
    cur.execute("select * from users where username = '" + request.form['user']  + "';")
    global_db_con.commit()
    queryRSP = cur.fetchall()
    if(len(queryRSP) >  0):
        if(bcrypt.checkpw(bytes(pw, "utf-8"), bytes(queryRSP[0][2], "utf-8"))):
            usr = queryRSP[0][0]
            UID = {
                "sub" : usr #sub is used by pyJwt as the owner of the token
              }
        else: 
            goto(line)
    else:
        return json_response(status_=401, message = 'Invalid credentials', authenticated = False )
    
    return json_response(status_=200, token = create_token(UID), authenticated = True)

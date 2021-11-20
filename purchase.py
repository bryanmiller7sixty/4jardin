from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from db_con import get_db_instance, get_db
import cgi, cgitb
import datetime
global_db_con = get_db()
from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")
    cur = global_db_con.cursor()
    cur.execute("INSERT INTO purchases(U_ID, B_id, date_time) VALUES(" + str(g.jwt_data.get('sub'))  + ",'" + str(request.args.get('book_id')) + "','" + str(datetime.datetime.now()) + "');")
    #global_db_con.commit()
    return json_response(status_=200, data={ })


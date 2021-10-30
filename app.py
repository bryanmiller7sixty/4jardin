from flask import Flask,render_template,request, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt
import datetime
import bcrypt
import json

from db_con import get_db_instance, get_db
from random import randint

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    print(request.form)
    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
    print(salted)

    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

    return render_template('backatu.html',input_from_browser= str(request.form) )

@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")

# Assignment 3
@app.route('/login', methods=['POST','GET']) #endpoint
def login():
    #return redirect(request.referrer) 
    bln = 0
    usr = 0
    recvdUSR = jwt.encode({'username': request.args.get('username')} , JWT_SECRET, algorithm="HS256")
    cur = global_db_con.cursor()
    cur.execute("select * from users where username = '" + recvdUSR + "';")
    global_db_con.commit()
    queryRSP = cur.fetchall()
    if(len(queryRSP) >  0):
        print("In if block")
        if bcrypt.checkpw(bytes(request.args.get('password'), 'utf-8'), bytes(queryRSP[0][2], 'utf-8')):
            print("In if block")
            bln = 1
            usr = queryRSP[0][0]
    return json_response(data={"bln" : bln, "uID" : usr})



@app.route('/register', methods=['POST','GET']) #endpoint
def register():
    bln = 0
    usr = 0
    recvdUSR = jwt.encode({'username': request.args.get('username')} , JWT_SECRET, algorithm="HS256")
    recvdPSS = bcrypt.hashpw( bytes(request.args.get('password'),  'utf-8' ) , bcrypt.gensalt(10))
    cur = global_db_con.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + recvdUSR + "';");
    global_db_con.commit()
    queryRSP = cur.fetchall()
    if(len(queryRSP) == 0):
        cur.execute("INSERT INTO users(id, username, salted_pass) VALUES(" + str(randint(1, 1000000))  + ",'" + recvdUSR + "','" + recvdPSS.decode() + "');")
        global_db_con.commit()
        bln = 1
        usr = 11 
    return json_response(data={"bln" : bln, "uID" : usr})

@app.route('/popBooks', methods=['POST','GET']) #endpoint
def popBooks():
    cur = global_db_con.cursor()
    cur.execute("SELECT * FROM books;");
    global_db_con.commit()
    queryRSP = cur.fetchall()
    return json_response(data=queryRSP)

@app.route('/purchase', methods=['POST','GET']) #endpoint
def purchase():
    cur = global_db_con.cursor()
    cur.execute("INSERT INTO purchases(U_ID, B_id, date_time) VALUES(" + request.args.get('uid')  + ",'" + request.args.get('bid') + "','" + str(datetime.datetime.now()) + "');")
    global_db_con.commit()
    return json_response(data="Success, thank you for your purchase!")

app.run(host='0.0.0.0', port=80)


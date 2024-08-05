from flask import json
import mysql.connector
from flask import make_response,request
import jwt
import re
class auth_model:
    def __init__(self):
        # connection establishment code 
        try:
            self.conn = mysql.connector.connect(host="localhost",user="root",password="Vamsi.2002",database="Flask_CRUD")
            self.conn.autocommit = True
            self.curr = self.conn.cursor(dictionary=True)
            print('success')
        except:
            print("error")
    
    def token_auth(self,endpoint):
        def inner1(func):
            def inner2(*args):
                auth = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$",auth,flags=0):
                    token = auth.split(" ")[1]
                    decoded = jwt.decode(token,"ram",algorithms="HS256")
                    role_id = decoded['payload']['role_id']
                    self.curr.execute(f"SELECT roles FROM accessbility_view WHERE endpoint='{endpoint}")
                    res = self.curr.fetchall()
                    if len(res)>0:
                        
                    return func(*args)
                return "Invalid token"
            return inner2
        return inner1


from flask import json
import mysql.connector
from flask import make_response
from datetime import datetime, timedelta
import jwt
class user_model:
    def __init__(self):
        # connection establishment code 
        try:
            self.conn = mysql.connector.connect(host="localhost",user="root",password="Vamsi.2002",database="Flask_CRUD")
            self.conn.autocommit = True
            self.curr = self.conn.cursor(dictionary=True)
            print('success')
        except:
            print("error")
    
    # CREATE
    def user_add_model(self,data):
        self.curr.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
        return make_response({"message":"Data added successfully"},201)

    # READ
    def user_getall_model(self):
        self.curr.execute("SELECT * FROM users")
        res = self.curr.fetchall()
        if len(res)>0:
            ans = make_response({'payload':res},200)
            ans.headers['Access-Control-Allow-Origin']='*'
            return ans
        return make_response({'message':"No Data Found"},204)
    
    # UPDATE
    def user_update_model(self,data):
        self.curr.execute(f"UPDATE users SET name='{data['name']}',role='{data['role']}' WHERE id={data['id']}")
        if self.curr.rowcount>0:
            return make_response({"message":"updated successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
        
    
    # DELETE
    def user_delete_model(self,id):
        self.curr.execute(f"DELETE FROM users WHERE id={id}")
        if self.curr.rowcount>0:
            return make_response({'message':"Data deleted successfully"},200)
        else:
            return make_response({'message':"Nothing to delete"},202)
        
    # PATCH
    def user_patch_model(self,data,id):
        updates = ""
        for key,val in data.items():
            updates+=f"{key}='{val}',"
        query = f"UPDATE users SET {updates[:-1]} WHERE id={id}"
        self.curr.execute(query)
        if self.curr.rowcount>0:
            return make_response({"message":"updated successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
    
    # READ
    def user_get_model(self,pno):
        query = f"SELECT * FROM users LIMIT {(int(pno)-1)*5},5"
        self.curr.execute(query)
        res = self.curr.fetchall()
        if len(res)>0:
            ans = make_response({'payload':res},200)
            ans.headers['Access-Control-Allow-Origin']='*'
            return ans
        return make_response({'message':"No Data Found"},204)
    
    # PUT
    def user_upload_avatar_model(self,uid,filePath):
        query = f"UPDATE users SET avatar='{filePath}' WHERE id={uid}"
        self.curr.execute(query)
        if self.curr.rowcount>0:
            return make_response({"message":"updated successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
        
    # POST JWT
    def user_login_model(self,data):
        self.curr.execute(f"SELECT name,email,phone,avatar,role_id FROM users WHERE name='{data['username']}' AND password='{data['password']}'")
        res = self.curr.fetchall()
        userdata = res[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time
        }
        token = jwt.encode(payload,"ram",algorithm="HS256")
        return make_response({"token":token},200)
        
    
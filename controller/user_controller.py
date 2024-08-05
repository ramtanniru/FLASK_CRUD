from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request,send_file
from datetime import datetime

obj = user_model()
auth = auth_model()

@app.route("/user/getall")
@auth.token_auth('/user/getall')
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/get/limit/<pno>")
def user_get_controller(pno):
    return obj.user_get_model(pno)

@app.route('/user/add',methods=['POST'])
def user_add():
    return obj.user_add_model(request.form)

@app.route('/user/update',methods=['PUT'])
def user_update():
    return obj.user_update_model(request.form)

@app.route('/user/delete/<id>',methods=['DELETE'])
def user_delete(id):
    return obj.user_delete_model(id)

@app.route('/user/patch/<id>',methods=['PATCH'])
def user_patch(id):
    return obj.user_patch_model(request.form,id)

@app.route('/user/<uid>/upload/avatar',methods=['PUT'])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    name = str(datetime.now().timestamp()).replace('.','_')
    filePath = f"uploads/{name}.{file.filename.split('.')[-1]}"
    file.save(filePath)
    return obj.user_upload_avatar_model(uid,filePath)

@app.route('/uploads/<filename>',methods=['GET'])
def user_getavatar_controlller(filename):
    return send_file(f'uploads/{filename}')


# JWT
@app.route('/user/login',methods=['POST'])
def user_login_controller():
    return obj.user_login_model(request.form)
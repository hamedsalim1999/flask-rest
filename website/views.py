from flask import jsonify,request,Blueprint
from flask_jwt_extended import jwt_required,create_access_token
from flask_mail import Message
from .models import User
from . import db,mail
from .serilizers import users_schema,user_schema
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

@views.route('/')
def main_page():
    return jsonify(msg="hello it's me"), 200


@views.route('/not_found')
def not_found():
    return jsonify(msg="sorry this resource was not found"),404


@views.route('/paramerts')
def paramets_dy ():
    email=request.args.get('email')
    name=request.args.get('name')
    age=int(request.args.get('age'))
    if age < 18:
        return jsonify(msg=f"sorry {name} you are not old enough") , 401
    else:
        data = User(name=name,age=age,email=email)
        db.session.add(data)
        db.session.commit()
        return jsonify(msg=f"welcome {name}"), 201


@views.route('/url/<string:name>/<string:email>/<int:age>',methods=['GET','POST'])
def paramets_st(name: str,age: int,email:str):

    if age < 18:
        return jsonify(msg=f"sorry {name} you are not old enough") , 401
    else:
        data = User(name=name,age=age,email=email)
        db.session.add(data)
        db.session.commit()
        return jsonify(msg=f"welcome {name}"), 200

@views.route('/result',methods=['GET'])
def return_data():
    data = User.query.all()
    result = users_schema.dump(data)
    return jsonify(result)


@views.route('/register',methods=['POST'])
def register():
    name = request.form['name']
    test = User.query.filter_by(name=name).first()
    if test :
        return jsonify (msg="that user alredy exists"),409
    else :
        age = request.form['age']
        user = User(name=name,age=age)
        db.session.add(user)
        db.session.commit()
        return jsonify (msg="user crate"),201


@views.route('/login',methods=['POST'])
def login():
    if request.is_json:
        age = request.json['age']
        email = request.json['email']
    else :
        email = request.form['email']
        age = request.form['age']
    
    test = User.query.filter_by(email= email , age = age ).first()
    if test :
        acess_token = create_access_token(identity=email)
        return jsonify(msg="log in ",acess_token=acess_token)
    else:
        return jsonify(msg='your name is wrong')


@views.route('/retrive/<string:email>',methods=['GET'])
def retrive(email : str):
    user = User.query.filter_by(email=email).first()
    if user :
        msg = Message(f"your age is {user.age}",sender=os.environ['MAIL_USERNAME'],recipients=[email])
        mail.send(msg)
        return jsonify(msg="password was send")
    else:
        return jsonify(msg="your email not exiest")
@views.route('/get/<int:id>')
def get_by_id(id: int):
    data = User.query.filter_by(id=id).first()
    if data:
        result = user_schema.dump(data)
        return jsonify(result) , 200
    else:
        return jsonify(msg="we don't have this id ") ,404


@views.route('/senddata',methods=['POST'])
@jwt_required()
def send_data():
    email = request.form['email']
    data = User.query.filter_by(email=email).first()
    if data :
        return jsonify(msg='this email dos exist'),409
    else:
        name=request.form['name']
        age=int(request.form['age'])
        new_user = User(
                email=email,
                name=name,
                age=age,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify (msg="user crate"),201


@views.route('/update_data',methods=['PUT'])
@jwt_required()
def update_data():
    user_id = request.form['id']
    data = User.query.filter_by(id=user_id).first()
    if data :
        data.email=request.form['email']
        data.name=request.form['name']
        data.age=int(request.form['age'])
        db.session.commit()
        return jsonify(msg='your data was update'),201
    else:

        return jsonify (msg="we dont have your data"),404


@views.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_data():
    user_id = request.form['id']
    data = User.query.filter_by(id=user_id).first()
    if data :
        db.session.delete(data)
        db.session.commit()
        return jsonify(msg='your data was deleted'),201
    else:

        return jsonify (msg="we dont have your data"),404
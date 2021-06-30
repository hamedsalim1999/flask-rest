from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , Integer , String , Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
from flask_mail import Mail , Message
import os
from dotenv import load_dotenv
load_dotenv()

# config
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "2Hk8q_YjpSzxLyXjA" 
jwt = JWTManager(app)
ma = Marshmallow(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir,'mydb.db')}"
db= SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# models
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("data base is create")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("data base is drop")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'age',
            'email',
        )
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# view functions 
@app.route('/')
def main_page():
    return jsonify(msg="hello it's me"), 200


@app.route('/not_found')
def not_found():
    return jsonify(msg="sorry this resource was not found"),404


@app.route('/paramerts')
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


@app.route('/url/<string:name>/<string:email>/<int:age>',methods=['GET','POST'])
def paramets_st(name: str,age: int,email:str):

    if age < 18:
        return jsonify(msg=f"sorry {name} you are not old enough") , 401
    else:
        data = User(name=name,age=age,email=email)
        db.session.add(data)
        db.session.commit()
        return jsonify(msg=f"welcome {name}"), 200

@app.route('/result',methods=['GET'])
def return_data():
    data = User.query.all()
    result = users_schema.dump(data)
    return jsonify(result)


@app.route('/register',methods=['POST'])
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


@app.route('/login',methods=['POST'])
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


@app.route('/retrive/<string:email>',methods=['GET'])
def retrive(email : str):
    user = User.query.filter_by(email=email).first()
    if user :
        msg = Message(f"your age is {user.age}",sender=os.environ['MAIL_USERNAME'],recipients=[email])
        mail.send(msg)
        return jsonify(msg="password was send")
    else:
        return jsonify(msg="your email not exiest")
@app.route('/get/<int:id>')
def get_by_id(id: int):
    data = User.query.filter_by(id=id).first()
    if data:
        result = user_schema.dump(data)
        return jsonify(result) , 200
    else:
        return jsonify(msg="we don't have this id ") ,404


@app.route('/senddata',methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
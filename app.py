from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , Integer , String , Float
import os

# config
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir,'mydb.db')}"

db= SQLAlchemy(app)


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
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)


# view functions 
@app.route('/')
def main_page():
    return jsonify(msg="hello it's me"), 200


@app.route('/not_found')
def not_found():
    return jsonify(msg="sorry this resource was not found"),404


@app.route('/paramerts')
def paramets_dy ():
    name=request.args.get('name')
    age=int(request.args.get('age'))
    if age < 18:
        return jsonify(msg=f"sorry {name} you are not old enough") , 401
    else:
        return jsonify(msg=f"welcome {name}"), 200


@app.route('/url/<string:name>/<int:age>')
def paramets_st(name: str,age: int):

    if age < 18:
        return jsonify(msg=f"sorry {name} you are not old enough") , 401
    else:

        return jsonify(msg=f"welcome {name}"), 200




if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route('/')
def main_page():
    return jsonify(msg="hello it's me"), 200


@app.route('/not_found')
def not_found():
    return jsonify(msg="sorry this resource was not found"),404


@app.route('/paramerts')
def paramets():
    name=request.args.get('name')
    age=int(request.args.get('age'))
    if age < 18:
        return jsonify(msg=f"sorry you{name}are not old enough") , 401
    else:
        return jsonify(msg=f"welcome{name}"), 200

if __name__ == '__main__':
    app.run(debug=True)
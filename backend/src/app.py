from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonreactdb'
mongo = PyMongo(app)

db = mongo.db.users


@app.route('/usuarios', methods=['POST'])
def crearUsuarios():
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    #print(jsonify(str(ObjectId(id))))
    return jsonify(str(id))

@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    users = []
    for doc in db.find():
        users.append({
            '_id':str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': ['email'],
            'password': ['password']
        })
    return jsonify(users)

@app.route('/usuario/<id>', methods=['GET'])
def getUsuario(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
    })

@app.route('/usuario/<id>', methods=['DELETE'])
def eliminarUsuario(id):
    db.delete_one({'id': ObjectId(id)})
    return jsonify({'msg': 'Usuario eliminado'})

@app.route('/usuario/<id>', methods=['PUT'])
def actualizarUsuario(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'msg': 'Usuario actualizado'})

if __name__ == "__main__":
    app.run(debug=True)
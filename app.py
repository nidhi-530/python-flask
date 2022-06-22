from bson import ObjectId
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask import jsonify, request
from bson.json_util import dumps

app = Flask(__name__)

app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/mydatabase"

mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_customers():
  _json=request.json
  _name=_json['name']
  _address=_json['address']

  if _name and _address and request.method == 'POST':
    id = mongo.db.customers.insert_one({'name':_name,'address':_address})

    resp = jsonify("Record Added Successfully")
    resp.status_code =200
    return resp

  else:
    return not_found()


@app.route('/customers')
def customers():
  customers = mongo.db.customers.find()
  resp = dumps(customers)
  return resp

@app.route('/custById/<id>')
def custId(id):
  customer = mongo.db.customers.find_one({"_id": ObjectId(id)}) 
  resp = dumps(customer)
  return resp

@app.route('/delete/<id>')
def deleteCustomer(id):
  mongo.db.customers.delete_one({"_id": ObjectId(id)}) 
  resp = jsonify("User Deleted Successfully")
  return resp

@app.route('/updateCustomer/<id>', methods=['PUT'])
def update_customers(id):
  _id = id
  _json = request.json
  _name = _json['name']
  _address = _json['address']

  if _id and _name and _address and request.method == 'PUT':
    mongo.db.customers.update_one( {"_id": ObjectId(id)}, {"$set": {'name':_name,'address':_address}} )
    resp = jsonify("Record Updated Successfully")
    resp.status_code =200
    return resp

  else:
    return not_found()



@app.errorhandler(404)
def not_found(error=None):
  message = {
    'status':404,
    'message': 'Not found' + request.url
  }

  resp = jsonify(message)
  resp.status_code =200

  return resp  

if __name__ == "__main__":
  app.run(debug=True)

from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

cloth = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["cloth"]
collection = db["item"]
@cloth.route("/addcloths" , methods = ['POST'])
def addcloths():
    data = request.json
    clothname=data.get("clothname")
    itemname1=data.get("itemname 1")

    existing_item=collection.find_one({"clothname":clothname,"itemname 1":itemname1})

    if existing_item:
        return jsonify({"error":"item1 already exists in this cloth"})
    else:
        result=collection.insert_one(data)
        return jsonify({'id':str(result.inserted_id)})
    result = collection.insert_one(data)
    return jsonify({'id':str(result.inserted_id)})

@cloth.route("/getcloths", methods = ['GET'])
def getproduct():
    result = list(collection.find())
    for results in result:
        results['_id'] = str(results['_id'])
    return jsonify(result)

@cloth.route("/putcloths/<_id>" , methods = ['PUT'])
def putcloths(_id):
    data = request.json
    clothname=data.get("clothname")
    itemname=data.get("itemname")
    object_id = ObjectId(_id)

    existing_item=collection.find_one({
        '_id':{'$ne':object_id},
        'clothname':clothname,
        'itemname':itemname
    })

    if existing_item:
        return jsonify({"MESSAGE":"PRODUCT UPDATED"})
    else:
        result = collection.update_one({'_id': object_id} ,{'$set':data})
    return jsonify({"error":"there are empty item"})



@cloth.route("/getsname/<_id>" , methods = ['GET'])
def getsname(_id):
    object_id = ObjectId(_id)
    result = collection.find_one({'_id':object_id})
    result['_id'] = str(result['_id'])
    return jsonify(result)

@cloth.route("/deletecloths/<_id>" , methods = ['DELETE'])
def deletecloths(_id):
    data = request.json
    object_id = ObjectId(_id)
    result = collection.delete_one({'_id': object_id})
    return jsonify({"MESSAGE":"PRODUCT DELETE"})


if __name__ == "__main__":
    cloth.run(debug=True)
 


 



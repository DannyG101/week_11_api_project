import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import json_util, ObjectId
import json

load_dotenv()

port= os.getenv('DB_PORT')
host= os.getenv('DB_HOST')
db_name= os.getenv('DB_NAME')




def get_connection():
    try:
        uri = f"mongodb://{host}:{port}/"
        print(uri)
        client = MongoClient(uri)
        client.admin.command("ping")
        print("✓ Successfully connected to MongoDB!")
        database = client[db_name]
        collection = database["contacts"]
        return collection
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to collection on Mongodb: {e}")
        print("Make sure MongoDB is running on localhost:27017")
        return None


def get_all_contacts():
    list_of_contacts = []
    collection = get_connection()
    results = json.loads(json_util.dumps(collection.find({})))
    for contact in results:
        list_of_contacts.append(contact)
    return list_of_contacts


def add_contact(contact_dict:dict):
    collection = get_connection()
    new_contact = {"first_name": contact_dict["first_name"],
                   "last_name": contact_dict["last_name"],
                   "phone_number": contact_dict["phone_number"]}
    added_contact = collection.insert_one(new_contact)
    return {"message": "Contact added successfully",
            "id":str(added_contact.inserted_id)
            }

def update_contact(user_id, contact_dict:dict):
    collection = get_connection()
    updated_contact = {"first_name": contact_dict["first_name"],
                   "last_name": contact_dict["last_name"],
                   "phone_number": contact_dict["phone_number"]}
    collection.replace_one({"_id": ObjectId(user_id)}, updated_contact)
    return {"message": "Contact updated successfully"}

def delete_contact(user_id):
    collection = get_connection()
    collection.delete_one({"_id":ObjectId(user_id)})
    return {"message": "Contact deleted successfully"}


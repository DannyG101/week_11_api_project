from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import List, Dict, Optional
from bson import json_util, ObjectId
import json

def get_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        client.admin.command("ping")
        print("✓ Successfully connected to MongoDB!")
        database = client["contacts_db"]
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


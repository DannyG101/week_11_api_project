import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from bson import json_util, ObjectId
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB   = os.getenv("MONGO_DB")


def get_connection():
    try:
        uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
        client = MongoClient(uri)
        client.admin.command("ping")
        print("✓ Successfully connected to MongoDB!")
        database = client[MONGO_DB]
        collection = database["contacts"]

        collection.create_index([("phone_number", ASCENDING)], unique=True)

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

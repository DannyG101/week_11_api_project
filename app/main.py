from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import data_interactor
from utils import helper_functions
import uvicorn

app = FastAPI()

class Contact(BaseModel):
    first_name : str
    last_name : str
    phone_number :str


@app.get("/contacts")
def get_all_contacts():
    try:
        return data_interactor.get_all_contacts()
    except HTTPException as err:
        return {"ERROR": err}


@app.post("/contacts")
def add_contact(contact:Contact):
    try:
        contact_object = helper_functions.data_to_contact_object(contact)
        contact_dict = contact_object.contact_to_dict()
        return data_interactor.add_contact(contact_dict)
    except HTTPException as err:
        return err


@app.put("/contacts/{user_id}")
def update_contact(user_id, contact:Contact):
    try:
        contact_object = helper_functions.data_to_contact_object(contact)
        contact_dict = contact_object.contact_to_dict()
        return data_interactor.update_contact(user_id, contact_dict)
    except HTTPException as err:
        return err


@app.delete("/contacts/{user_id}")
def delete_contact(user_id):
    try:
        return data_interactor.delete_contact(user_id)
    except HTTPException as err:
        return err

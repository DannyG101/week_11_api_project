class Contact:
    def __init__(self, first_name:str, last_name:str, phone_number:str, contact_id:str=None):
        self.id = contact_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def contact_to_dict(self):
        return {"id": self.id,"first_name": self.first_name, "last_name": self.last_name, "phone_number": self.phone_number}
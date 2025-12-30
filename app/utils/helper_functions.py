from models import contact


def data_to_contact_object(data):
    return contact.Contact(data.first_name, data.last_name, data.phone_number)
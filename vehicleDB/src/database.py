import os
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient(os.environ["DB_URL"])
database = client.vehicledb
driver_collection = database.get_collection("drivers")

def driver_helper(driver) -> dict:
    return {
        "id": str(driver["_id"]),
        "full name": str(driver["full_name"]),
        "dni": str(driver["dni"]),
        "facial_embedding": str(driver["facial_embedding"])
    }

def get_drivers():
    drivers = []
    for driver in driver_collection.find():
        drivers.append(driver_helper(driver))
    return drivers

# Agregar un driver a la base de datos

def add_driver(driver_data: dict) -> dict:
    driver = driver_collection.insert_one(driver_data)
    new_driver = driver_collection.find_one({"_id": driver.inserted_id})
    return driver_helper(new_driver)

# Buscar un driver a partir de un ID
def get_driver(id: str) -> dict:
    driver = driver_collection.find_one({"_id": ObjectId(id)})
    if driver:
        return driver_helper(driver)


# Actulizar un driver a partir de un ID
def update_driver(id: str, data: dict):
    # Devuelve falso si el cuerpo del request está vacio
    if len(data) < 1:
        return False
    driver = driver_collection.find_one({"_id": ObjectId(id)})
    if driver:
        updated_driver = driver_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_driver:
            return True
        return False

# Borrar un driver de la base de datos
def delete_driver(id: str):
    driver = driver_collection.find_one({"_id": ObjectId(id)})
    if driver:
        driver_collection.delete_one({"_id": ObjectId(id)})
        return True
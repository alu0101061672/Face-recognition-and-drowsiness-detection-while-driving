from hashlib import new
from fastapi import FastAPI, UploadFile, Form #Python class that provides all the functionality for your API
from models.driver import *
from models.license import *
from models.vehicle import *
from database import *
import bson.json_util as json_util
import json
from bson import ObjectId
from dateutil.relativedelta import relativedelta
import cv2
import face_recognition
import re

app = FastAPI() #FastAPI instance

@app.get("/")
def root() -> dict:
    return {"message": "Hello world"}

#######################################DRIVERS################################################
###############################################################################################
##############################################################################################
##############################################################################################

#####################################GET FUNCTIONS#############################################
@app.get("/drivers/")
def get_drivers():
    drivers = []
    for driver in drivers_collection.find():
        res = {key: driver[key] for key in driver.keys()
            & {'_id', 'full_name', 'gender', 'dni', 'address', 'infractions'}}
        drivers.append(res)
    return json.loads(json_util.dumps(drivers))

@app.get("/drivers/{driver_id}")
def get_driver_by_id(driver_id):
    driver = drivers_collection.find_one({'_id': ObjectId(driver_id)})
    res = {key: driver[key] for key in driver.keys()
            & {'_id', 'full_name', 'gender', 'dni', 'address', 'infractions', 'facial_embedding'}}
    return json.loads(json_util.dumps(res))

@app.get("/drivers/encoding/{dni}")
def get_encoding_by_dni(dni):
    driver = drivers_collection.find_one({'dni': dni})
    return driver["facial_embedding"]

#####################################POST FUNCTIONS###########################################
############
@app.post("/drivers/")
async def create_driver(full_name: str = Form(), gender: Gender = Form(), dni: str = Form(), address: str = Form(), infractions: str = Form(), face: UploadFile = Form()):
    img = face_recognition.load_image_file(face.file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)
    driver_dict = {
        "full_name": full_name,
        "gender": gender,
        "dni": dni,
        "address": address,
        "facial_embedding": encode[0].tolist(),
        "infractions": infractions.split(","),
        "created_at": datetime.now()
    }
    driver = drivers_collection.insert_one(driver_dict)
    new_driver = drivers_collection.find_one({"_id": driver.inserted_id})
    res = {key: new_driver[key] for key in new_driver.keys()
            & {'_id', 'full_name', 'gender', 'dni'}}
    return json.loads(json_util.dumps(res))

#####################################PUT FUNCTIONS############################################

@app.put("/drivers/{driver_id}")
def update_driver_data(driver_id, data: dict):
    if len(data) < 1:
        return "no se ha podido hacer el update"
    driver = drivers_collection.find_one({'_id': ObjectId(driver_id)})
    if driver:
        updated_driver = drivers_collection.update_one({'_id': ObjectId(driver_id)}, {'$set': data})
        if updated_driver:
            new_values = drivers_collection.find_one({'_id': ObjectId(driver_id)})
            return json.loads(json_util.dumps(new_values))
    return "no se ha podido hacer el update"

@app.put("/drivers/photo/{driver_id}")
def update_driver_photo(driver_id, face: UploadFile = Form()):
    if len(face.filename) < 1:
        return "no se ha podido hacer el update"
    img = face_recognition.load_image_file(face.file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)

    new_data = {
        "facial_embedding": encode[0].tolist(),
    }
    driver = drivers_collection.find_one({'_id': ObjectId(driver_id)})
    if driver:
        updated_driver = drivers_collection.update_one({'_id': ObjectId(driver_id)}, {'$set': new_data})
        if updated_driver:
            new_values = drivers_collection.find_one({'_id': ObjectId(driver_id)})
            return json.loads(json_util.dumps(new_values))
    return "no se ha podido hacer el update"

#####################################DELETE FUNCTIONS#########################################
@app.delete("/drivers/")
def delete_all_drivers():
    drivers_collection.delete_many({})
    return {"All drivers deleted"}

@app.delete("/drivers/{driver_id}")
def delete_one_driver(driver_id):
    drivers_collection.delete_one({"_id" : ObjectId(driver_id)})
    return "Driver has been correctly deleted"

#######################################VEHICLES###############################################
##############################################################################################
##############################################################################################
##############################################################################################

#####################################GET FUNCTIONS############################################
@app.get("/vehicles/")
def get_vehicles():
    vehicles = []
    for vehicle in vehicles_collection.find():
        vehicles.append(vehicle)
    return json.loads(json_util.dumps(vehicles))

@app.get("/vehicles/{driver_id}")
def get_vehicles_from_owner(driver_id):
    vehicles = vehicles_collection.find({'driver_id': driver_id})
    driver = drivers_collection.find_one({'_id': ObjectId(driver_id)})
    res = {key: driver[key] for key in driver.keys()
            & {'_id', 'full_name', 'gender', 'dni'}}
    driver_vehicles = {"driver": res, "vehicles": vehicles}
    return json.loads(json_util.dumps(driver_vehicles))

#####################################POST FUNCTIONS###########################################
@app.post("/vehicles/")
def create_vehicle(vehicle: dict):
    vehicle = vehicles_collection.insert_one(vehicle)
    new_vehicle = vehicles_collection.find_one({"_id": vehicle.inserted_id})
    return json.loads(json_util.dumps(new_vehicle))

#####################################PUT FUNCTIONS############################################

@app.put("/vehicles/{vehicle_id}")
def update_vehicle_data(vehicle_id, data: dict):
    if len(data) < 1:
        return "no se ha podido hacer el update"
    vehicle = vehicles_collection.find_one({'_id': ObjectId(vehicle_id)})
    print(vehicle)
    if vehicle:
        updated_vehicle = vehicles_collection.update_one({'_id': ObjectId(vehicle_id)}, {'$set': data})
        if updated_vehicle:
            new_values = vehicles_collection.find_one({'_id': ObjectId(vehicle_id)})
            return json.loads(json_util.dumps(new_values))
    return "no se ha podido hacer el update"

#####################################DELETE FUNCTIONS#########################################
@app.delete("/vehicles/")
def delete_all_vehicles():
    vehicles_collection.delete_many({})
    return {"All vehicles deleted"}

@app.delete("/vehicles/{driver_id}")
def delete_one_driver_vehicle(driver_id):
    vehicles_collection.delete_one({"driver_id" : driver_id})
    return "Driver's vehicle has been correctly deleted"

#######################################LICENSES###############################################
##############################################################################################
##############################################################################################
##############################################################################################

#####################################GET FUNCTIONS############################################

@app.get("/licenses/")
def get_licenses():
    licenses = []
    for lic in licenses_collection.find():
        licenses.append(lic)
    return json.loads(json_util.dumps(licenses))

@app.get("/licenses/{driver_id}")
def get_license_from_owner(driver_id):
    licenses = licenses_collection.find({'driver_id': driver_id})
    driver = drivers_collection.find_one({'_id': ObjectId(driver_id)})
    res = {key: driver[key] for key in driver.keys()
            & {'_id', 'full_name', 'gender', 'dni'}}
    driver_licenses = {"driver": res, "licenses": licenses}
    return json.loads(json_util.dumps(driver_licenses))

#####################################POST FUNCTIONS###########################################
@app.post("/licenses/{driver_id}")
def create_license(license: dict, driver_id):
    license["driver_id"] = driver_id
    license["expiration_date"] = (date.today() + relativedelta(years=10)).strftime('%d-%m-%Y')
    license = licenses_collection.insert_one(license)
    new_license = licenses_collection.find_one({"_id": license.inserted_id})
    print(new_license)
    return json.loads(json_util.dumps(new_license))

#####################################PUT FUNCTIONS############################################

@app.put("/licenses/{license_id}")
def update_license_data(license_id, data: dict):
    if len(data) < 1:
        return "no se ha podido hacer el update"
    oblicense = licenses_collection.find_one({'_id': ObjectId(license_id)})
    print(oblicense)
    if oblicense:
        updated_license = licenses_collection.update_one({'_id': ObjectId(license_id)}, {'$set': data})
        if updated_license:
            new_values = licenses_collection.find_one({'_id': ObjectId(license_id)})
            return json.loads(json_util.dumps(new_values))
    return "no se ha podido hacer el update"

#####################################DELETE FUNCTIONS#########################################
@app.delete("/licenses/")
def delete_all_licenses():
    licenses_collection.delete_many({})
    return {"All licenses deleted"}

@app.delete("/licenses/{driver_id}")
def delete_one_driver_license(driver_id):
    licenses_collection.delete_one({"driver_id" : driver_id})
    return "Driver's license has been correctly deleted"
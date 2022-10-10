from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database import (
    add_driver,
    delete_driver,
    get_driver,
    get_drivers,
    update_driver
)

from models.driver import (
    ErrorResponseModel,
    ResponseModel,
    SchemaDriver,
    UpdateDriverModel
)

router = APIRouter()

@router.post("/", response_description="Driver data inserted into database")
def add_driver_data(driver: SchemaDriver = Body(...)):
    driver = jsonable_encoder(driver)
    new_driver = add_driver(driver)
    return ResponseModel(new_driver, "New driver inserted")

@router.get("/", response_description="Get drivers data")
def get_drivers_data():
    drivers = get_drivers()
    if drivers:
        return ResponseModel(drivers, "Drivers data retrieved")
    return ResponseModel(drivers, "Empty list")


@router.get("/{id}", response_description="Get one driver data")
def get_driver_data(id):
    driver = get_driver(id)
    if driver:
        return ResponseModel(driver, "Driver data retrieved")
    return ErrorResponseModel("Error", 404, "Driver does not exist")


@router.put("/{id}")
def update_driver_data(id: str, req: UpdateDriverModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_driver = update_driver(id, req)
    if updated_driver:
        return ResponseModel(
            "Updated driver with id: {} ".format(id), "Driver correctly updated"
        )
    return ErrorResponseModel(
        "Error",
        404,
        "Driver could not be updated",
    )

@router.delete("/{id}", response_description="driver data deleted from the database")
def delete_driver_data(id: str):
    deleted_driver = delete_driver(id)
    if deleted_driver:
        return ResponseModel(
            "driver ID: {} deleted".format(id), "Driver correctly deleted"
        )
    return ErrorResponseModel(
        "Error", 404, "Driver with id {0} does not exist".format(id)
    )
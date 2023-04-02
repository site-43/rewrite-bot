##### Database Manager file. #####

import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from colorama import Fore
load_dotenv()
cluster = MongoClient(host=os.getenv("MONGO_DB_CONNECTION_STRING"))

async def addData(
    database: str = "main",
    collection: str = "unsaved",
    document: dict = None,
):
    if document == None:
        print(Fore.LIGHTMAGENTA_EX + "Aucun document n'a été passé dans la DB." + Fore.RESET)
        return
    
    database = cluster[database][collection]
    data = database.insert_one(document)
    return data

async def getData(
    database: str = "main",
    collection: str = "unsaved",
    searchValue: dict = None
):
    if not searchValue:
        return False

    database = cluster[database][collection]
    data = database.find_one(searchValue)
    return data or None

async def deleteData(
    database:str = "main",
    collection: str = "unsaved",
    searchValue: dict = None
):
    if not searchValue:
        return False
    
    database = cluster[database][collection]
    todel = database.find_one(searchValue)
    if todel:
        database.delete_one(todel)
    else:
        return None

async def updateData(
    database:str = "main",
    collection: str = "unsaved",
    filters: str = None,
    document: str = None
):
    if not document or not filters:
        return False
    print(filters)
    database = cluster[database][collection]
    toupdate = database.update_one(filters, document)

async def getCount(
    database:str = "main",
    collection:str = "unsaved"
):
    database = cluster[database][collection]
    return database.estimated_document_count()
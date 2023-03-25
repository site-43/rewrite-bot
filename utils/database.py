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
    print(database)
    data = database.insert_one(document)
    return data

async def getData(
    database: str = "main",
    collection: str = "unsaved",
    searchValue: dict = {}
):
    if not searchValue:
        return False

    database = cluster[database][collection]
    data = database.find_one(searchValue)
    return data or None
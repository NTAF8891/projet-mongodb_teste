from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.database import Database

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path

# Chargement du fichier .env
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

# Données de connexion
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
cluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB_NAME")
coll_name = os.environ.get("COLL_NAME")

# Vérification
if not username or not password or not cluster or not db_name or not coll_name:
    raise ValueError("Vérifie ton fichier .env — une ou plusieurs variables sont vides.")

# Construction de l'URI
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}.mongodb.net/"

class MongoManager:
    def _init_(self, uri: str, db_name: str, coll_name: str):
        self.__client = MongoClient(uri, server_api=ServerApi('1'), tls=True)
        try:
            ping = self.__client.admin.command({'ping': 1})
            print(f"Pinged your deployment: {ping}. Successfully connected to MongoDB.")
        except Exception as e:
            raise Exception("Unable to connect to MongoDB due to the following error: ", e)

        self._db: Database = self._client["excercise"]
        self._collection: Collection = self._db["jeux videos"]

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db_name: str):
        self._db = self._client[db_name]
        self._collection = self._db[self.__collection.name]

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, coll_name: str):
        self._collection = self._db[coll_name]

    def list_databases(self):
        try:
            return self.__client.list_database_names()
        except Exception as e:
            raise Exception("Unable to list the databases: ", e)

    def list_collections(self):
        try:
            return self.__db.list_collection_names()
        except Exception as e:
            raise Exception("Unable to list the collections: ", e)

    def read_many_documents(self, query: dict, projection: dict = None, sort: list = None, limit: int = 0):
        try:
            cursor = self.__collection.find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            raise Exception("Unable to read the documents due to the following error:", e)

    def close_connection(self):
        self.__client.close()
        print("Connection closed.")

mongo = MongoManager() 
games_3ds = mongo.read_many_documents(
    { "platform": { "$regex": "3DS", "$options": "i" } }
)

for g in games_3ds:
    print(g)
        
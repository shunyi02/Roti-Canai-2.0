from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://admin:admin@cluster0.tu1qoxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))

# Access the specified database
db = client['roticanai']

# Access the specified collection
collection = db['roticanai']

# Define the documents to be inserted
documents = [
    {
        "userId": "admin1",
        "walletId": "",
        "walletAddr": "",
        "balance": 0,
        "pass": "123",
        "email": "admin1@gmail.com"
    },
    {
        "userId": "admin2",
        "walletId": "",
        "walletAddr": "",
        "balance": 0,
        "pass": "123",
        "email": "admin2@gmail.com"
    },
    {
        "userId": "admin",
        "walletId": "",
        "walletAddr": "",
        "balance": 0,
        "pass": "123",
        "email": "admin@gmail.com"
    }
]

# Insert the documents into the collection
insert_result = collection.insert_many(documents)

# Print the inserted documents' IDs
print(f"Documents inserted with IDs: {insert_result.inserted_ids}")

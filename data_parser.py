import json 
import bank_pb2

# Data feed functions for server. 
# Don't want to messup the server code and making things modular

def read_finance_data():
    ls = []
    with open('bank_db.json') as database:
        for item in json.load(database):
            element = bank_pb2.FinanceDetails(
                Account_No = item["Account_No"],
                Name = item["Name"],
                Balance = item["Balance"])
            ls.append(element)
    return ls

def read_personal_data():
    ls = []
    with open('bank_db.json') as database:
        for item in json.load(database):
            element = bank_pb2.CustomerDetails(
                Account_No = item["Account_No"],
                Name = item["Name"],
                Age = item["Age"],
                Gender = item['Gender'])
            ls.append(element)
    return ls

# with open('bank_db.json') as database:
#     for item in json.load(database):
#         if(item["Account_No"] == "RBC19569"):
#             print("Name: " + str(item["Name"]))
#             print("Balance: " + str(item["Balance"])) 
#             break
#         else:
#             print("Searching . . .")
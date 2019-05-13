from concurrent import futures
import grpc 
import time 
import bank_pb2
import bank_pb2_grpc
import logging 
import datetime
from pymongo import MongoClient

'''
To replicate this server code make sure you have following schema configured for your MongoDB


Database Name: BankDB
Collection Name: Customers
Example of document for MongoDB collection:

{
    {
        "_id":"5cd9f08fcfbd5507b03d2ca6",
        "Account_No":"RBCD16600",
        "Name":"Adrian Smith",
        "Balance":9500,
        "Age":22
    }
}

'''

# Server Live time variable :P

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BankServicer(bank_pb2_grpc.BankOpsServicer):
    
    def __init__(self,*args, **kwargs):
        self.client = MongoClient('localhost',27017)

    # QueryDetails is a similar implementation like QueryBalance as shown below
    # Function names in server should be same as the ones specified in .proto file rpc definitions

    def QueryBalance(self,request,context):
        # Data Query Variable 
        acc_no = request.Account_No
        # Data Store Variables 
        name = None
        balance = None
        # Query Fire
        cursor = self.client.BankDB.Customers.find({"Account_No": acc_no})
        for x in cursor:
            name = x["Name"]
            balance = x["Balance"]
        if name and balance != None:
            print("Request Accepted for " + acc_no + "------" + str(datetime.datetime.now()))
        else:
            print(" Bad Request for " + acc_no + "------" + str(datetime.datetime.now())) 
        # Returned Result for all cases
        return bank_pb2.FinanceDetails(Account_No = acc_no, Name = name, Balance = balance)   

    def Deposit(self,request,context):
        # Data Query Variable 
        from_acc = request.fromAccount
        to_acc = request.toAccount
        amt = request.amount
        # Transaction validation
        cursor0 = self.client.BankDB.Customers.find({"Account_No": to_acc})
        for x0 in cursor0:
            bal_to = x0["Balance"]
        cursor1 = self.client.BankDB.Customers.find({"Account_No": from_acc})
        for x1 in cursor1:
            bal_from = x1["Balance"]
        if (bal_from < amt):
            print("Insufficient balance in account " + from_acc + "to make a transfer" + "-------" + str(datetime.datetime.now()))
            return bank_pb2.UpdatedAccounts(fromAccount = from_acc, fromAccountBal= bal_from, toAccount = to_acc, toAccountBal = bal_to)
        else:
            bal_from -= amt
            bal_to += amt
            self.client.BankDB.Customers.update({'Account_No': from_acc}, {"$set" :{"Balance" : bal_from}})
            self.client.BankDB.Customers.update({'Account_No': to_acc}, {"$set" :{"Balance" : bal_to}})
            cursor01 = self.client.BankDB.Customers.find({"Account_No": to_acc})
            for x in cursor01:
                bal_to = x["Balance"]
            cursor11 = self.client.BankDB.Customers.find({"Account_No": from_acc})
            for y in cursor11:
                bal_from = y["Balance"]
            return bank_pb2.UpdatedAccounts(fromAccount = from_acc, fromAccountBal= bal_from, toAccount = to_acc, toAccountBal = bal_to)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_BankOpsServicer_to_server(BankServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()
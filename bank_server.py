from concurrent import futures
import grpc 
import time 
import bank_pb2
import bank_pb2_grpc
import data_parser
import logging 
import json
#Server Live time variable :P

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BankServicer(bank_pb2_grpc.BankOpsServicer):
    
    def __init__(self,*args, **kwargs):
        pass

    def QueryBalance(self,request,context):
        # Data Query Variable 
        acc_no = request.Account_No
        #Flag Variable
        val = None

        with open('bank_db.json') as database:
            for item in json.load(database):
                if(item["Account_No"] == acc_no):
                    print("Match Found for " + acc_no)
                    val = {"Account_No" : acc_no, "Name" : item["Name"], "Balance": item['Balance']}
                    break
                else:
                    print("Searching . . .")
        return bank_pb2.FinanceDetails(**val)
        
        # for item in self.finance_db:
        #     if item.Account_No == acc_no:
        #         val = item 
        # if val is None:
        #     print("Bad Request")
        #     return "Bad Request for " + str(acc_no)
        # else:
        #     return val
    
    def QueryDetails(self,request,context):
        acc_no = request.Account_No
        val = None
        for item in self.personal_db:
            if item.Account_No == acc_no:
                val = item 
        if val is None:
            print("Bad Request")
            return "Bad Request for " + str(acc_no)
        else:
            return val
    
    def Deposit(self,request,context):
        sender_acc = request.fromAccount
        print(sender_acc)
        recv_acc = request.toAccount
        print(recv_acc)
        with open('bank_db.json') as database:
            for item in json.load(database):
                if item["Account_No"] == sender_acc:
                    sender_account = item["Account_No"]
                    sender_balance = item["Balance"]
                    if sender_balance >= request.amount:
                        with open("bank_db.json") as database_2:    
                            for item2 in json.load(database_2):
                                if item2["Account_No"] == recv_acc:
                                    reciever_account = item2["Balance"]
                                    item2["Balance"] += request.amount
                                    item["Balance"] =- request.amount
                                    return bank_pb2.UpdatedAccounts(
                                        fromAccount = sender_account,
                                        fromAccountBal = item["Balance"],
                                        toAccount = reciever_account,
                                        toAccountBal = item2["Balance"])
            #           else:
            #                 print("Receiever account not found")
            #                 return "Account (Receiever)" + str(recv_acc) + " not Found"
            #     else:
            #         print("Insufficient balance at Sender")
            #         return "Insufficient balance with "  + str(sender_acc)
            # else:
            #     print("Sender account not found")
            #     return "Account (Sender)" + str(sender_acc) + " not Found"

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
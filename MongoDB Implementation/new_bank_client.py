import grpc 
import bank_pb2
import bank_pb2_grpc
import logging

# There might be chance that reflected output might not be synced with latest updates but on DB engine
# changes are observed instantly

def getQueryDetails(stub,message):
    query = bank_pb2.AccountNo(Account_No = message)
    return stub.QueryDetails(query)

def getFinanceDetails(stub,message):
    query = bank_pb2.AccountNo(Account_No = message)
    return stub.QueryBalance(query)

def doTransaction(stub,fromAcc,toAcc,amt):
    query = bank_pb2.TransferMessage(fromAccount = fromAcc, toAccount = toAcc, amount= amt)
    return stub.Deposit(query)

def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bank_pb2_grpc.BankOpsStub(channel)
        # Make your function calls here 

if __name__ == '__main__':
    logging.basicConfig()
    run()


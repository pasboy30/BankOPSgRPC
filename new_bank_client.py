import grpc 
import bank_pb2
import bank_pb2_grpc
import logging


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
    # TE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bank_pb2_grpc.BankOpsStub(channel)
        print(doTransaction(stub,"RBCD19191", "RBCD19192", 1000))


if __name__ == '__main__':
    logging.basicConfig()
    run()


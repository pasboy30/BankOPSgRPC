import grpc 
import bank_pb2
import bank_pb2_grpc

class BankClient(object):
    
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host,self.server_port))
        self.stub = bank_pb2_grpc.BankOpsStub(self.channel)
    
    def getQueryDetails(self,message):
        query = bank_pb2.AccountNo(Account_No = message)
        return self.stub.QueryDetails(query)
    
    def getFinanceDetails(self,message):
        query = bank_pb2.AccountNo(Account_No = message)
        return self.stub.QueryBalance(query)
    
    def doTransaction(self,message):
        acc_s = bank_pb2.TransferMessage(fromAccount = message)
        acc_r = bank_pb2.TransferMessage(toAccount  = message)
        amt = bank_pb2.TransferMessage(amount = message)
        return self.stub.Deposit(acc_s, acc_r,amt)

client = BankClient()
print(client.getFinanceDetails("RBCD19192"))

print(client.doTransaction("RBCD19191", "RBCD19192", 1000))

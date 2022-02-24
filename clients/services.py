import csv
from clients.models import Client
import os

class ClientService():
    
    def __init__(self,table_name):
        self.table_name = table_name

    def create_client(self,client):
        with open(self.table_name,mode='a') as f:
            writer=csv.DictWriter(f,fieldnames=Client.schema())
            writer.writerow(client.to_dict())

    def list_clients(self):
        with open(self.table_name,mode='r') as f:
            reader=csv.DictReader(f,fieldnames=Client.schema())

            return list(reader)

    def uptade_client(self,updated_client):
        clients = self.list_clients()

        updated_clients=[]

        for client in clients:
            if client['uid']== updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)
        
        self._save_to_disk(updated_clients)

    def _save_to_disk(self,updated_clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w',newline="") as f:
            writer = csv.DictWriter(f,fieldnames=Client.schema())
            writer.writerows(updated_clients)

        os.remove(self.table_name)
        os.rename(tmp_table_name,self.table_name)

    def delete_client(self,client_uid):
        clients = self.list_clients()

        for idx,client in enumerate(clients):
            if client['uid']==client_uid:
                clients.pop(idx)
        
        self._save_to_disk(clients)

        



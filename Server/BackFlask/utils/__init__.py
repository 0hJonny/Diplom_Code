from .minioClient import MinioClient


class MinioClientFactory:
    def __init__(self):
        self.clients = []

    def create_client(self):
        client = MinioClient()
        self.clients.append(client)
        return client

    def delete_clients(self):
        for client in self.clients:
            del client
        print("All MinioClients deleted")
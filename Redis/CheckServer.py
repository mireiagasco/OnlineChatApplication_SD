from NameServer import NameServer
from Client import Client

# Instantiate Name Server
name_server = NameServer()

# Register a client with the Name Server
name_server.register_client('user1', '192.168.1.100', 5000)

# Instantiate a client
client = Client('user2', '192.168.1.101', 6000)

# Register client with the Name Server
client.register_with_name_server()

# Get chat address from the Name Server
chat_address = client.get_chat_address('user1')
print(chat_address)

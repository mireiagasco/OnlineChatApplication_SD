import redis


class Client:
    def __init__(self, username, ip_address, port):
        self.username = username
        self.ip_address = ip_address
        self.port = port
        self.redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    def register_with_name_server(self):
        # Register client's IP address and port with the Name Server
        self.redis_conn.hset(self.username, 'ip_address', self.ip_address)
        self.redis_conn.hset(self.username, 'port', self.port)

    def get_chat_address(self, chat_id):
        # Request chat address from the Name Server
        connection_info = self.redis_conn.hgetall(chat_id)
        return connection_info

import redis


class NameServer:
    _instance = None  # Singleton instance variable

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    def register_user(self, username, chat_id, ip_address, port):
        # Store client's IP address, port, and user ID associated with chat ID in Redis
        self.redis_conn.hset(chat_id, 'ip_address', ip_address)
        self.redis_conn.hset(chat_id, 'port', port)
        self.redis_conn.hset(chat_id, 'chat_id', chat_id)
        self.redis_conn.hset(chat_id, 'username', username)

    def remove_user(self, user_id):
        self.redis_conn.delete(user_id)

    def get_connection_params(self, chat_id):
        # Retrieve connection parameters associated with chat ID from Redis
        return self.redis_conn.hgetall(chat_id)

    def get_connected_clients(self):
        # Retrieve all connected clients from Redis
        connected_clients = {}
        for chat_id in self.redis_conn.scan_iter():
            connection_params = self.redis_conn.hgetall(chat_id)
            connected_clients[chat_id] = {
                'ip_address': connection_params[b'ip_address'].decode(),
                'port': int(connection_params[b'port']),
                'username': connection_params[b'username'].decode()
            }
        return connected_clients


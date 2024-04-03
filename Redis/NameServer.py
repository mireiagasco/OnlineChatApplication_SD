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

    def register_client(self, chat_id, ip_address, port, user_id):
        # Store client's IP address, port, and user ID associated with chat ID in Redis
        self.redis_conn.hmset(chat_id, {'ip_address': ip_address, 'port': port, 'user_id': user_id})

    def get_connection_params(self, chat_id):
        # Retrieve connection parameters associated with chat ID from Redis
        connection_info = self.redis_conn.hgetall(chat_id)
        return connection_info
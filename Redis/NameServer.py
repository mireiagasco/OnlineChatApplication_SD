import redis


class NameServer:
    def __init__(self):
        self.redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    def register_client(self, username, ip_address, port):
        # Store client's IP address and port associated with username in Redis
        self.redis_conn.hset(username, 'ip_address', ip_address)
        self.redis_conn.hset(username, 'port', port)

    def get_connection_params(self, chat_id):
        # Retrieve connection parameters associated with chat_id from Redis
        connection_info = self.redis_conn.hgetall(chat_id)
        return connection_info

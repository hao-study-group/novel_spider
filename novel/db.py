from redis import Redis


class DB_REDIS():
    def __init__(self):
        self.conn = Redis(host='127.0.0.1', port=6379)

    def insert(self, md5):
        xx = self.conn.sadd('biquge', md5)
        return xx

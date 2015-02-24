class Connection:
    def __init__(self, host, auth, port=8000, management_port=8002):
        self.host = host
        self.port = port
        self.management_port = management_port
        self.auth = auth
class Chain:
    def __init__(self, chain):
        self.chain = chain

    def handle_msg(self, data):
        self.chain.run(data)

import interactions
from configs import sections
class Extension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

   


def setup(client: interactions.Client):
    Extension(client)
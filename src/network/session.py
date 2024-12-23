import gi
gi.require_version('Soup', '3.0')

from gi.repository import Soup, GObject

class MutinySession(GObject.Object):
    websocket_url = None
    api_url = None
    soup_session = None
    current_channel = None
    current_server = None
    user_token = None

    def __init__(self, websocket_url: str, api_url: str, user_token: str):
        super().__init__()

        self.user_token = user_token
        self.websocket_url = websocket_url
        self.api_url = api_url
        self.soup_session = Soup.Session()
        

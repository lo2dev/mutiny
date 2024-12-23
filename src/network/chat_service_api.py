import gi, json
gi.require_version('Soup', '3.0')

from gi.repository import Soup, GLib, GObject

class ChatServiceApi:
    session = None
    soup_session = None
    # user_auth = None

    def __init__(self, session):
        super().__init__()

        self.session = session
        self.soup_session = session.soup_session

    def request(self, request_type: str, url_endpoint: str, callback, request_body = None) -> None:

        def on_receive_bytes(session, result, message) -> None:
            if not callback:
                return

            if message.get_status() != Soup.Status.OK:
                print(f"HTTP Status {message.get_status()}")
                return

            bytes = session.send_and_read_finish(result)
            decoded_text = bytes.unref_to_array().decode("utf-8")
            callback(json.loads(decoded_text))

        soup_message = Soup.Message.new(request_type, f"https://{self.session.api_url}{url_endpoint}")
        soup_message.get_request_headers().append("x-session-token", self.session.user_token)

        if request_body:
            soup_message.set_request_body_from_bytes(None, request_body)

        self.session.soup_session.send_and_read_async(
            soup_message,
            GLib.PRIORITY_DEFAULT,
            None,
            on_receive_bytes,
            soup_message
        )


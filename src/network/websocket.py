import gi, json
gi.require_version('Soup', '3.0')

from gi.repository import Soup, GLib, GObject

class ClientWebsocket(GObject.Object):
    websocket_connection = None
    # session = None


    def __init__(self, session):
        super().__init__()

        # self.session = session
        soup_message = Soup.Message.new(
            "GET",
            f"wss://{session.websocket_url}/?token={session.user_token}"
        )
        session.soup_session.websocket_connect_async(
            soup_message,
            "Mutiny",
            [],
            GLib.PRIORITY_DEFAULT,
            None,
            self.on_websocket_connected,
            None
        )


    def on_websocket_connected(self, obj, res, data) -> None:
        self.websocket_connection = obj.websocket_connect_finish(res)
        self.websocket_connection.props.keepalive_interval = 15

        self.websocket_connection.connect("message", self.proccess_websocket_message)
        self.websocket_connection.connect("error", self.on_error)
        self.websocket_connection.connect("closed", self.on_closed)


    @GObject.Signal(flags=GObject.SignalFlags.RUN_FIRST, arg_types=(str,))
    def on_websocket_message(self, ws_message):
        return ws_message


    def proccess_websocket_message(self, _self, data_type, message):
        if data_type != Soup.WebsocketDataType.TEXT:
            return

        decoded_ws_message = message.unref_to_array().decode("utf-8")
        self.emit('on_websocket_message', decoded_ws_message)


    def on_open():
        print("open")


    def on_closed(self, _self):
        print("closed")


    def on_error(self, _self, err):
        print("error")
        print(err, file=sys.stderr)




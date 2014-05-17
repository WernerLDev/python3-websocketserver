"""
 Copyright 2014 Werner Langenhuisen

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

# -*- coding: utf-8 -*-

import threading
from websockets.websocket import Websocket


class WebsocketThread(threading.Thread):

    connected = True
    client = 0
    channel = 0
    details = 0
    server = 0
    websocket = Websocket()

    def __init__(self, channel, details, client, server):
        super(WebsocketThread, self).__init__()
        self.channel = channel
        self.details = details
        self.client = client
        self.server = server

    def run(self):
        self.connected = True

        msg = "Server: Device #{0} connected at {1}"
        print((msg.format(self.client.clientid, self.details[0])))

        self.websocket.do_handshake(self.channel)

        while self.connected:
            self.interact(self.channel)

    def stop(self):
        self.connected = False
        self.channel.close()

    def interact(self, channel):
        encodeddata = channel.recv(8192)
        data = self.websocket.decode_data(encodeddata)

        if data[2] == 8:
            msg = "Client #{0} closed connecting, bye!"
            print((msg.format(self.client.clientid)))
            self.channel.close()
            self.connected = False
        else:
            msg = "Received data from client #{0} saying: {1}"
            print((msg.format(self.client.clientid, data[0])))

            if data[0] == "hallo":
                response = self.websocket.encode_data(True, "hey browser")
                channel.send(response)
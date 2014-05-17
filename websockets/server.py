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
import socket
from websockets.wsclient import Wsclient
from websockets.wsthread import WebsocketThread


class SocketServer():

    port = 0
    clientid = 0
    clients = []
    threads = []
    socketConn = 0
    connected = False

    def __init__(self, address, port):
        self.port = port
        self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketConn.bind(("", port))
        self.socketConn.listen(1)

    def stopListening(self):
        self.connected = False

        for thread in self.threads:
            thread.stop()

        for client in self.clients:
            client.socket.close()

        self.socketConn.close()
        print("Websocket server stopped listening")

    def startListening(self):
        self.connected = True

        print(("Websocket server started on port {0}".format(self.port)))

        while self.connected:
            channel, details = self.socketConn.accept()

            client = Wsclient(channel, self.clientid)
            self.clients.append(client)
            self.clientid = self.clientid + 1

            thread = WebsocketThread(channel, details, client, self)
            thread.start()
            self.threads.append(thread)
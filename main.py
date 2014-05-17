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
from websockets.server import SocketServer
import signal
import sys


if __name__ == "__main__":
    server = SocketServer("localhost", 1234)

    def signalHandler(s, frame):
        if s == signal.SIGINT:
            server.stopListening()
            print('Goodbye')
            sys.exit(0)

    signal.signal(signal.SIGINT, signalHandler)

    server.startListening()
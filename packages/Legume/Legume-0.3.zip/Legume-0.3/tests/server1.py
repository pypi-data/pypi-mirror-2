# legume. Copyright 2009 Dale Reidy. All rights reserved. See LICENSE for details.

import time
import sys
sys.path.append('..')
import legume

PORT = 14822

server = legume.udp.Server()
server.listen(('', PORT))

while True:
    server.update()
    time.sleep(0.001)
import p2p_framework as p2p
import socket

peer1 = p2p.BTPeer(0, 9000, 0, socket.gethostname())
peer2 = p2p.BTPeer(1, 9000, 0, socket.gethostname())
peer1.mainloop()
peer2.mainloop()

pconnect = p2p.BTPeerConnection(0, socket.gethostname(), 9000)
pconnect.senddata(int, 902)
pconnect.recvdata()



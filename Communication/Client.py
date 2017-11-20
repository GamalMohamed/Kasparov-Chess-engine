import socket
from struct import *
from time import *


class chess_client():

    def __init__(self,serv,port):
        self.server = serv
        self.port = port
        self.hsocket = None

    def __del__(self):
        self.hsocket.close()

    # connect to server and intialize socket handle
    def srvconnect(self):
        s = socket.socket()
        s.settimeout(None)
        s.connect((self.server, self.port))
        self.hsocket = s

    # wait for mov from other palyer
    # return type : list [type of mov , mov data]
    # type of move :
    #     0 => single mov   , mov data (tuple) => (piece , dst)
    #     1 => state string , mov data (string)=> board string state
    def waitformov(self):
        try :
            result = []
            type = self.hsocket.recv(4)
            type, = unpack('i', type)

            # single move
            if type == 0:
                move = self.hsocket.recv(8)
                piece, dst = unpack('ii', move)
                result = [0, (piece, dst)]

            # string
            elif type == 1:
                size = self.hsocket.recv(4)
                sz, = unpack('i', size)
                board_state = self.hsocket.recv(sz)
                fmt = str(sz) + 's'
                state, = unpack(fmt, board_state)
                result = [1, state]

            return result
        except Exception ,e :
            print e

    # send single move to the server
    # return  : 1 if acked  0 if failed
    # ex: send_move(15 , 12)
    def send_mov(self, piece, dst):
        print '[+] sending single move : piece = %d  | dst = %d' % (piece, dst)
        data = (piece, dst)
        self.hsocket.send(pack('iii', 2, *data))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1
        return 0

    # send win message to the server to end the game
    # the server will end the game when it receives that message
    # return 1 if acked :  0 otherwise
    def send_win(self):
        print '[+] Congratulations ...'
        self.hsocket.send(pack('i', 3))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1
        return 0

    # Probe the existence of the other player
    # return  : 1 if other player connected  , otherwise blocks
    def waitForPlayer(self):
        while 1:
            sleep(1)
            print 'probing ...'
            self.hsocket.send(pack('i', 4))
            data = self.hsocket.recv(4)
            result, = unpack('i', data)
            if result == 1: return 1

    # send state board string to server
    # return  : 1 if acked  0 if failed
    # ex: send_state('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq- 0 1')
    def send_state(self, state):
        print '[+] sending state : %s' % state
        sz = len(state)
        opcode = 1
        fmt = 'ii ' + str(sz) + 's'
        self.hsocket.send(pack(fmt, opcode, sz, state))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1
        return 0

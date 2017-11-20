
import socket
import threading
from struct import *
import binascii
import time

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))


        self.opcodes = [None  , 'board state string','single move','win message','check probe']
        self.players = [False ,False]

        self.hsockets = [None , None]

        # start timestamp for each player waiting for it's move
        self.timers = [0 ,0]
        # total time used for each player
        self.total_time = [0 ,0]


        self.game = False
        self.first_play = True


    def listen(self):
        self.sock.listen(5)
        while 1:
            if  not self.players[0] or not self.players[1]:
                print 'waiting ... '

                client, address = self.sock.accept()
                client.settimeout(999999)

                if self.players[0] == False :
                    print '==================='
                    print 'player 1 registered'
                    print '==================='
                    self.players[0] = True
                    self.hsockets[0] = client

                elif self.players[0] == True and self.players[1] == False:
                    print '==================='
                    print 'player 2 registered'
                    print '==================='
                    self.players[1] = True
                    self.game = True
                    self.hsockets[1] = client

                x = None
                if self.players[0] : x = 0
                if self.players[1] : x = 1

                threading.Thread(target = self.listenToClient,args = (x,)).start()


    def listenToClient(self ,player):
        # opcode size
        size = 4

        if player == 0 : print '[player 1 thread]'
        elif player == 1 : print '[player 2 thread]'

        sock = self.hsockets[player]

        try :
            while 1:
                    data = sock.recv(size)
                    opcode , = unpack('i',data)

                    # Start counting time base as soon as the two players are already registered
                    if self.first_play and self.players[0] == True and self.players[1] == True:
                        self.timers[1] = time.time();
                        self.timers[0] = time.time()
                        self.first_play = False
                        print '[Server] starting timers'

                    # Debug Msg
                    # print '[Server] Received opcode [%s] from player %d' %(self.opcodes[opcode],player+1)

                    # board state string == ' Size | S-T-R-I-N-G'
                    if opcode == 1 :

                        str_sz = sock.recv(size)
                        sz , = unpack('i', str_sz)
                        board_state = sock.recv(sz)

                        fmt = str(sz)+'s'
                        state , = unpack(fmt , board_state)

                        print '[Player%d] reccived state string : %s' %(player+1,state)

                        # Send Ack
                        sock.send(pack('i',1))

                        # Start time for other player
                        self.start_timer((player + 1) % 2)
                        # stop my timer
                        self.stop_timer(player)

                        try:
                            Othersock = self.hsockets[(player + 1) % 2]
                            Othersock.sendall(pack('i', 1))
                            relay = ''
                            relay += str_sz
                            relay += board_state
                            Othersock.sendall(relay)

                        except Exception,e:
                            # any exception for the other palyer thread should not hang the current thread
                            print '[-] failed to send string state to player %d' % ((player + 1)%2 + 1) # just show the other player num from it's index
                            print e
                            continue

                    # single move
                    elif opcode == 2 :

                        data = sock.recv(8)
                        piece , dst  = unpack('ii', data)
                        print '[Player%d] Recieved move : piece = %d  dst = %d'%(player+1 ,piece , dst)

                        # Send Ack
                        sock.send(pack('i', 1))

                        # Start time for other player
                        self.start_timer((player + 1) % 2)
                        # stop my timer
                        self.stop_timer(player)

                        try :
                            Othersock = self.hsockets[(player + 1) % 2]
                            Othersock.sendall(pack('i', 0))
                            Othersock.sendall(data)
                        except Exception,e:
                            # any exception for the other palyer thread should not hang the current thread
                            print '[-] failed to send single move to player %d'% ((player + 1)%2 + 1) # just show the other player num from it's index
                            print e
                            continue

                    # win message
                    elif opcode == 3:
                        print '[++] Player %d won the game' %(player+1)

                        # Send Ack
                        sock.send(pack('i', 1))
                        raw_input('Done')
                        exit(0)

                    # check other player : each client is responsible for checking the availability of the other player
                    elif opcode == 4:
                        if self.players[(player+1)%2] == True:
                            x=  pack('i',1)
                        else :
                            x = pack('i', 0)
                        sock.sendall(x)


        except Exception ,e:
            print e
        finally:
            # if any thread killed , disconnect it's corresponding player
            print '************************************************'
            print '[-] closing connection for player %d' %(player+1)
            print '************************************************'

            sock.close()
            self.players[player] = False
            self.hsockets[player] = None


    def start_timer(self,player):
        self.timers[player] = time.time()

    def stop_timer(self,player):
        current = time.time()
        c = current - self.timers[player]
        self.total_time[player] += int(c)

        print '[Player%d_Timing] Move took : %d sec , total time elasped : %d sec' %(player+1 ,c ,self.total_time[player])
        max = 900 # 15 minutes
        if int(self.total_time[player]) >= max :
            print '[Timing] Player %d lose => timeout !!' %player

if __name__ == "__main__":
    ThreadedServer('127.0.0.1',7777).listen()

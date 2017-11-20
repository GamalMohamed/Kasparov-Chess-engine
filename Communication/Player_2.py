from Client import *

client = chess_client('127.0.0.1', 7777)
player_no = client.srvconnect()

if client.waitForPlayer() == 1:
    try:
        print 'other Player connected'
        i = 0
        while 1:

            mov = client.waitformov()
            print '[+] Receiving move :' + str(mov)

            sleep(5)

            client.send_mov(i, i)
            print '[+] Sending move : (%d ,%d)' %(i,i)

            i += 1

    except Exception, e:
        print e

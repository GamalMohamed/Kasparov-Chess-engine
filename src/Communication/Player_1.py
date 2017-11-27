from Client import *


# create client object
client = chess_client('127.0.0.1', 7777)

# connect to sever
client.srvconnect()

# wait for other player to connect ; blocks
if client.waitForPlayer() == 1:
    try:
        print 'other Player connected'
        i=555
        while 1 :

            sleep(3)

            # send move to the other player
            client.send_mov(i, i)
            print '[+] Sending move : (%d ,%d)' % (i, i)

            # wait for the move from the other player ; blocks
            mov = client.waitformov()
            print '[+] Receiving move :' + str(mov)

            i+=1


    except Exception, e:
        print e


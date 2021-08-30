
import socket

if __name__ == "__main__":

	HOST = '172.16.180.10'
	PORT = 6789

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))
	print 'Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.'

	message = 'Hello, world'
	print 'Envoi de :' + message
	n = client.send(message)
	if (n != len(message)):
    print 'Erreur envoi.'
	else:
	  print 'Envoi ok.'

	print 'Reception...'
	donnees = client.recv(1024)
	print 'Recu :', donnees

	print 'Deconnexion.'
	client.close()
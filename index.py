from socket import *
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = input("Input lowercase sentence (or 'q' to quit): ");

while (message != "q"):
    clientSocket.sendto (message.encode(),(serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(serverAddress)
    print(modifiedMessage.decode())
    message = input("Input lowercase sentence (or 'q' to quit): ");
clientSocket.close()
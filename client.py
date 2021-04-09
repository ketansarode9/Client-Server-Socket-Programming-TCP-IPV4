import socket		 	 # Import socket module
import sys
import ipaddress

try:
     
    try:
        host = str(ipaddress.ip_address(sys.argv[1]))     # Reading IP Address
        port = int(sys.argv[2])  
    except IndexError:
          print("Wrong arguments - Terminating the Program")
          exit(1)                      # Reading port number

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # connect to server on local computer
    try:
        s.connect((host,port))
    except ConnectionRefusedError:
        print("Server down or busy")
        exit(1)
    

    print("The IP address of the server is:", host)
    print("The port number of the server is:", port)

    while(True):
        equ=input("Please give me your equation (Ex: 2+2) or Q to quit: ")
        s.send(equ.encode())
        result = s.recv(1024).decode()
        if result == "Quit":
            print("Closing client connection, goodbye")
            break
        elif result == "ZeroDiv":
            print("You can't divide by 0, try again")
        elif result == "MathError":
            print("There is an error with your math, try again")
        elif result == "SyntaxError":
            print("There is a syntax error, please try again")
        elif result == "NameError":
            print("You did not enter an equation, try again")
        else:
            print("The answer is:", result)
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close() 				 # Close the socket when done

except (IndexError, ValueError):
    print("You did not specify an IP address and port number")

except:
    print("INVALID - NO PROPER CONNECTION ")




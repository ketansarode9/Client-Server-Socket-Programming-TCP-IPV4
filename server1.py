import socket		 	 # Import socket module
import sys


def binding(s):
     try:
          s.bind((host, port))
     except socket.error as e:
          print(str(e))
     print("socket binded to port", port)

def listing(s,x):
     # put the socket into listening mode
     s.listen(x)
     print("socket is listening")

def get_equation(c):
     while True:
          try:
               equation=c.recv(1024).decode()
               if not equation:
                    print('Bye')
                    break
               if equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
                    c.send("Quit".encode())
                    break
               else:
                    print("You gave me the equation:", equation)
                    result = eval(equation)

               c.send(str(result).encode())

          except (ZeroDivisionError):
               c.send("ZeroDiv".encode())
          except (ArithmeticError):
               c.send("MathError".encode())
          except (SyntaxError):
               c.send("SyntaxError".encode())
          except (NameError):
               c.send("NameError".encode())

     c.close() 			# Close the connection.



if __name__ == '__main__':
     try:
          host = socket.gethostbyname("localhost")                    # Get local machine name
          port = int(sys.argv[1])
     except IndexError:
          print("Wrong arguments - Terminating the Program")
          exit(1)
     
     try:
          # a forever loop until client wants to exit
          while True:
               s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket Creation
               s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for reusaiblity of same port otherwise give exception
               binding(s)  #binding to the respective port 
               listing(s,5)  #put the socket into listening mode
               # establish connection with client
               c, addr = s.accept() #conn-c
               s.close()
               print('Connected to :', addr[0], ':', addr[1])
               get_equation (c)

     except KeyboardInterrupt:
          print('\n Closing the server connection ....', end = '')
          c.close()
          s.close()

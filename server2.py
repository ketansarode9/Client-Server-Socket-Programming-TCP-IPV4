import socket
import os
import sys
from _thread import *
import threading


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




# thread function
def client_thread(c):
     while True:
          try:
               equation=c.recv(1024).decode()

               if not equation:
                    print('Bye closing...')
                    break


               if equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
                    c.sendall("Quit".encode())
                    break
               else:
                    print("You gave me the equation:", equation)
                    result = eval(equation)

               c.sendall(str(result).encode())

          except (ZeroDivisionError):
               c.sendall("ZeroDiv".encode())
          except (ArithmeticError):
               c.sendall("MathError".encode())
          except (SyntaxError):
               c.sendall("SyntaxError".encode())
          except (NameError):
               c.sendall("NameError".encode())

     c.close() 			# Close the connection.

def client_connection(s):
     # establish connection with client
     c, addr = s.accept()
     print('Connected to :', addr[0], ':', addr[1])
     start_new_thread(client_thread, (c, ))



if __name__ == '__main__':
     
     try:
          host = socket.gethostbyname("localhost")                    # Get local machine name
          port = int(sys.argv[1])
     except IndexError:
          print("Wrong arguments - Terminating the Program")
          exit(1)
     ThreadCount = 0 #for taking the count of respective threads

     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket Creation
     binding(s)  #binding to the respective port 
     listing(s,5)  #put the socket into listening mode
  

     # forever loop until client wants to exit
     try:
          while True:
                    client_connection(s)
                    ThreadCount += 1
                    print('Thread Number: ' + str(ThreadCount))
          
          print('\n Closing the socket ...' , end='')
          s.close()
     except KeyboardInterrupt:
          print('\n Closing the server connection ....', end = '')
          s.close()
     

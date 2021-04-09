import socket
import os
import sys
from _thread import *
import threading
import select
import queue

try:

          host = socket.gethostbyname("localhost")                    # Get local machine name
          port = int(sys.argv[1])
except IndexError:
          print("Wrong arguments - Terminating the Program")
          exit(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP/IP Socket Creation

try:
    server.bind((host, port)) # Bind the socket to the port
except socket.error as e:
    print(e)

print("socket binded to port", port)

# put the socket into listening mode
server.listen(5)
print("socket is listening")

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}



while inputs:
    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,outputs,inputs)


    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            print('connection from', client_address,file=sys.stderr)
            connection.setblocking(0)
            inputs.append(connection)
            # Give the connection a queue for equation
            # we want to send
            message_queues[connection] = queue.Queue()
        else:
            equation=s.recv(1024).decode()
            if not equation or equation == "Q" or equation == "q" or equation == "Quit" or equation == "quit" or equation == "quit()":
                # Interpret empty result as closed connection
                print('  closing', client_address,file=sys.stderr)
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                str = "Quit"
                s.send(str.encode())
                s.close()

                # Remove message queue
                del message_queues[s]
                
            else:
                try:
                    result = eval(equation)
                    message_queues[s].put(result)
                    if s not in outputs:
                        outputs.append(s)
                except (ZeroDivisionError):
                    s.sendall("ZeroDiv".encode())
                except (ArithmeticError):
                    s.sendall("MathError".encode())
                except (SyntaxError):
                    s.sendall("SyntaxError".encode())
                except (NameError):
                    s.sendall("NameError".encode())
    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            # No messages waiting so stop checking
            # for writability.
            print('  ', s.getpeername(), 'queue empty',file=sys.stderr)
            outputs.remove(s)
        else:
            print('  sending {!r} to {}'.format(next_msg,s.getpeername()),file=sys.stderr)
            s.send(str(next_msg).encode())

    # Handle "exceptional conditions"
    for s in exceptional:
        print('exception condition on', s.getpeername(),file=sys.stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]

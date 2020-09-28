from multiprocessing import Process, Pipe
from os import getpid

def event(pid, counter):
    counter[pid] += 1
    print('Some event in process \t{}\t{}'.format(pid, counter))
    return counter

def send(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from \t{}\t{}'.format(pid,counter))
    return counter

def recv(pipe, pid, counter):
    counter[pid] += 1
    message, timestamp = pipe.recv()
    # update timestamp
    for id  in range(len(counter)):
        counter[id] = max(timestamp[id], counter[id])
    print('Message received at \t{}\t{}'.format(pid, counter))
    return counter

def pr1(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send(pipe12, pid, counter)
    counter = send(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv(pipe12, pid, counter)
    counter  = event(pid, counter)
    counter  = event(pid, counter)
    counter = recv(pipe12, pid, counter)
    print(pid, counter)


def pr2(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = recv(pipe21, pid, counter)
    counter = recv(pipe21, pid, counter)
    counter = send(pipe21, pid, counter)
    counter = recv(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send(pipe21, pid, counter)
    counter = send(pipe23, pid, counter)
    counter = send(pipe23, pid, counter)
    print(pid, counter)


def pr3(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = send(pipe32, pid, counter)
    counter = recv(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv(pipe32, pid, counter)
    print(pid, counter)

if __name__ == '__main__':
    p12, p21 = Pipe()
    p23, p32 = Pipe()

    process1 = Process(target=pr1, 
                       args=(p12,))
    process2 = Process(target=pr2, 
                       args=(p21, p23))
    process3 = Process(target=pr3, 
                       args=(p32,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

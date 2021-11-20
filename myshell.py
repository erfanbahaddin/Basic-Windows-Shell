import os
import re
import signal

MAX_BG_PROCESSES = 5
children = []


while True:
    command = input("shell> ")
    try:
        if command == "exit":
            break
        elif command == "pwd":
            print(os.getcwd())
        elif command.startswith("cd"):
            cd_split = command.split(" ", 1)
            if command == "cd":
                os.chdir("/home/erfan")
            else:
                os.chdir(cd_split[1])
        elif command == "bglist":
            for job in children:
                print(children.index(job)+1, end=" ")
                print(job)
            print("Total Background jobs: %d" % len(children))
        elif command.startswith("bgkill"):
            a = command.split()
            try:
                os.kill(int(a[1]), signal.SIGTERM)
                children.remove(int(a[1]))
            except:
                print("Invalid process")
        elif command.startswith("bgstop"):
            a = command.split()
            try:
                os.kill(int(a[1]), signal.SIGSTOP)
            except:
                print("Invalid process")
        elif command.startswith("bgstart"):
            a = command.split()
            try:
                os.kill(int(a[1]), signal.SIGCONT)
            except:
                print("Invalid process")
        else:
            regexp1 = re.compile('".*"')
            if regexp1.search(command):
                first_quote_index = command.index('"')
                second_quote_index = command.index('"', first_quote_index + 1, len(command))
                x = command[0:first_quote_index].split()
                x.append(command[first_quote_index:second_quote_index + 1])
                x.extend(command[second_quote_index + 1:len(command)].split())
            else:
                x = command.split()
            if x[0] == "bg":
                if len(children) < MAX_BG_PROCESSES:
                    pid = os.fork()
                    if pid > 0:
                        children.append(pid)
                    else:
                        os.execvp(x[1], x[1:])
                        os.kill(os.getpid(), signal.SIGKILL)
                        children.remove(os.getpid())
            else:
                pid = os.fork()
                if pid > 0:
                    os.wait()
                else:
                    os.execvp(x[0], x)
    except:
        try:
            y = eval(command)
            if y:
                print(y)
        except:
            try:
                exec(command)
            except Exception as e:
                print("error:", e)

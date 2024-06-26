import argparse
import os
import re
import socket
import socketserver
import sys
import time
import threading
def helpers(host, port, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(request.encode())
    response = s.recv(1024)
    s.close()
    return response.decode()


    


def dispatch_tests(server, commit_id):
    while True:
        print("trying to dispatch to runners")
        for runner in server.runners:
            response = helpers(runner["host"],
                               int(runner["port"]),
                               "runtest:%s" %commit_id)
            if response == "OK":
                print("Adding id %s"% commit_id)
                server.dispatched_commits[commit_id] = runner
                if commit_id in server.pending_commits:
                    server.pending_commits.remove(commit_id)
                return
        time.sleep(3)

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    runners = [] #keep track of test runner pool
    dead = False # indicate to other thread that we are no longer running
    dispatched_commits = {} #keep track of commits we dispatched
    pending_commits = [] #keeps track of commits we have yet to dispatch

class DispatcherHandler(socketserver.BaseRequestHandler):
    """
    The Requesthandler class for our dispatcher.
    This will dispatch test runners against the incoming commit
    and handle their requests and test results 
    """

    command_re = re.compile(r"(\w+)(:.+)*")
    BUF_SIZE = 1024
    def handle(self):
        self.data = self.request.recv(self.BUF_SIZE).strip()
        command_groups = self.command_re.match(self.data.decode('utf-8'))
        if not command_groups:
            self.request.sendall(b'Invalid command')
            return
        command = command_groups.group(1)
        if command =="status":
            print("in status")
            self.request.sendall(b'OK')
        elif command == "register":
            print("register")
            address = command_groups.group(2)
            host, port = re.findall(r":(\w*)",address)
            runner = {"host": host, "port":port}
            self.server.runners.append(runner)
            self.request.sendall(b'OK')
        elif command =="dispatch":
            print("going to dispatch")
            commit_id = command_groups.group(2)[1:]
            if not self.server.runners:
                self.request.sendall(b'no runners are registered')
            else:
                self.request.sendall(b'OK')
                dispatch_tests(self.server, commit_id)
        elif command == "results":
            print("got test results")
            results = command_groups.group(2)[1:]
            results = results.split(":")
            commit_id = results[0]
            length_msg = int(results[1])
            remaining_buffer = self.BUF_SIZE - \
                (len(command) + len(commit_id) + len(results[1]) + 3)
            if length_msg > remaining_buffer:
                self.data += self.request.recv(length_msg - remaining_buffer).strip()
            del self.server.dispatched_commits[commit_id]
            if not os.path.exists("test_results"):
                os.makedirs("test_results")
            with open("test_results/%s"% commit_id, "w") as f:
                decoded_data = self.data.decode('utf-8')
                data = decoded_data.split(":")[3:]
                data = "\n".join(data)
                f.write(data)
            self.request.sendall(b'OK')

def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        help="dispatcher's host, by default it uses localhost",
                        default="localhost",
                        action="store")
    parser.add_argument("--port",
                        help="dispatcher's port, by default it uses 8888",
                        default=8888,
                        action="store")
    args = parser.parse_args()
    server = ThreadingTCPServer((args.host, int(args.port)), DispatcherHandler)
    print("serving on %s:%s" % (args.host, int(args.port)))
    

    def runner_checker(server):
        def manage_commit_lists(runner):
            for commit, assigned_runner in server.dispatched_commits.items():
                if assigned_runner == runner:
                    del server.dispatched_commits[commit]
                    server.pending_commits.append(commit)
                    break
            server.runners.remove(runner)
        while not server.dead:
            time.sleep(2)
            for runner in server.runners:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    response = helpers(runner["host"],
                                       int(runner["port"]),
                                       "ping")
                    if response != "pong":
                        print("Removing runner %s"%runner)
                        manage_commit_lists(runner)
                except socket.error as e:
                    manage_commit_lists(runner)

    def redistribute(server):
        while not server.dead:
            for commit in server.pending_commits:
                print("running redistribute")
                print(server.pending_commits)
                dispatch_tests(server, commit)
                time.sleep(5)

    runner_heartbeat = threading.Thread(target=runner_checker, args=(server,))
    redistributor = threading.Thread(target=redistribute, args=(server,))

    try:
        runner_heartbeat.start()
        redistributor.start()
        server.serve_forever()
    except(KeyboardInterrupt, Exception):
        server.dead = True
        runner_heartbeat.join()
        redistributor.join()

if __name__ == "__main__":
    serve()

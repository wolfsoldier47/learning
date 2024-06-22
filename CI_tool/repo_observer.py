import argparse
import os
import re
import socket
import socketserver
import subprocess
import sys
import time
def helpers(host, port, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(request.encode())
    response = s.recv(1024)
    s.close()
    return response.decode()

def poll():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatcher-server",
                        help="dispatch host:port, " \
                            "by default it uses localhost:8888",
                            default="localhost:8888",
                            action="store")
    parser.add_argument("repo", metavar="REPO", type=str,
                        help="path to the repository this will observe")
    args = parser.parse_args()
    dispatcher_host, dispatcher_port = args.dispatcher_server.split(":")
    while True:
        try:
            subprocess.check_output(["./update_repo.sh", args.repo])
        except subprocess.CalledProcessError as e:
            raise Exception("could not update and check repo. Reasons: %s" % e.output)
        
        if os.path.isfile(".commit_id"):
            try:
                response = helpers(dispatcher_host,
                                    int(dispatcher_port),
                                    "status")
            except socket.socket as e:
                raise Exception("Cloud not communicate with disaptcher server: %s" % e)
            
            if response == "OK":
                commit = ""
                with open(".commit_id","r") as f:
                    commit = f.readline()
                response = helpers(dispatcher_host,
                                    int(dispatcher_port),
                                    "status")
                
                if response != "OK":
                    raise Exception("Could not dispatch the test: %s"%response)
                print("dispatched!")
            else:
                raise Exception("could not dispatch the test: %s"%response)
            
        time.sleep(5)
if __name__ == "__main__":
    poll()
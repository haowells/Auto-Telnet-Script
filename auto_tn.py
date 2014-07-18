#!/usr/bin/env python
import os
import sys
import telnetlib
import multiprocessing as mp

	
def tnOne(host):

    oldStdout = sys.stdout
    sys.stdout = open(host,"w")

    t = telnetlib.Telnet()
    t.open(host)

    t.write("\n")

    response = t.read_until(login_prompt, 10)
    if login_prompt in response:
        print response + str(username)
    else:
        return 0
    t.write("%s\n" % username)

    response = t.read_until(password_prompt, 10)
    if password_prompt in response:
        print password_prompt + str(passwd)
    else:
        return 0
    t.write("%s\n" % passwd)

    response = t.read_until(command_prompt, 600)
    if command_prompt not in response:
        return 0
    else:
        print command_prompt

    for cmd in cmd_list:
        t.write("%s\n" % cmd)
        response = t.read_until(command_prompt, 600)
        if command_prompt not in response:
            return 0
        print response
            
    t.close()

    sys.stdout = oldStdout

    return 1



basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
import getopt
optlist,left = getopt.getopt(sys.argv[1:], 'h:l:f:c:u:p:') 
usage = """
usage: %s [-h host] [-l hostfile] [-f cmdfile] [-c "command"] [-u username] [-p passowrd]
       -c command
       -f command file
       -h single hostname
   -l hostname file
       -u username
       -p password
Example: %s -c "echo $HOME" -u %s -p password
""" % (basename, basename, "root")

if len(sys.argv) < 2:
    print usage
    sys.exit(1)

host_list = [ ]
cmd_list = [ ]
for opt, optarg in optlist:
    if opt == '-f':
        for r in open(optarg):
            r = r.strip()
            if r:
                cmd_list.append(r)
    elif opt == '-c':
        command = optarg
        if command[0] == '"' and command[-1] == '"':
            command = command[1:-1]
        cmd_list.append(command)
    elif opt == '-h':
        host_list = [optarg]
    elif opt == '-l':
        for h in open(optarg):
	    h = h.strip()
            if h:
	        host_list.append(h)
    elif opt == '-u':
        username = optarg
    elif opt == '-p':
        passwd = optarg

timeout = 600
login_prompt = "login:"
password_prompt = "Password:"
command_prompt = "#"

print (cmd_list)

bulk_tn = mp.Pool(processes=100)
bulk_tn.map_async(tnOne, host_list)
bulk_tn.close()
bulk_tn.join()

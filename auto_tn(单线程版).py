#!/usr/bin/env python
import os
import sys
import telnetlib
from getpass import getpass
##from __future__ import print_function



class AutoTelnet(object):
    def __init__(self, username, password, host_list, cmd_list, **kw):
        self.timeout = kw.get('timeout', 600)
        self.command_prompt = kw.get('command_prompt', "#")
        #self.command_prompt = ["#","$",">"]

        #self.passwd = getpass("Enter user %s password: " % username)
        self.passwd = password

        self.telnet = telnetlib.Telnet()
         
	for host in host_list:
            self.telnet.open(host)

	    #print username
            #print host
	    #print cmd_list
            #print self.passwd

            ok = self.action(username, cmd_list, host)
            if not ok:
                print "Unable to process:", host
            
            self.telnet.close()

    def action(self, username, cmd_list, host):

	oldStdout = sys.stdout
	sys.stdout = open(host,"w+")

        t = self.telnet
        t.write("\n")
        login_prompt = "login:"
        response = t.read_until(login_prompt, 5)
        if login_prompt in response:
            print response + str(username)
        else:
            return 0
        t.write("%s\n" % username)

        password_prompt = "Password:"
        response = t.read_until(password_prompt, 3)

        if password_prompt in response:
            #print response
            print password_prompt + str(self.passwd)
        else:
            return 0
        t.write("%s\n" % self.passwd)

        response = t.read_until(self.command_prompt, 5)
        if self.command_prompt not in response:
            return 0
	else:
	    print self.command_prompt

        for cmd in cmd_list:
            t.write("%s\n" % cmd)
            response = t.read_until(self.command_prompt, self.timeout)
            if self.command_prompt not in response:
                return 0
	    print response
            
	sys.stdout = oldStdout

        return 1
	

if __name__ == '__main__':
    basename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    #logname = os.environ.get("LOGNAME", os.environ.get("USERNAME"))
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
            password = optarg

    print cmd_list
    #print host_list
    autoTelnet = AutoTelnet(username, password, host_list, cmd_list)

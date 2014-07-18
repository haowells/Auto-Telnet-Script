Auto-Telnet-Script
==================

auto telnet to bulk of same root password target machines and execute command

usage: %s [-h host] [-l hostfile] [-f cmdfile] [-c "command"] [-u username] [-p passowrd]
       -c command
       -f command file
       -h single hostname
   -l hostname file
       -u username
       -p password
Example: %s -c "echo $HOME" -u %s -p password

#!/usr/bin/python3
#
# simple_move_robot.py: a simple program to send movement commands to Pulurobot
#
# Copyright (C) 2018 Fabian Fagerholm
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket, sys, struct, binascii, time 

#Main

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCPIP 

server_address = ("192.168.43.23", 22222) #mask and address of the robot 
print("Connecting to {} port {}".format(*server_address))
sock.connect(server_address)
print("Connected.")

while True:
		robotData = sock.recv(3,socket.MSG_WAITALL) #enable to have 3 bytes always
		reply = struct.unpack(">B H", robotData)
		msg_type = reply[0]
		msg_length = reply[1]
		
		if msg_type == 138:
			print("it found 138")     
			robotData = sock.recv(15,socket.MSG_WAITALL) 
			#print("Received {} ({} bytes)".format([b for b in robotData], len(robotData)))
			reply=struct.unpack(">h h h I I B", robotData)
			xsamp = reply[0] #number of column in "map"
			ysamp = reply[1] #nb line
			data = [[0]*xsamp for i in range(ysamp)] #creation of 2D array
			for l in range(0,ysamp):
				for c in range(0,xsamp):
					robotData = sock.recv(1,socket.MSG_WAITALL)
					reply=struct.unpack("> B ", robotData)
					data[l][c] = reply[0]
			print("all data are in a tab")
			print(data)
			break
		else:
			sock.recv(msg_length)

print("Closing socket")
sock.close()
				
















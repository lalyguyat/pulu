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
from math import sqrt

def better_coordinate(posRobot_x, posRobot_y, posHuman_x, posHuman_y):
	vx = posRobot_x - posHuman_x  				#coordinate vector compared to x axe
	vy = posRobot_y - posHuman_y  					#coordinate vector compared to y axe
	lengthv = sqrt(vx*vx + vy*vy) 				#length of vector between robot and human
	BetterCoord_x = posHuman_x + vx / lengthv * 500 	#coordinate of the closest point compared to x axe
	BetterCoord_y = posHuman_y + vy / lengthv * 500 			#coordinate of the closest point compared to x axe
	print("better coordinates are x = %f and y = %f",BetterCoord_x, BetterCoord_y)
	BetterCoord=[]
	BetterCoord.append(BetterCoord_x)
	BetterCoord.append(BetterCoord_y)
	return BetterCoord


#Main 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCPIP 

server_address = ("192.168.43.15", 22222) #mask and adress of the robot 
print("Connecting to {} port {}".format(*server_address))
sock.connect(server_address)
print("Connected.")


fichier = open("coordinates.txt","r") #open text file 
old_x, old_y = None, None

for ligne in fichier:

	#Desc: returning message, position of the robot
	#Retrieved Message Decimal: (130, 10, int16_t ang (--) (2), int32_t x (----)(4), int32_t y (----)(4))
	#recv(socks, msg, lg, option) 
	#int socks : describe socket service 
	#char *msg : adress of the message 
	#int lg : length of the message
	
	while True:
		robotData = sock.recv(3,socket.MSG_WAITALL) #eneable to have 3 bytes always
		#print("Received {} ({} bytes)".format([b for b in robotData], len(robotData)))
		reply = struct.unpack(">B H", robotData)
		msg_type = reply[0]
		msg_length = reply[1]
		if msg_type == 130:
			print("it found 130")
			robotData=sock.recv(msg_length,socket.MSG_WAITALL)
			print("Received {} ({} bytes)".format([b for b in robotData], len(robotData)))
			data=struct.unpack(">h i i B", robotData)
			posRobot_x = int(data[1])
			posRobot_y = int(data[2])
			print(posRobot_x,posRobot_y)
			break
		else:
			sock.recv(msg_length)

	#posRobot_x =-13 
	#posRobot_y =-1

	b=ligne.split(",")
	posHuman_x = int(b[0])
	posHuman_y = int(b[1])
	#y -= 500	don't useful here 
	#print("x =", x, "y =", y)
	coordinates =[]
	coordinates = better_coordinate(posRobot_x, posRobot_y, posHuman_x, posHuman_y) 
	betterCoord_x = int(coordinates[0])
	betterCoord_y = int(coordinates[1])
	
	if old_x == betterCoord_x and old_y == betterCoord_y:
		print("same coordinates")
		continue
	values = (56, 9, betterCoord_x, betterCoord_y, 0) # Find route to specified coordinate
	print(values)

	packer = struct.Struct(">B H i i B")
	packed_data = packer.pack(*values)
	print(packed_data)
	print("Sending {!r}".format(binascii.hexlify(packed_data)))
	sock.sendall(packed_data)
	time.sleep(20)
	old_x, old_y = betterCoord_x, betterCoord_y

fichier.close()
print("Closing socket")
sock.close()





#values = (55, 9, 0, 0, 1) # Move to absolute coordinate, using backwards movement



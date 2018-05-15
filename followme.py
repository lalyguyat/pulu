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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCPIP 

server_address = ("192.168.43.23", 22222) #mask and adress of the robot 
print("Connecting to {} port {}".format(*server_address))
sock.connect(server_address)
print("Connected.")


fichier = open("coordinates.txt","r") #open text file 
old_x, old_y = None, None

for ligne in fichier:

	
	b=ligne.split(",")
	x = int(b[0])
	y = int(b[1])
	y -= 500
	print("x =", x, "y =", y)
	if old_x == x and old_y == y :
		print("same coordinates")
		continue
	values = (56, 9, x, y, 0) # Find route to specified coordinate
	print(values)

	packer = struct.Struct(">B H i i B")
	packed_data = packer.pack(*values)
	print(packed_data)
	print("Sending {!r}".format(binascii.hexlify(packed_data)))
	sock.sendall(packed_data)
	time.sleep(20)
	old_x, old_y = x, y

fichier.close()
print("Closing socket")
sock.close()





#values = (55, 9, 0, 0, 1) # Move to absolute coordinate, using backwards movement



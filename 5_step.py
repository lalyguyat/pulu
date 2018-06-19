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


from PIL import Image, ImageDraw
import socket, sys, struct, binascii, time, csv
#from PIL.Image import *

	

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCPIP 

server_address = ("192.168.43.23", 22222) #mask and adress of the robot 
print("Connecting to {} port {}".format(*server_address))
sock.connect(server_address)
print("Connected.")

#Main

while True:
		robotData = sock.recv(3,socket.MSG_WAITALL) #eneable to have 3 bytes always
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
			#x_robot = reply[3] # it should be the postion of the robot but is isn't like you can see on the terminal because the robtot is always in the center of the windows 100 100
			#y_robot = reply[4]
			#print("la position du robot est :")
			#print(x_robot, y_robot)
			data = [[0]*xsamp for i in range(ysamp)] #creation of 2D tab
			for l in range(0,ysamp):
				for c in range(0,xsamp):
					robotData = sock.recv(1,socket.MSG_WAITALL)
					reply=struct.unpack("> B ", robotData)
					data[l][c] = reply[0]
			print("all data are in a tab")
			#print(data)
			break
		else:
			sock.recv(msg_length)


valeurs = [[0]*xsamp for i in range(ysamp)] #creation of 2D tab
for l in range(0,ysamp):
	for c in range(0,xsamp):
		valeurs[l][c] = str(data[l][c])
			
entetes=200*[0] #creation of header (I do not need header for line because in calc there are already line numbers)
for i in range(len(entetes)):
	entetes[i]=str(i)

f = open('dataHmap.csv', 'w') #creation and open of a csv file 
ligneEntete = ";".join(entetes) + "\n" # write header 
f.write(ligneEntete)
for valeur in valeurs:
     ligne = ";".join(valeur) + "\n"
     f.write(ligne)  # after write header write data

f.close()



# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
img = Image.new( 'RGB', (xsamp,ysamp), "white") # create a new white image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every col:
	for j in range(img.size[1]):    # For every row
		if data[i][j]==0 :
			continue #just let white this box
		elif data[i][j]==1:
			pixels[i,j] = (232, 234, 237) # floor white or very light grey
		elif data[i][j]==2:
			pixels[i,j] = (237, 230, 8) # threshold = yellow 
		elif data[i][j]==3:
			pixels[i,j] = (145, 0, 206) # small drop = purple  
		elif data[i][j]==4:
			pixels[i,j] = (132, 134, 134) # small item = grey 
		elif data[i][j]==5:
			pixels[i,j] = (246, 95, 210) # big drop = pink 
		elif data[i][j]==6:
			pixels[i,j] = (94, 249, 24) # low ceiling = flash green 
		elif data[i][j]==7:
			pixels[i,j] = (94, 55,24) # big item = brown
		else :
			pixels[i,j] = (2, 0, 0) # wall = black 
img=img.transpose(Image.FLIP_LEFT_RIGHT)#the origin of the rows and colums are in the left bottom not in the top left page like I thought so i just inverse 
img=img.transpose(Image.ROTATE_180)# to have the orientation of the robot in the top of the page
draw = ImageDraw.Draw(img)
RED = (255, 0, 0, 0)
draw.ellipse([(97, 97), (103, 103)], fill="white", outline=RED)  #robot in red at the position 100, 100 always.We could use the TCP/IP to know were is the robot, because the 3 and 4 bytes of the 138 case is the position but it doesn't work


BLACK = (0, 0, 0, 0)
draw.text((20, 20), "InFrontOfR_OnlyLegs", fill=BLACK)
img.show()
print("Closing socket")
sock.close()

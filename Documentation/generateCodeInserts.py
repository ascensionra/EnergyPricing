import os

def createFile(outName):
	o = open(outName,"w+r")
	f = open("EIA_PET_codes.txt","r")

	if not o.seek(0,2) == 0:
		print outName + " not empty, truncating file for writing\n"
		o.truncate(0)

	for i in f:
		line = i.split("::")
		o.write("INSERT INTO PET_SERIES VALUES (q'[%s]',q'[%s]',q'[%s]');\n" % (line[0],line[1],line[2]))

	o.close()
	f.close()

if __name__ == '__main__':
	createFile("codes.sql")

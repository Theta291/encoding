from encoding_class import *
import math
import os

first = True
while True:
	filename = input("Enter filename: ")
	if len(filename) == 0:
		break
	nameWOExt, fileExt = filename.split('.')
	print("File size:\t", getFileSize(filename) * 8, "bits")
	encodeName = nameWOExt + '_tern1.bin'
	file = open(filename, 'r')
	fileString = file.read()
	file.close()
	fileString = fileString[:-1]
	countDict = countChars(fileString)
	fileEntropy = getEntropy(countDict)
	print("Avg info density:\t", fileEntropy / 8)

	if first:
		testEncoder = createTernEncoder1(fileString)
		first = False
	
	newFile = open(encodeName, 'wb+')
	newFile.write(testEncoder.encode(fileString))
	newFile.close()
	del newFile

	newFile = open(encodeName, 'rb')
	encodedBytes = newFile.read()
	newFile.close()
	print("File size:\t", getFileSize(encodeName) * 8, "bits")
	binStr = BIN_STR_TO_BYTES.decode(encodedBytes)
	encodedEntPerBit = testEncoder.getWeightedEntropy(fileString)
	print("Avg info density:\t", encodedEntPerBit)

	testName = nameWOExt + '_2.' + fileExt
	newnewFile = open(testName, 'w+')
	newnewFile.write(testEncoder.decode(encodedBytes))
	newnewFile.write('\n')
	newnewFile.close()

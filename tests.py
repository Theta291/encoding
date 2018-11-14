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
	
	encodeNameTern = nameWOExt + '_tern1.bin'
	encodeNameHuff = nameWOExt + '_huff.bin'
	
	file = open(filename, 'r')
	fileString = file.read()
	file.close()
	fileString = fileString[:-1]
	countDict = countChars(fileString)
	fileEntropy = getEntropy(countDict)
	print("Avg info density (original):\t", fileEntropy / 8)

	if first:
		testTernEncoder = createTernEncoder1(fileString)
		testHuffEncoder = createHuffEncoder(fileString)
		first = False
	
	newFile = open(encodeNameTern, 'wb+')
	newFile.write(testTernEncoder.encode(fileString))
	newFile.close()
	del newFile

	newFile = open(encodeNameHuff, 'wb+')
	newFile.write(testHuffEncoder.encode(fileString))
	newFile.close()
	del newFile

	newFile = open(encodeNameTern, 'rb')
	encodedBytes1 = newFile.read()
	newFile.close()
	del newFile

	print("File size:\t", getFileSize(encodeNameTern) * 8, "bits")
	encodedEntPerBitTern = testTernEncoder.getWeightedEntropy(fileString)
	print("Avg info density (tern 1):\t", encodedEntPerBitTern)

	testNameTern = nameWOExt + '_tern1_decoded.' + fileExt
	newnewFile = open(testNameTern, 'w+')
	newnewFile.write(testTernEncoder.decode(encodedBytes1))
	newnewFile.write('\n')
	newnewFile.close()
	del newnewFile

	newFile = open(encodeNameHuff, 'rb')
	encodedBytes2 = newFile.read()
	newFile.close()

	print("File size:\t", getFileSize(encodeNameHuff) * 8, "bits")
	encodedEntPerBitHuff = testHuffEncoder.getWeightedEntropy(fileString)
	print("Avg info density (huff):\t", encodedEntPerBitHuff)

	testNameHuff = nameWOExt + '_huff_decoded.' + fileExt
	newnewFile = open(testNameHuff, 'w+')
	newnewFile.write(testHuffEncoder.decode(encodedBytes2))
	newnewFile.write('\n')
	newnewFile.close()
	

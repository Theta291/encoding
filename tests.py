import math
import os

all_ascii = [chr(i) for i in range(128)]

def sumDictVals(aDict):
	return sum(aDict.values())

def getFileSize(fileName):
	statinfo = os.stat(fileName)
	return statinfo.st_size

def bytesFromFile(file, chunksize=8192):
	fileBytes = bytearray()
	while True:
		chunk = file.read(chunksize)
		if chunk:
			for b in chunk:
				fileBytes.append(b)
		else:
			return fileBytes

def countChars(aString):
	countDict = {}
	for aChar in aString:
		if aChar in countDict:
			countDict[aChar] += 1
		else:
			countDict[aChar] = 1
	return countDict

def countToProbDict(countDict):
	total = sumDictVals(countDict)
	return {k: v/total for k, v in countDict.items()}

def unitsToLogFunc(units=None):
	if units == 'bits' or units == 'shannons':
		logger = math.log2
	elif units == 'digits' or units == 'hartleys':
		logger = math.log2
	else:
		logger = math.log
	def retFunc(num):
		if num == 0:
			return 0
		else:
			return logger(num)
	return retFunc

def getInfoCont(countDict, units='bits'):
	total = sumDictVals(countDict)
	toLog = unitsToLogFunc(units)
	return total * toLog(total) - sum(map(lambda x: x * toLog(x), countDict.values()))

def getEntropy(countDict, units='bits'):
	total = sumDictVals(countDict)
	toLog = unitsToLogFunc(units)
	return toLog(total) - sum(map(lambda x: x * toLog(x), countDict.values())) / total

'''def binStrToBytes(binStr):
	rem = len(binStr) % 8
	if rem > 0:
		binStr = ''.join(['0' for i in range(rem, 8)] + list(binStr))
	return 

class encoder:
	def __init__(self, encodeDict, outValType=str):
		self.encodeDict = dict(encodeDict)
		self.decodeDict = {v: k for k, v in encodeDict.items()}
		self.outValType = outValType

	def encode(self, inIter):
		if self.outValType == str:
			return ''.join([self.encodeDict[val] for val in inIter])
		elif self.outValType == bool:
			bitStr = ''.join([self.encodeDict[val] for val in inIter])
			rem = len(bitStr) % 8
			if rem > 0:
				bitStr = ''.join(list(bitStr) + ['0' for i in range(rem, 8)])
			return binStrToBytes(bitStr)

	def decode(self, inIter):
		if self.outValType == str:
			return ''.join([decodeDict[val] for val in inIter])'''

class encoder:
	pass

binStrToBytes = encoder()
binToHexDict = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7', '1000': '8', '1001': '9', '1010': 'a', '1011': 'b', '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f'}
hexToBinDict = {v: k for k, v in binToHexDict.items()}

def binStrToBytesEncode(bitStr):
	rem = len(bitStr) % 8
	if rem > 0:
		bitStr = ''.join(list(bitStr) + ['0' for i in range(rem, 8)])
	hexStr = ''.join([binToHexDict[bitStr[i:i+4]] for i in range(0, len(bitStr), 4)])
	retBytes =  bytes.fromhex(hexStr)
	return retBytes

def binStrToBytesDecode(inBytes):
	hexStr = inBytes.hex()
	return ''.join([hexToBinDict[char] for char in hexStr])

binStrToBytes.encode = binStrToBytesEncode
binStrToBytes.decode = binStrToBytesDecode

def toBaseStr(num, base, minLen=0, startBase=10):
	rem = num
	retList = []
	if type(num) == str or startBase != 10:
		num = str(num)
	if num == 0:
		return ''.join(['0' for i in range(minLen)])
	numDigs = int(math.log(rem, base)) + 1
	currDigs = numDigs
	
	while currDigs > 0:
		placeVal = base ** (currDigs - 1)
		retList.append(str(int(rem / placeVal)))
		rem = rem % placeVal
		currDigs -= 1
		
	if numDigs < minLen:
		retList = ['0' for i in range(numDigs, minLen)] + retList
	return ''.join(retList)

def ternEncoder1(aString):
	def encodeValsGen(numVals=None):
		counter = 1
		while True:
			if numVals == 0:
				return
			encodeLen = math.ceil(math.log(2 * counter + 1, 3)) - 1
			encodeNum = counter - int((3 ** (encodeLen) - 1) / 2) - 1
			terStr = toBaseStr(encodeNum, 3, minLen = encodeLen)
			yield ''.join([toBaseStr(int(digit), 2, minLen=2) for digit in terStr])
			counter += 1
			if numVals is not None:
				numVals -= 1

	countDict = countChars(aString)
	charsByProb = sorted(countDict.keys(), key=countDict.get, reverse=True)
	charsByProb.extend([char for char in all_ascii if char not in charsByProb])
	decodeDict = dict(zip(encodeValsGen(len(charsByProb)), charsByProb))
	encodeDict = {v: k + '11' for k, v in decodeDict.items()}

	def encodeFunc(someString):
		bitStr = ''.join([encodeDict[char] for char in someString])
		return binStrToBytes.encode(bitStr)

	def decodeFunc(someBytes):
		bitStr = binStrToBytes.decode(someBytes)
		splitBitStr = []
		prevSplit = 0
		for i in range(0, len(bitStr), 2):
			if bitStr[i:i+2] == '11':
				splitBitStr.append(bitStr[prevSplit:i])
				prevSplit = i+2
		retList = [decodeDict[bins] for bins in splitBitStr]
		retList.pop()
		return ''.join(retList)
	
	retEncoder = encoder()
	retEncoder.encodeDict = dict(encodeDict)
	retEncoder.decodeDict = dict(decodeDict)
	retEncoder.encode = encodeFunc
	retEncoder.decode = decodeFunc
	
	return retEncoder

first = True
while True:
	filename = input("Enter filename: ")
	nameWOExt, fileExt = filename.split('.')
	print("File size:\t", getFileSize(filename) * 8, "bits")
	encodeName = nameWOExt + '_tern1.bin'
	file = open(filename, 'r')
	fileString = file.read()
	file.close()
	fileString = fileString[:-1]
	countDict = countChars(fileString)
	fileEntropy = getEntropy(countDict)
	print("Bits entropy per byte:\t", fileEntropy)

	if first:
		testEncoder = ternEncoder1(fileString)
		first = False
	
	newFile = open(encodeName, 'wb+')
	newFile.write(testEncoder.encode(fileString))
	newFile.close()
	del newFile

	newFile = open(encodeName, 'rb')
	encodedBytes = bytesFromFile(newFile)
	newFile.close()
	print("File size:\t", getFileSize(encodeName) * 8, "bits")
	binStr = binStrToBytes.decode(encodedBytes)
	total = sumDictVals(countDict)
	encodedEntPerByte =  -sum(map(lambda item: 8 * item[1] * math.log2(item[1] / total) / len(testEncoder.encodeDict[item[0]]), countDict.items())) / total
	print("Bits entropy per byte:\t", encodedEntPerByte)

	testName = nameWOExt + '_2.' + fileExt
	newnewFile = open(testName, 'w+')
	newnewFile.write(testEncoder.decode(encodedBytes))
	newnewFile.write('\n')
	newnewFile.close()

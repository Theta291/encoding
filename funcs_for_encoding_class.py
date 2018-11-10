import math
import os

ALL_ASCII = [chr(i) for i in range(128)]

def sumDictVals(aDict):
	return sum(aDict.values())

def getFileSize(fileName):
	statinfo = os.stat(fileName)
	return statinfo.st_size

def countChars(aString):
	countDict = {}
	for aChar in aString:
		if aChar in countDict:
			countDict[aChar] += 1
		else:
			countDict[aChar] = 1
	return countDict

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

def getWeightedEntropy(countDict, encodeDict, units='bits'):
	total = sumDictVals(countDict)
	toLog = unitsToLogFunc(units)
	return -sum(map(lambda item: item[1] * toLog(item[1] / total) / len(encodeDict[item[0]]), countDict.items())) / total

def toDigit(num):
	if num < 10:
		return str(num)
	elif num < 36:
		return chr(num + 87)
	else:
		raise ValueError('Cannot convert to bases greater than 36')

def toBaseStr(num, base, minLen=0, startBase=10):
	retList = []
	if startBase != 10:
		num = str(num)
	try:
		if int(num) == 0:
			return ''.join(['0' for i in range(minLen)])
	except ValueError:
		pass
	rem = num
	numDigs = int(math.log(rem, base)) + 1
	currDigs = numDigs
	
	while currDigs > 0:
		placeVal = base ** (currDigs - 1)
		retList.append(toDigit(int(rem / placeVal)))
		rem = rem % placeVal
		currDigs -= 1
	
	if numDigs < minLen:
		retList = ['0' for i in range(numDigs, minLen)] + retList
	return ''.join(retList)

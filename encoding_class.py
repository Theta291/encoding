from funcs_for_encoding_class import *

class encoder:
	def __init__(self, *posArgs, **kwArgs):
		if 'outputType' in kwArgs:
			outputType = kwArgs['outputType']
			self.outputType = outputType
		if 'encodeDict' in kwArgs:
			encodeDict = kwArgs['encodeDict']
			try:
				if self.outputType == bool:
					if all([type(val) is int for val in encodeDict.values()]):
						self.encodeDict = {k: toBaseStr(v, 2) for k, v in encodeDict.items()}
					else:
						self.encodeDict = dict(encodeDict)
				else:
					self.encodeDict = dict(encodeDict)
			except AttributeError:
				self.encodeDict = dict(encodeDict)
			if 'decodeDict' in kwArgs:
				decodeDict = kwArgs['decodeDict']
				try:
					if self.outputType == bool:
						if all([type(key) is int for key in decodeDict.keys()]):
							self.decodeDict = {toBaseStr(k, 2): v for k, v in decodeDict.items()}
						else:
							self.decodeDict = dict(decodeDict)
					else:
						self.decodeDict = dict(decodeDict)
				except AttributeError:
					self.decodeDict = dict(decodeDict)
			else:
				self.decodeDict = {v: k for k, v in encodeDict.items()}

	def encode(self, unCoded):
		try:
			if self.outputType == bool:
				try:
					binStr = ''.join([self.encodeDict[char] for char in unCoded])
					return BIN_STR_TO_BYTES.encode(binStr)
				except AttributeError as err:
					raise err
			if self.outputType == str:
				try:
					key1len = len(list(self.encodeDict.keys())[0])
					if all([len(k) == key1len for k in self.encodeDict]):
						if key1len == 1:
							chopped = unCoded
						else:
							chopped = [unCoded[i:i+key1len] for i in range(0, len(unCoded), key1len)]
						retStr = ''.join([self.encodeDict[char] for char in chopped])
						return retStr
				except AttributeError as err:
					raise err
		except AttributeError as err:
			raise err

	def getWeightedEntropy(self, unCoded, units='bits'):
		toLog = unitsToLogFunc(units)
		try:
			if self.outputType == str:
				if units == 'bits':
					raise NotImplemented
			elif self.outputType == bool:
				if units == 'bits':
					size = lambda x : len(self.encodeDict[x])
		except AttributeError as err:
			raise err
		countDict = countChars(unCoded)
		total = sumDictVals(countDict)
		return -sum(map(lambda item : item[1] * toLog(item[1] / total) / size(item[0]), countDict.items())) / total

BIN_TO_HEX_DICT = {toBaseStr(i, 2, minLen=4): hex(i)[2:] for i in range(16)}
BIN_STR_TO_BYTES = encoder(encodeDict=BIN_TO_HEX_DICT, outputType=bool)
HEX_TO_BIN_DICT = {v: k for k, v in BIN_TO_HEX_DICT.items()}

def binStrToBytesEncode(bitStr):
	rem = len(bitStr) % 8
	if rem > 0:
		bitStr = ''.join(list(bitStr) + ['0' for i in range(rem, 8)])
	hexStr = ''.join([BIN_TO_HEX_DICT[bitStr[i:i+4]] for i in range(0, len(bitStr), 4)])
	retBytes =  bytes.fromhex(hexStr)
	return retBytes

def binStrToBytesDecode(inBytes):
	hexStr = inBytes.hex()
	return ''.join([HEX_TO_BIN_DICT[char] for char in hexStr])

BIN_STR_TO_BYTES.encode = binStrToBytesEncode
BIN_STR_TO_BYTES.decode = binStrToBytesDecode

CHANGE_BASE = encoder()

CHANGE_BASE.encode = toBaseStr
CHANGE_BASE.decode = lambda numStr, base: int(toBaseStr(numStr, 10))

def createTernEncoder1(aString):
	def encodeValsGen(numVals=None):
		counter = 1
		while True:
			if numVals == 0:
				return
			encodeLen = math.ceil(math.log(2 * counter + 1, 3)) - 1
			encodeNum = counter - int((3 ** (encodeLen) - 1) / 2) - 1
			terStr = CHANGE_BASE.encode(encodeNum, 3, minLen = encodeLen)
			yield ''.join([CHANGE_BASE.encode(int(digit), 2, minLen=2) for digit in terStr])
			counter += 1
			if numVals is not None:
				numVals -= 1

	countDict = countChars(aString)
	charsByProb = sorted(countDict.keys(), key=countDict.get, reverse=True)
	charsByProb.extend([char for char in ALL_ASCII if char not in charsByProb])
	decodeDict = dict(zip(encodeValsGen(len(charsByProb)), charsByProb))
	encodeDict = {v: k + '11' for k, v in decodeDict.items()}

	def decodeFunc(someBytes):
		bitStr = BIN_STR_TO_BYTES.decode(someBytes)
		splitBitStr = []
		prevSplit = 0
		for i in range(0, len(bitStr), 2):
			if bitStr[i:i+2] == '11':
				splitBitStr.append(bitStr[prevSplit:i])
				prevSplit = i+2
		retList = [decodeDict[bins] for bins in splitBitStr]
		retList.pop()
		return ''.join(retList)

	retEncoder = encoder(encodeDict=encodeDict, decodeDict=decodeDict, outputType=bool)
	retEncoder.decode = decodeFunc

	return retEncoder

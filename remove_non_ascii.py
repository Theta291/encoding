filename = input('File name: ')
file = open(filename, 'r')
fileString = file.read(encoding='utf-8')
file.close()

def check_val_ascii(val):
    return 0 <= val and val < 128

newList = [char for char in fileString if check_val_ascii(ord(char))]
newString = ''.join(newList)

file = open(filename, 'w')
file.write(newString)
file.close()

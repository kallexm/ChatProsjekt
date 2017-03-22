import time

def testTupleReturn():
	return "String1", "String2"

timeStruct = time.localtime(None)
print(time.strftime("%x"))
str1, str2 = testTupleReturn()

print(str1)
print(str2)


dict1 = {"one": 1, "two": 2}
print(dict1)
#del dict1["two"]
print(dict1)

for elem in dict1:
	print(elem)


print("Hello this is a long string\n that should go over several lines")
#Python 3

dataFile = open("student_requests.txt")

students = []
requests = {}
good = 2
bad = 1

temp = ""
count = 1
for line in dataFile:
	temp = line.split()
	name = temp[0] + " " + temp[1]
	prefs = list(map(int, temp[2:]))
	
	students.append(name)
	requests[count] = [prefs[:good],[],prefs[good:]] #Test this to make sure the code is correct
	count += 1
#print(requests)
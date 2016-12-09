import random

random.seed()

data = open("student_requests.txt", 'w')
names = open("names_25.txt")

count = 1
for line in names:
	temp = []
	while len(temp) != 5:
		temp_rand = random.randint(1, 25)
		if temp_rand not in temp and temp_rand != count:
			temp.append(temp_rand)
	
	data.write(line.strip() + " " + str(temp[0]) + " " + str(temp[1]) + " " + str(temp[2]) + " " + str(temp[3]) + " " + str(temp[4]) + "\n")
	count += 1
	
names.close()
data.close()
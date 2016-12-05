import read_in_data as rd
import copy

original = rd.requests
oneDegree = copy.deepcopy(original)

for key, value in original.items():
	for person in value[0]:
		#Add a list in the big list of lists to be the list of people that are one degree away
		oneDegree[key][1] = oneDegree[key][1] + original[int(person)][0]
		#oneDegree[key] = [oneDegree[key][0], original[int(person)][0] + oneDegree[key][1], value[1]]
		#print(oneDegree[key])
	oneDegree[key][1] = list(set(oneDegree[key][1]))
	#if key in oneDegree[key][0]:
	#	oneDegree[key][0].remove(key)

print(oneDegree)

#for person in len(rd.students):
	#start making a not-a-matrix matrix for the students' preferences, initializing every value to 2
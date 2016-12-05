import read_in_data as rd
import copy, pdb

original = rd.requests
oneDegree = copy.deepcopy(original)

for key, value in original.items():
	oneDegree[key].insert(1, [])


for key, value in original.items():
	for person in value[0]:
		pdb.set_trace()
		oneDegree[key][1] + list(set(original[int(person)][0]))
		#print(oneDegree[key])
	#oneDegree[key] = [list(set(oneDegree[key][0])),value[1]]
	if key in oneDegree[key][0]:
		oneDegree[key][0].remove(key)
		


print(oneDegree)
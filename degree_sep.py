import read_in_data as rd
import happiness

import copy, pdb
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering

def print_data(data):
	for i in data:
		for j in i:
			print(j, end="")
		print()

original = rd.requests
oneDegree = copy.deepcopy(original)

for key, value in original.items():
	for person in value[0]:
		#Add a list in the big list of lists to be the list of people that are one degree away
		oneDegree[key][1] = oneDegree[key][1] + original[int(person)][0]
		#oneDegree[key] = [oneDegree[key][0], original[int(person)][0] + oneDegree[key][1], value[1]]
		#print(oneDegree[key])
	oneDegree[key][1] = list(set(oneDegree[key][1]))
	if key in oneDegree[key][1]:
		oneDegree[key][1].remove(key)

print(oneDegree)
friendWeight = .75
"""
preferences = np.array([])
distances = np.array([])
for i in range(len(rd.students)):
	temp = np.array([])
	temp2 = np.array([])
	for j in range(len(rd.students)):
		np.append(temp, 0)
		np.append(temp2, 2)
		#temp.append(0)
		#temp2.append(2)
	#preferences.append(temp)
	#distances.append(temp2)
	np.append(preferences, temp)
	np.append(distances, temp2)
"""	
#This works!!!
preferences = np.identity(len(rd.students))
distances = np.full((len(rd.students), len(rd.students)), 2)


#preferences = [[0]*len(rd.students)]*len(rd.students)
for person, prefs in oneDegree.items():
	preferences[person-1][person-1] = 1
	#print(person)
	#print(prefs)
	#pdb.set_trace()
	friendWeight = .75
	for friend in prefs[0]:
		preferences[person-1][friend-1] += friendWeight
		friendWeight *= .25
	friendWeight = .25
	for secondaryFriend in prefs[1]:
		preferences[person-1][secondaryFriend-1] += friendWeight
	friendWeight = -.33
	for enemy in prefs[2]:
		preferences[person-1][enemy-1] += friendWeight

for row in range(len(preferences)): #row and column are indeces to parallel distances[]
	for column in range(len(preferences)):
		#if preferences[row][column]  != 0.0 and row != column:
		#if row != column:
		distances[row][column] = np.linalg.norm(preferences[row] - preferences[column])

		
num_clusters = 5
		
#----------------KMeans Clustering Algoritm-----------------------
#kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(distances)
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(preferences)
kmeans_groups = kmeans.labels_ #This is a np.ndarray

groups = {}
for i  in range(num_clusters):
	groups[i] = []
	
for i in range(len(kmeans_groups)):
	groups[kmeans_groups[i]].append(rd.students[i])

print("-------------------KMeans------------------------")
print_data(groups.items())
print()
group_happiness = happiness.calculate_happiness(groups, distances, rd.students) # prints the happiness of the people
print("Total Happiness: " + str(sum(group_happiness)))
print("-------------------------------------------------\n\n\n")



#--------------------Spectral Clustering-------------------------------
#spectral = SpectralClustering(n_clusters=num_clusters).fit(distances)
spectral = SpectralClustering(n_clusters=num_clusters).fit(preferences)
spectral_groups = spectral.labels_

groups = {}
for i  in range(num_clusters):
	groups[i] = []
	
for i in range(len(spectral_groups)):
	groups[spectral_groups[i]].append(rd.students[i])
	
print("--------------------Spectral----------------------")
print_data(groups.items())
print()
group_happiness = happiness.calculate_happiness(groups, distances, rd.students) # prints the happiness of the people
print("Total Happiness: " + str(sum(group_happiness)))
print("--------------------------------------------------\n\n\n")
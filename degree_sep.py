import read_in_data as rd
import happiness

import copy, pdb
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors

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
		try:
			oneDegree[key][1] = oneDegree[key][1] + original[int(person)][0]
		except:
			pdb.set_trace()
		#oneDegree[key] = [oneDegree[key][0], original[int(person)][0] + oneDegree[key][1], value[1]]
		#print(oneDegree[key])
	oneDegree[key][1] = list(set(oneDegree[key][1]))
	if key in oneDegree[key][1]:
		oneDegree[key][1].remove(key)

#print(oneDegree)
friendWeight = .75

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
	friendWeight = -.5
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
kmeans = KMeans(n_clusters=num_clusters, init='k-means++', random_state=0).fit(preferences)
kmeans_groups = kmeans.labels_ #This is a np.ndarray

group_centers = kmeans.cluster_centers_ #These are the cluster centers



"""neigh = NearestNeighbors(algorithm='ball_tree')
neigh_centers_fit = [neigh.fit(center) for center in centers]
neigh_groups = {}

for center in centers:
	neigh_groups[center] = neigh.kneighbors(preferences, 5, return_distance=False)

print(neigh_groups)
"""

#-----------------Outputs the kmean groups in a readable fashion

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


while True:
	done = True
	for groupNumber, people in groups.items():
		if len(people) != 5:
			done = False
	
	if done == True:
		break
	small_group_centers = {}
	bigPeopleNames = {}

	for key, group in groups.items():
		if len(group) < 5:
			small_group_centers[key] = group_centers[key]
		if len(group) > 5:
			for person in group:
				bigPeopleNames[rd.students.index(person)] = key
	#pdb.set_trace()

	new_prefs = {}
	for person, groupNumber in bigPeopleNames.items():
		new_prefs[person] = preferences[person]
		
	lowestDistance = float("inf")
	lowestPerson = None
	lowestGroup = None
	bigGroup = None
	for personIndex, personPrefs in new_prefs.items():
		for groupNumber, groupCenter in small_group_centers.items():
			distance = np.linalg.norm(personPrefs - groupCenter)
			if distance < lowestDistance:
				lowestDistance = distance
				lowestPerson = personIndex
				lowestGroup = groupNumber
				bigGroup = bigPeopleNames[personIndex]
	print(lowestDistance)
	print(lowestPerson)
	print(bigGroup)
	print(lowestGroup)

	groups[bigGroup].remove(rd.students[lowestPerson])
	groups[lowestGroup].append(rd.students[lowestPerson])
	print(groups)

#print(small_group_centers)


#Average the groups < 5 into a single point. 
# For all of the people in the groups > 5, move the closest person to the "single point" into the smaller group
# recalculate the average if the small group is still less than 5

"""
#pdb.set_trace()
group_points = {}
for key, group in groups.items():
	#Condenses the group into a single point
	if len(group) < 5:
		avg = np.zeros_like(preferences[key])
		#pdb.set_trace()
		count = 0.0
		for member in group:
			idx = rd.students.index(member)
			#pdb.set_trace()
			avg += preferences[idx]
			count += 1.0
			print(preferences[idx])
		avg = avg/count
		group_points[key] = avg
		print(avg)

bigPeopleNames = []
temp_groups = copy.deepcopy(groups)
for key, group in groups.items():
	if len(group) == 5:
		del temp_groups[key] #make sure this doesn't mess up with copying stuff
"""
	
	#if len(group) > 5:
	#	bigPeopleNames += group
"""
num_clusters = len(temp_groups)

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
"""



"""[ 0.25      0.296875  0.        1.        0.        0.        0.        0.
  0.        0.4375    0.        0.        0.        0.        0.       -0.25
  0.        0.       -0.5       0.25      1.        0.        0.25      0.25
  0.25    ]
[ 0.        0.        0.25      0.       -0.5       0.        0.        0.25
  0.        0.1875   -0.5       0.        0.25      0.046875  0.        1.
  0.        0.        0.        0.25      0.25      0.75      0.25      0.
  0.25    ]
[ 0.        0.        0.        0.        0.046875  0.        0.        1.
  0.        0.25      0.25      0.       -0.25      0.        0.        0.25
  1.        0.25      0.        0.        0.25      0.1875    0.        0.
 -0.5     ]
[ 0.05395833 -0.02354167 -0.23416667  0.00645833  0.47916667  0.05583333
  0.113125    0.73729167  0.01645833  0.23479167  0.275625   -0.01333333
 -0.04270833  0.18020833  0.13458333  0.08833333  0.47208333  0.69791667
  0.01666667  0.13895833  0.24291667  0.20083333  0.1525      0.11791667
 -0.32604167]"""
		


"""#--------------------Spectral Clustering-------------------------------
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
"""
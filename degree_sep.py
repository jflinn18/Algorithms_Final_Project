import read_in_data as rd
import happiness

import copy, pdb
import numpy as np
from sklearn.cluster import KMeans

# Prints a list of lists
def print_data(data):
	for i in data:
		for j in i:
			print(j, end="")
		print()

# imports some data from read_in_data.py
original = rd.requests
# This is a dictionary of data that corresponds to each student
oneDegree = copy.deepcopy(original)

# Adds some data to the dictionary of data for each person
#   The new data is a list of people that are one degree from the key person
for key, value in original.items():
	for person in value[0]:
		oneDegree[key][1] = oneDegree[key][1] + original[int(person)][0]
	oneDegree[key][1] = list(set(oneDegree[key][1]))
	if key in oneDegree[key][1]:
		oneDegree[key][1].remove(key)

friendWeight = .75
# Initializes the preferences of all of the people
preferences = np.identity(len(rd.students))
# Initializes all of the distances to 2
distances = np.full((len(rd.students), len(rd.students)), 2)


# This creates an n-dimensional vector space
# Each vector represents a person that we are trying to group
for person, prefs in oneDegree.items():
	preferences[person-1][person-1] = 1

	# Moves the person in the direction of the people that they want to work with
	friendWeight = .75
	for friend in prefs[0]:
		preferences[person-1][friend-1] += friendWeight
		friendWeight *= .25

	# Moves the person in the direction of the one degree people
	friendWeight = .25
	for secondaryFriend in prefs[1]:
		preferences[person-1][secondaryFriend-1] += friendWeight

	# Moves away from the people that the person doesn't want to work with.
	friendWeight = -.5
	for enemy in prefs[2]:
		preferences[person-1][enemy-1] += friendWeight

# Computes the distances between each person and everyone else
# This is an NxN matrix that is symmetrical over the major axis
for row in range(len(preferences)): #row and column are indeces to parallel distances[]
	for column in range(len(preferences)):
		distances[row][column] = np.linalg.norm(preferences[row] - preferences[column])


num_clusters = 5

#----------------KMeans Clustering Algoritm-----------------------
kmeans = KMeans(n_clusters=num_clusters, init='k-means++', random_state=0).fit(preferences)
kmeans_groups = kmeans.labels_ #This is a np.ndarray

group_centers = kmeans.cluster_centers_ #These are the cluster centers
#-----------------------------------------------------------------

# Initializes groups
groups = {}
for i  in range(num_clusters):
	groups[i] = []

# Translates the numbers to actual names
for i in range(len(kmeans_groups)):
	groups[kmeans_groups[i]].append(rd.students[i])


# Prints the groups information after clustering
print("\n\n")
print("-------------------KMeans------------------------")
print_data(groups.items())
print()
group_happiness = happiness.calculate_happiness(groups, distances, rd.students) # prints the happiness of the people
print("Total Happiness: " + str(sum(group_happiness)))
print("-------------------------------------------------\n\n\n")


# This evens out the groups. KMeans creates a specific number of clusters.
# But these clusters may not be even.

# [!] Note: this is hard coded. If the size of the input data changes dramatically,
#           some of these values will need to be changed.
while True:
	done = True
	for groupNumber, people in groups.items():
		if len(people) != 5:
			done = False

	if done == True:
		break

	small_group_centers = {}
	bigPeopleNames = {}

	# Gets the small group centers
	# Also compiles a list of all of the people in groups that are too big
	for key, group in groups.items():
		if len(group) < 5:
			small_group_centers[key] = group_centers[key]
		if len(group) > 5:
			for person in group:
				bigPeopleNames[rd.students.index(person)] = key

	# Compile the preferences of only the people in the groups that are too big
	# This will be used to compute the distance between these people and the
	#   centers of the small groups
	new_prefs = {}
	for person, groupNumber in bigPeopleNames.items():
		new_prefs[person] = preferences[person]

	# Conducts a greedy search for the person that is in one of the larger groups
	#    that is closest to one of the smaller groups. That person is moved into
	#    the smaller group.
	lowestDistance = float("inf")
	lowestPerson = None
	lowestGroup = None
	bigGroup = None
	for personIndex, personPrefs in new_prefs.items():
		for groupNumber, groupCenter in small_group_centers.items():
			distance = np.linalg.norm(personPrefs - groupCenter)
			# Gets all of the needed information of the person that is in one of
			#   the groups that are too big that is closest to one of the smaller groups
			if distance < lowestDistance:
				lowestDistance = distance
				lowestPerson = personIndex
				lowestGroup = groupNumber
				bigGroup = bigPeopleNames[personIndex]

	# Move the person from the big group to the small group
	groups[bigGroup].remove(rd.students[lowestPerson])
	groups[lowestGroup].append(rd.students[lowestPerson])


# Prints out the groups that have been assigned
print("---------------KMeans Evened Out-----------------------")
print_data(groups.items())
print()
group_happiness = happiness.calculate_happiness(groups, distances, rd.students) # prints the happiness of the people
print("Total Happiness: " + str(sum(group_happiness)))
print("-------------------------------------------------\n\n\n")

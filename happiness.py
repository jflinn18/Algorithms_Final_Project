import pdb

"""
@groups: 						 A map of the created groups
@happiness_matrix: 		 A matrix of distances of all of the people
@member_encoder:        A map of people and the number associated with them (indecies of the matrix)
"""
def calculate_happiness(groups, happiness_matrix, member_encoder): 
	happy_list = [0]*len(groups)
	
	for group_num, group_members in groups.items():
		for i in range(len(group_members)):
			for j in range(i,len(group_members)):
				happy_list[group_num] += happiness_matrix[member_encoder.index(group_members[i])][member_encoder.index(group_members[j])]
					
	for i in range(len(happy_list)):
		print("group" + str(i) + ": ", happy_list[i])
		
	return happy_list
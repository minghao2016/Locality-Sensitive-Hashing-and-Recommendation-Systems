from __future__ import division
import json
import sys
import re
import math
import operator
from itertools import combinations

# deine user node object for storing (user, jaccard similarity) pair
class UserNode():
	def __init__(self, name, num):
		self.userName = name
		self.jaccard = num

def createCharacteristicSets(document, matrix):
	for user in document:
		matrix.setdefault(user[0], set(user[1]))
	return matrix

def calulateJaccard(setA, setB):
	intersection = setA & setB
	union = setA | setB
	return len(intersection) / len(union)

def recommendationSystem(candidateList):
	# import input data in problem 1
	userData = []
	document = open(sys.argv[1])
	for line in document:
		user = json.loads(line)
		userData.append(user)

	# create characteristic sets
	characteristic = createCharacteristicSets(userData, dict())

	# find top-5-similar-users candidates for each users
	topFiveDict = {}
	for pair in candidateList:
		# pair[0]/pair[1]'s Jaccard Similarity to user pair[1]/pair[0]
		jacSim = calulateJaccard(characteristic[pair[0]], characteristic[pair[1]])

		# create instances and insert into topFiveDict
		userA = UserNode(pair[0], jacSim)
		userB = UserNode(pair[1], jacSim)

		topFiveDict.setdefault(pair[0], [])
		topFiveDict[pair[0]].append(userB)

		topFiveDict.setdefault(pair[1], [])
		topFiveDict[pair[1]].append(userA)

	# ready for recommendation system output
	recommendationSystemOuput = []

	for user, topFiveCands in topFiveDict.items():
		# if top-5-similar-users candidates is less than 3, then we prune it
		if(len(topFiveCands) < 3):
			continue
		
		# sort top-5-similar-users in each corresponding user, sort in descending order by instances' Jaccard 
		topFiveDict[user].sort(key = operator.attrgetter("jaccard"), reverse = True)

		# find TRUE top 5 similar users among each user
		trueTopFiveList = []
		countTopFive = 0
		for i in range(0, len(topFiveCands)):
			countTopFive += 1;

			# consider 5th, 6th...so on, has the same Jaccard Similarity
			if(countTopFive > 5 and i > 0 and topFiveCands[i].jaccard != topFiveCands[i - 1].jaccard):
				break

			trueTopFiveList.append(topFiveCands[i].userName)

		
		# find a movie that has at least three users have watched
		movieBucketList = set()
		for threesome in combinations(trueTopFiveList, 3):
			localMovieBucketList = set()
			setUser = characteristic[ user ]
			setA = characteristic[ threesome[0] ]
			setB = characteristic[ threesome[1] ]
			setC = characteristic[ threesome[2] ]

			# find common movies among them -> intersection of three sets
			movieSet = setA & setB & setC
			# find movies that user hasn't watched -> union(setUser, movieSet) - setUser
			localMovieBucketList = (setUser | movieSet) - setUser

			# add recommened movies into movieBucketList
			for movie in localMovieBucketList:
				movieBucketList.add(movie);

		# store results
		if movieBucketList:
			result = [user, sorted(list(movieBucketList))]
			recommendationSystemOuput.append(result)

	# return result
	return recommendationSystemOuput

if __name__ == '__main__':
	lshOutput = []
	document = open(sys.argv[2])
	for line in document:
		candidatePair = json.loads(line)
		lshOutput.append(candidatePair)

	recommendationList = recommendationSystem(lshOutput)
	
	jenc = json.JSONEncoder()
	# print recommended movies for each user in recommendationList
	for pair in recommendationList:
		print jenc.encode(pair)
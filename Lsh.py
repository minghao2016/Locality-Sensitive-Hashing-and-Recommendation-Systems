from __future__ import division
import json
import sys
import re
import math
from itertools import combinations

def createCharacteristicSets(document, matrix):
	for user in document:
		matrix.setdefault(user[0], set(user[1]))
		# matrix[user[0]] = set(user[1])
	return matrix


def minHashFunction(oldRow, i):
	# minhash function - h(x,i) = (3x + i) % 100
	newRow = (3 * oldRow + i) % 100
	return newRow


def findMinRow(oldRst):
	# finding minimal row using one variable technique
	minRow = oldRst[0]
	for i in range(1, len(oldRst)):
		if minRow > oldRst[i]:
			minRow = oldRst[i]
	return minRow


def createSignatureSets(characteristic, matrix):
	for userName in characteristic:
		matrix.setdefault(userName, [])

	for i in range(1, 21):
		for userName, movieList in characteristic.items():
			permuteRst = []
			for movie in movieList:
				# permute rows, in this case, movies
				permuteRst.append(minHashFunction(movie, i))
			# insert new h value for current i
			matrix[userName].append(findMinRow(permuteRst))
	return matrix


def localitySensitveHashing(signature, candList):
	band = 1
	startRow = 0

	while band <= 5:
		candPairs = {}
		for userName, movieList in signature.items():
			# hash signature into bucket
			hashSig = tuple(movieList[startRow : startRow + 4])
			candPairs.setdefault(hashSig, [])
			candPairs[hashSig].append(userName)
		# check there is a pair agrees on all rows in this band
		for pair in candPairs.values():
			if len(pair) >= 2:
				pair.sort()
				for simUsers in combinations(pair, 2):
					# eliminate duplicate pairs
					if not candList.has_key(simUsers):
						candList.setdefault(simUsers, [])
		# move on to the next band
		band += 1
		startRow += 4

	return candList


def findSimilarUsers(userData):
	# create characteristic sets
	characteristic = createCharacteristicSets(userData, dict())

	# create signature matrix aka minhash
	signature = createSignatureSets(characteristic, dict())

	# apply locality-sensitive hashing to find candidate pairs
	candidates = localitySensitveHashing(signature, dict())

	return candidates

if __name__ == '__main__':
	userData = []
	document = open(sys.argv[1])
	for line in document:
		user = json.loads(line)
		userData.append(user)

	similarUsersRst = findSimilarUsers(userData)

	jenc = json.JSONEncoder()
        # print each pair in similarUsersRst
        for pair in similarUsersRst:
            print jenc.encode(pair)
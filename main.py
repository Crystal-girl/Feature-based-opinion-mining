
"""
The main code which runs the entire review analysis
"""

import sys
import HAC
import math
import FileCreationWithBigrams
import AdjScore
import operator
import collections
from textblob import TextBlob

#Get the review filename as command line argument
filename = sys.argv[1]

#reviewTitle is the list containing title of all reviews
reviewTitle = []

#reviewContent is the list containing all reviews
reviewContent = []

posCount = 0
negCount = 0
#Extract review title and content from the file
with open(filename) as f:
	review = []
	for line in f:
		if line[:6] == "[+][t]":							#Incase the line starts with [t], then its the title of review
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[+][t]")[1].rstrip("\r\n"))
			posCount = posCount + 1
		elif line[:6] == "[-][t]":							#Incase the line starts with [t], then its the title of review
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[-][t]")[1].rstrip("\r\n"))
			negCount = negCount + 1
		else:	
			if "##" in line:								#Each line in review starts with '##'
				x = line.split("##")
				for i in range(1, len(x)):			#x[0] is the feature given the file.Its been ignored here as its not a part of the review
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

#Creating a File attaching Bigrams
FileCreationWithBigrams.fileCreation(reviewContent,filename)

import MOS
import WithNgrams

#The HAC algorithm to extract features and adjectives in the review
adjDict = HAC.findFeatures(reviewContent,filename)
featureList = WithNgrams.final()

#Get adjective scores for each adjective
adjScores = AdjScore.getScore(adjDict,filename)

#MOS algorithm to get feature score and review score
posRevIndex, negRevIndex, avgFeatScore = MOS.rankFeatures(adjScores, featureList, reviewTitle, reviewContent)

<<<<<<< HEAD
total = posCount + negCount

print "Number of Wrong Classifications are " , abs(negCount-len(negRevIndex)) , " out of " , total

count = abs(negCount-len(negRevIndex))


print "Accuracy " , (total-count)*100.0/total


=======
with open('featureScore.txt', 'w') as fp:
    fp.write('\n'.join('%s, %s' % x for x in avgFeatScore))
>>>>>>> a09fe9531883889628154fb183837ae28a7a4180

with open('positiveReviews.txt', 'w') as fp:
	for x, y in posRevIndex.items():
		fp.write('[t] ' + reviewTitle[x] + '\n' + '[r] ' + ''.join(reviewContent[x]) + '\n\n')

with open('negativeReviews.txt', 'w') as fp:
	for x, y in negRevIndex.items():
		fp.write('[t] ' + reviewTitle[x] + '\n' + '[r] ' + ''.join(reviewContent[x]) + '\n\n')

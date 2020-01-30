'''Python Code to get the optimal weights needed for testing on the test set'''

from random import *
import numpy as np
import math
import csv

def classprob(score, count, y):
	corr_op = int(y)
	value = 1/(1+math.exp(-score))
	if value > 0.5:
		if corr_op == 1:
			count += 1
		return "POS", count
	else:
		if corr_op == 0:
			count += 1
		return "NEG", count

def sigmoid(z):
	return (1/(1+math.exp(-z)))

def train_data(features, weights, y):
	n = 0.1
	
	z = np.dot(weights,features)						# (w.x + b)
	loss = sigmoid(z) - y								#Calculate Loss
	g = loss * features									#Calculate Gradient
	weights = weights - n*g 							#New Weights calculated

	return weights


weights = np.zeros(7)									#x1,x2,x3,x4,x5,x6,b

with open("Bhat-Krithika-assgn2-part1.csv", newline="") as csv_file:
	review_reader = list(csv.reader(csv_file))

	positive_reviews = [x for x in review_reader if x[7] == '1']
	negative_reviews = [x for x in review_reader if x[7] == '0']

	shuffle(positive_reviews)
	shuffle(negative_reviews)

	training_data, test_data = positive_reviews[:85], positive_reviews[85:]
	training_data.extend(negative_reviews[:85])
	test_data.extend(negative_reviews[85:])

	shuffle(training_data)
	shuffle(test_data)

	for i in range(0,100000):
		rand = randint(0,151)
		review_id, features, y = training_data[rand][0], np.array(training_data[rand][1:7],dtype="float"), float(training_data[rand][-1])
		features = np.append(features,1)
		weights = train_data(features, weights, y)

	count = 0

	for vector in test_data:
		review_id, features, y = vector[0], np.array(vector[1:len(vector)-1],dtype="float"), float(vector[-1])
		features = np.append(features,1)
		sent_class, count = classprob(np.dot(weights,features),count, y)
		print(review_id, sent_class, y)

print("Efficiency: ",(count*100)/(len(test_data)))
print("Weights:", weights)
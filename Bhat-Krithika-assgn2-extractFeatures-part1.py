'''Python Code to extract features from the training set, for both positive and negative reviews'''

from collections import Counter
import re
import math
import csv

#Function to extract count of positive words
def positive_count(review, pos_count):
	with open('positive-words.txt','r') as f:
		contents = f.read()
		wc = Counter(re.findall(r"\b[a-zA-Z-']+\b", review))

		for key,value in wc.items():
			pattern = re.compile(r'\s\b{0}\b\s'.format(key))

			if re.search(pattern,contents):
				pos_count += value
	return pos_count

#Function to extract count of negative words
def negative_count(review, neg_count):
	with open('negative-words.txt','r') as f:
		contents = f.read()
		wc = Counter(re.findall(r"\b[a-zA-Z-']+\b", review))

		for key,value in wc.items():
			pattern = re.compile(r'\s\b{0}\b\s'.format(key))

			if re.search(pattern,contents):
				neg_count += value

	return neg_count

#Function to check if 'no' exists in review
def check_for_no(review):
	pattern = re.compile(r'\s\bno\b\s')

	if re.search(pattern,review):
		return 1
	else:
		return 0

#Function to check for pronouns
def check_pronouns(review, pronouns):
	wc = Counter(re.findall(r"\b[a-zA-Z-']+\b", review))
	count = 0

	for key,value in wc.items():
		if key in pronouns:
			count += value

	return count

#Function to check for '!'
def check_for_ex(review):
	pattern = re.compile(r'!')

	if re.search(pattern,review):
		return 1
	else:
		return 0

#Fucntion to get log of word count
def log_count(review):
	res = re.findall(r"\b[a-zA-Z0-9-']+\b", review)
	length = len(res)
	return round(math.log(length),2)

#Function to extract all features
def extract_features(review, features):

	review = review.lower()
	pos_count = 0
	neg_count = 0
	pronouns = ["i", "me", "mine", "my", "you", "your", "yours", "we", "us", "ours"]

	features.append(positive_count(review,pos_count))
	features.append(negative_count(review,neg_count))
	features.append(check_for_no(review))
	features.append(check_pronouns(review,pronouns))
	features.append(check_for_ex(review))
	features.append(log_count(review))

	return features


review_features = []
with open("hotelPosT-train.txt", encoding="utf8") as pos_file:
	pos_reviews = pos_file.readlines()

	for line in pos_reviews:
		id_rev, review = line.split('\t')
		features = [id_rev]
		features = extract_features(review, features)
		features.append(1)
		review_features.append(features)

pos_file.close()

with open("hotelNegT-train.txt",encoding="utf8") as neg_file:
	neg_reviews = neg_file.readlines()

	for line in neg_reviews:
		id_rev, review = line.split('\t')
		features = [id_rev]
		features = extract_features(review, features)
		features.append(0)
		review_features.append(features)

neg_file.close()

with open("Bhat-Krithika-assgn2-part1.csv", "w", newline="") as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(review_features)

csv_file.close()
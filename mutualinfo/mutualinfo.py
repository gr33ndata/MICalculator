# This is a stand-alone implementation for Mutual Information
# In probability theory and information theory, the mutual information of two variables
# is a quantity that measures the mutual dependence of the two random variables.
# It is used in Machine Learning (Classification) as a way for feature-selection.

# Author: Tarek Amr <@gr33ndata> 

import os, math
from preprocessor import Preprocessor

class MutualInformation:
	
	def __init__(self, files_path='', classes={}, out_file='output.csv'):
		# self.mi_terms looks like this {'term1': {'d': 3, 't': 4, 'mi': 2, },}
		self.mi_terms = {}
		# self.mi_classes looks like this {'d': 3, 't': 4}
		self.mi_classes = {}
		self.total_terms_count = 0
		# Some configuration
		self.files_path = files_path
		self.out_file = out_file
		self.classes = classes
		self.files_prefixes = classes.keys()
		self.class_names = [classes[prefix] for prefix in classes]
		# For tokenizing, stemming, etc.
		self.prep = Preprocessor(pattern='\W+', lower=True, stem=False, stemmer_name='porter', pos=False, ngram=1)
	
	# Read terms from files, and fill self.mi_terms & self.mi_classes
	def load_terms(self):
		files = os.listdir(self.files_path)
		for filename in files:
			#print filename
			terms = []
			file_prefix = ''
			if filename.startswith(self.files_prefixes[0]):
				file_prefix = self.files_prefixes[0]
 			elif filename.startswith(self.files_prefixes[1]):
				file_prefix = self.files_prefixes[1]
			else:
				continue
			fd = open('%s/%s' % (self.files_path, filename), 'r')
			file_data = fd.read()
			fd.close()
			terms = self.prep.ngram_tokenizer(text=file_data)
			for term in terms:
				self.total_terms_count += 1
				if not self.mi_terms.has_key(term):
					self.mi_terms[term] = {self.files_prefixes[0]: 0, self.files_prefixes[1]: 0}
				self.mi_terms[term][file_prefix] += 1
				if self.mi_classes.has_key(file_prefix):
					self.mi_classes[file_prefix] += 1
				else:
					self.mi_classes[file_prefix] = 0
		print self.mi_classes

	# Term probablility
	def pr_term(self, term):
		term_count = self.mi_terms[term][self.files_prefixes[0]] + self.mi_terms[term][self.files_prefixes[1]]
		total_count = self.mi_classes[self.files_prefixes[0]] + self.mi_classes[self.files_prefixes[1]]
		return term_count * 1.00 / total_count

	# Class probability
	def pr_class(self, class_prefix):
		class_count = self.mi_classes[class_prefix]
		total_count = self.mi_classes[self.files_prefixes[0]] + self.mi_classes[self.files_prefixes[1]]
		return class_count * 1.00 / total_count

	# Posterior Probability Pr(term/class)
	def pr_post(self, term, class_prefix):
		term_count = self.mi_terms[term][class_prefix]
		total_count = self.mi_classes[class_prefix]
		return term_count * 1.00 / total_count

	# Joint Probability Pr(term, class)
	def pr_joint(self, term, class_prefix):
		return self.pr_post(term, class_prefix) * self.pr_class(class_prefix)

	# Q = 1- P
	def q(self, p):
		return (1 - p)

	# Calculate Mutual Information
	def calculate_mi(self):
		for term in self.mi_terms:
			mi = 0.0
			for class_prefix in self.files_prefixes:
				try:
					mi += self.pr_joint(term, class_prefix) * math.log10(self.pr_post(term, class_prefix) / self.pr_term(term))
					mi += self.q(self.pr_joint(term, class_prefix)) * math.log10(self.q(self.pr_post(term, class_prefix)) / self.q(self.pr_term(term)))
				except:
					# Ok, log(0), let's set mi = -1
					mi = 0
			self.mi_terms[term]['mi'] = mi

	# Dump results into a CSV File
	def mi2csv(self): 
		fd = open(self.out_file , 'w')
		header_line = "Term, %s, %s, Mutual Info\n" % (self.classes[self.files_prefixes[0]], self.classes[self.files_prefixes[1]])
		fd.write(header_line)
		for term in self.mi_terms:
			new_line = '%s, %f, %f, %f\n' % (term, self.mi_terms[term][self.files_prefixes[0]], 
						self.mi_terms[term][self.files_prefixes[1]], self.mi_terms[term]['mi'])
			fd.write(new_line)
		fd.close()	

if __name__ == '__main__':

	# Path to our data files
	my_path = '../all-folds/fold1'

	# We need to tell it which file prefix is tied to which class
	# {'s':'Spam', 'h': 'Ham'} => 
	# 	All files staring with s will be considered as Spam dataset
	#	All files staring with h will be considered as Ham dataset
	my_classes = {'a': 'Apple', 'n': 'Nokia'}

	mi = MutualInformation(files_path=my_path, classes=my_classes)
	mi.load_terms()
	mi.calculate_mi()
	mi.mi2csv()


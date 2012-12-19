# Mutual Information Calculator #

Calculates Mutual Information and dump results in a CSV file.
Let's say you have some files, each belong to a certain class (Machine Learning classes). Now you want to find the top terms in those files w.r.t. Mutual Information.

You then do the following

	# Path to our data files
	my_path = '/folders-path/folder-name/'

	# We need to tell it which file prefix is tied to which class
	# {'s':'Spam', 'h': 'Ham'} => 
	# 	All files staring with s will be considered as Spam dataset
	#	All files staring with h will be considered as Ham dataset
	# Files in my_path should start with s and h accordingly 
	my_classes = {'s': 'Spam', 'h': 'Ham'}

	mi = MutualInformation(files_path=my_path, classes=my_classes)
	mi.load_terms()
	mi.calculate_mi()
	
	# Will dump output in a csv file	
	mi.mi2csv()


# Contacts #
 
+ Name: Tarek Amr
+ Twitter: @gr33ndata
 


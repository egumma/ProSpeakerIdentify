import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture #GMM http://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
from featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
import os
import time
warnings.filterwarnings("ignore")

#path to training data
source   = "store/trainingData/"

#path to training data
sourceTest   = "store/sampleData/"

#path where training speakers will be saved
dest = "store/speakers_models/"
#train_file = "trainingDataPath.txt"        
#file_paths = open(train_file,'r')


# Extracting features for each speaker (5 files per speakers)
def trainDataByPerson(personID):
	directory_path = source+personID+"-001/"
	print ("---->Training data path :"+directory_path)
	features = np.asarray(())
	count = 1
	file_paths = os.listdir(directory_path)
	for path in file_paths:    
		path = path.strip()   
		print (path);
		
		# read the audio
		sr,audio = read(directory_path + path)
		
		# extract 40 dimensional MFCC & delta MFCC features
		vector   = extract_features(audio,sr)
		
		if features.size == 0:
			features = vector
		else:
			features = np.vstack((features, vector))
		# when features of 5 files of speaker are concatenated, then do model training
		# -> if count == 5: --> edited below
		if count == 4:
			#gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag',n_init = 3)
			gmm = GaussianMixture(n_components = 16, covariance_type='diag',n_init = 3)
			gmm.fit(features)
			
			# dumping the trained gaussian model
			#picklefile = path.split("-")[0]+".gmm" Edu commented
			picklefile = path.split("_")[0] + ".gmm"
			pickle.dump(gmm,open(dest + picklefile,'w'))
			print ('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)    
			features = np.asarray(())
			count = 0
		count = count + 1

def verifyVoiceByPerson(personID):
	path = personID+"_test.wav"
	print ("---->Verify voice file :"+path)

	gmm_files = [os.path.join(dest, fname) for fname in
				 os.listdir(dest) if fname.endswith('.gmm')]

	# Load the Gaussian gender Models
	models = [pickle.load(open(fname, 'r')) for fname in gmm_files]
	speakers = [fname.split("/")[-1].split(".gmm")[0] for fname
				in gmm_files]

	error = 0
	total_sample = 0.0

	print "Testing Audio : ", path
	total_sample += 1.0
	path = path.strip()
	print "Single File Test Audio : ", path
	sr,audio = read(sourceTest + path)
	vector   = extract_features(audio,sr)

	log_likelihood = np.zeros(len(models))

	for i in range(len(models)):
		gmm    = models[i]  #checking with each model one by one
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()

	winner = np.argmax(log_likelihood)
	print "\tSingle File detected as - ", speakers[winner]

	checker_name = path.split("_")[0]
	if speakers[winner] != checker_name:
		error += 1

	time.sleep(1.0)

	print error, total_sample
	accuracy = ((total_sample - error) / total_sample) * 100

	print "The Accuracy Percentage for the current testing Performance with MFCC + GMM is : ", accuracy, "%"
	return (True if accuracy == 100.0 else False)



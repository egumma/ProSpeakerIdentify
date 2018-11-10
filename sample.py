from pathlib import Path
import os


# Create target Directory if don't exist
def ensure_dir(dirName):
	if not os.path.exists(dirName):
		os.mkdir(dirName)
		print("Directory " , dirName ,  " Created ")
	else:    
		print("Directory " , dirName ,  " already exists")

arr = os.listdir("store/trainingData/ProCreate-001")
print "Files list :: ", arr;

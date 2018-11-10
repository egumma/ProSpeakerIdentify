#app.py


from flask import Flask, request, render_template, redirect, Response, url_for, flash
#import main Flask class and request object
from werkzeug.utils import secure_filename

import random, json
import os
import datetime
import time
import modeltraining_pro as training
#from pathlib import Path

UPLOAD_FOLDER_TRAIN = 'store/trainingData'
UPLOAD_FOLDER_VERIFY = 'store/sampleData'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav'])

app = Flask(__name__) #create the Flask app
app.config['UPLOAD_FOLDER_TRAIN'] = UPLOAD_FOLDER_TRAIN
app.config['UPLOAD_FOLDER_VERIFY'] = UPLOAD_FOLDER_VERIFY



@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='ProCreate')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	result = ''
    
	for item in data:
		# loop over every row
		result += str(item['make']) + '\n'

	return result

# ProCreate custom logic
@app.route('/voice-record', methods=['GET'])
def voice_record():
	# serve index template
	return render_template('voice_record.html', person_id='ProCreate')

#<!doctype html>
#<title>Upload new File</title>
#<h1>Upload new File</h1>
#<form method=post action="http://127.0.0.1:5000/upload_user_voice" enctype=multipart/form-data>
#  <p><input type=file name=file>
#	 <input type=submit value=Upload>
#</form>	
@app.route('/upload_user_voice', methods=['GET', 'POST'])
def upload_user_voice():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'audio_data' not in request.files:
			print("--->No file part")
			flash('No file part')
			return redirect(request.url)
		file = request.files['audio_data']
        # if user does not select file, browser also
        # submit a empty part without filename		
		print("--->File received to store : ", file.filename)
		if file.filename == '':
			print("--->No selected file")
			flash('No selected file')
			return redirect(request.url)	
		print("--->Allowed file extension : ", allowed_file(file.filename))
		if file and allowed_file(file.filename):
			print("--->File saving to location")
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER_TRAIN'], filename))
			#return redirect(url_for('upload_user_voice', filename=filename))
			return '''<br/><b>Upload data received....! </b>'''
		
		return '''Unable to upload data received....! '''


@app.route('/upload_user_train_voice', methods=['GET', 'POST'])
def upload_user_train_voice():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'audio_data' not in request.files:
			print("--->No file part")
			flash('No file part')
			return redirect(request.url)
		file = request.files['audio_data']
        # if user does not select file, browser also
        # submit a empty part without filename		
		print("--->Voice received to store : ", file.filename)
		
		if file.filename == '':
			print("--->No selected file")
			flash('No selected file')
			return redirect(request.url)	
		print("--->Allowed file extension : ", allowed_file(file.filename))
		if file and allowed_file(file.filename):
			#Get personid from the uploaded file
			personid = file.filename.split('.')[0];
			
			#Get date with timestamp
			timeNow = time.time()
			datetimeNow = ""+datetime.datetime.fromtimestamp(timeNow).strftime('%Y-%m-%d %H:%M:%S')
			datetimeNow = datetimeNow.replace(" ", "-")
			
			filename = personid +"_"+ datetimeNow +".wav";
			filename = secure_filename(filename) #46068_2018-11-04-201010.wav
			
			#Use existing or create new folder for each invidual person
			ensure_dir(app.config['UPLOAD_FOLDER_TRAIN']+"/"+personid +"-001")
			
			print("--->Voice saving to location :"+app.config['UPLOAD_FOLDER_TRAIN']+"/"+personid +"-001"+"/"+filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			file.save(app.config['UPLOAD_FOLDER_TRAIN']+"/"+personid +"-001"+"/"+filename)
			#return redirect(url_for('upload_user_voice', filename=filename))
			responseTxt = '''<font color=green>Voice Uploaded - </font>''' +filename
			return responseTxt
		
		return '''<font color=red>Failed Voice upload</font> '''


@app.route('/upload_user_verify_voice', methods=['GET', 'POST'])
def upload_user_verify_voice():
	if request.method == 'POST':

		if 'audio_data' not in request.files:
			print("--->No file part")
			return redirect(request.url)
		file = request.files['audio_data']
		print("--->Verify Voice received to store : ", file.filename)

		if file.filename == '':
			print("--->No selected file")
			return redirect(request.url)

		if file and allowed_file(file.filename):
			personid = file.filename.split('.')[0];
			filename = personid + "_test.wav";
			filename = secure_filename(filename)  # 46068_test.wav
			print("--->Verify Voice saving to location :" + app.config['UPLOAD_FOLDER_VERIFY'] + "/" + filename)
			file.save(app.config['UPLOAD_FOLDER_VERIFY'] +"/"+ filename)
			responseTxt = '''<font color=green>Verify Voice uploaded - </font>''' +filename
			return responseTxt

		return '''<font color=red>Failed Verify Voice Upload</font> '''


@app.route('/train_user_voice', methods = ['POST', 'GET'])
def train_user_voice():
	personid = request.args['person_id']
	# print("--->personid : ", personid)
	training.trainDataByPerson(personid);
	result = personid +'''<font color=green>: Voice training success </font>'''
	
	return result


@app.route('/verify_user_voice', methods=['POST', 'GET'])
def verify_user_voice():
	personid = request.args['person_id']
	# print("--->personid : ", personid)
	isValidVoice = training.verifyVoiceByPerson(personid);
	print(personid ,' - Voice verification status ', isValidVoice)

	return "Success" if isValidVoice else "Failure"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
		   

# Create target directory if don't exist
def ensure_dir(dirName):
	if not os.path.exists(dirName):
		os.mkdir(dirName)
		print("Directory " , dirName ,  " Created ")
	else:    
		print("Directory " , dirName ,  " already exists")
		   
		   
if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000

#import sample as s
import modeltraining_pro as training

print "------>I am sample 1";

#s.ensure_dir("store/trainingData")
print "------>Its communication success...!";

training.trainDataByPerson("46068");
print "------>Model training success...!";



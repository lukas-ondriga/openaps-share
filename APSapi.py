import json
import os
import datetime
import subprocess
from flask import Flask, request
from flask_restful import Resource, Api
from math import floor

OPENAPSROOT = os.environ['OPENAPSROOT']

app = Flask(__name__)
api = Api(app)


class TempTarget (Resource):

    def post(self):

	# Get JSON data
	
	json_data = [{}]
	json_data[0]['targetTop'] = request.form.get('targetTop');
	json_data[0]['targetBottom'] = request.form.get('targetBottom');
	json_data[0]['duration'] = request.form.get('duration');
	json_data[0]['created_at'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z");
	print json_data

	TEMPTARGETFILE = OPENAPSROOT+ "/settings/temptargets.json"
	with open(TEMPTARGETFILE, 'w') as outfile:
    	    json.dump(json_data, outfile)

	os.system('cd $OPENAPSROOT; openaps report invoke settings/profile.json &')
	return '', 200

api.add_resource(TempTarget, '/api/v1/temptarget')

class WakeUp (Resource):

    def post(self):

	json_data = {}
	json_data['units'] = 0.3;

	BOLUSFILE = OPENAPSROOT+ "/bolus/bolus.json"
	with open(BOLUSFILE, 'w') as outfile:
    	    json.dump(json_data, outfile)

    	subprocess.call('killall -g openaps', shell=True)
    	result = subprocess.call('cd $OPENAPSROOT; openaps use pump bolus bolus/bolus.json', shell=True)

	print result
	if result:
            return 'Unable to bolus!', 404 
	else:
	    return '', 200

api.add_resource(WakeUp, '/api/v1/wakeup')

class SuggestBolus (Resource):

    def post(self):

	carbs = request.form.get('carbs')
	print "Carbs: " + carbs + " g"

	IOBINPUT = OPENAPSROOT+ "/monitor/iob.json"
	with open(IOBINPUT) as iobfile:
    	    iob_data = json.load(iobfile)

	iob = iob_data[0]['iob']
	print "IOB: " + str(iob)

	AUTOSENSINPUT = OPENAPSROOT+ "/settings/autosens.json"
	with open(AUTOSENSINPUT) as autosensfile:
    	    autosens_data = json.load(autosensfile)

	autosens = autosens_data['ratio']
	print "Autosens ratio: " + str(autosens)

	PROFILEINPUT = OPENAPSROOT+ "/settings/profile.json"
	with open(PROFILEINPUT) as profilefile:
    	    profile_data = json.load(profilefile)

	carb_ratio = profile_data['carb_ratio']
	print "Carb ratio: " + str(carb_ratio)

	sensitivity = profile_data['sens']
	print "Sensitivity: " + str(sensitivity)

	min_bg = profile_data['min_bg']
	max_bg = profile_data['max_bg']
	target = (min_bg + max_bg)/2
	print "Target: " + str(target)

	MEALINPUT = OPENAPSROOT+ "/monitor/meal.json"
	with open(MEALINPUT) as mealfile:
    	    meal_data = json.load(mealfile)

	meal_cob = meal_data['mealCOB']
	print "Meal COB: " + str(meal_cob)

	GLUCOSEINPUT = OPENAPSROOT+ "/monitor/glucose.json"
	with open(GLUCOSEINPUT) as glucosefile:
    	    glucose_data = json.load(glucosefile)

	glucose = glucose_data[0]['glucose']
	print "Glucose: " + str(glucose)

	correction = ((glucose - target) / sensitivity) * autosens
	meal_correction  = float(meal_cob)/carb_ratio * autosens
	correction += meal_correction
	print "Correction: " + str(correction)
	meal_bolus = (float(carbs))/carb_ratio*autosens
	bolus = meal_bolus + correction - iob
	max_bolus = 60/carb_ratio
	bolus = min(bolus, max_bolus)
	correction = floor(correction*10)/10
	bolus = floor(bolus*10)/10
	meal_bolus = floor(meal_bolus*10)/10
	iob = floor(iob*10)/10
	print "Bolus: " + str(bolus)

	json_data = {}
	json_data['units'] = bolus;

    	subprocess.call('killall -g openaps', shell=True)

	BOLUSFILE = OPENAPSROOT+ "/bolus/bolus.json"
	with open(BOLUSFILE, 'w') as outfile:
    	    json.dump(json_data, outfile)

	json_data = [{}]
	json_data[0]['carbs'] = carbs;
	json_data[0]['created_at'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z");

	CARBSFILE = OPENAPSROOT+ "/bolus/carbshistory.json"
	with open(CARBSFILE, 'w') as outfile:
    	    json.dump(json_data, outfile)

	json_status = {}
	json_status['content'] = "Bolus: " + str(bolus) + "\nIOB: " + str(iob) + "\nCorrection: " + str(correction) + "\nMeal Bolus: " + str(meal_bolus)
	json_status['font'] = 5

	SUGGESTFILE = OPENAPSROOT+ "/upload/index.html"
	with open(SUGGESTFILE, 'w') as suggestfile:
    	    json.dump(json_status, suggestfile)

 #   	result = subprocess.call('cd $OPENAPSROOT; openaps use pump bolus bolus/bolus.json', shell=True)

	return '', 200

api.add_resource(SuggestBolus, '/api/v1/suggestbolus')

class EnactBolus (Resource):

    def post(self):

    	result = subprocess.call('cd $OPENAPSROOT; openaps use pump bolus bolus/bolus.json', shell=True)
    	subprocess.call('cd $OPENAPSROOT; rm bolus/bolus.json', shell=True)

	if result:
            return 'Unable to bolus!', 404 
	else:
	    return '', 200

api.add_resource(EnactBolus, '/api/v1/enactbolus')

class CancelBolus (Resource):

    def post(self):
    	result = subprocess.call('cd $OPENAPSROOT; rm bolus/bolus.json', shell=True)
	if result:
            return 'Unable to bolus!', 404 
	else:
	    return '', 200

api.add_resource(CancelBolus, '/api/v1/cancelbolus')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

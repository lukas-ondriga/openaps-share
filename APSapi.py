import json
import os
import datetime
from flask import Flask, request
from flask_restful import Resource, Api

TEMPTARGETFILE = os.environ['OPENAPSROOT']+ "/settings/temptargets.json"

app = Flask(__name__)
api = Api(app)

class TempTarget (Resource):

    def post(self):

	print "Creating temp target"
	print request.__dict__
	print request.form
	# Get JSON data
	
	json_data = [{}]
	json_data[0]['targetTop'] = request.form.get('targetTop');
	json_data[0]['targetBottom'] = request.form.get('targetBottom');
	json_data[0]['duration'] = request.form.get('duration');
	json_data[0]['created_at'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z");
	print json_data
	with open(TEMPTARGETFILE, 'w') as outfile:
    	    json.dump(json_data, outfile)

	os.system('cd $OPENAPSROOT; openaps report invoke settings/profile.json')
	print "Temporary target updated"
	return '', 200

api.add_resource(TempTarget, '/api/v1/temptarget')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

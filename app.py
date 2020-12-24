# app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import boto3
import key_config as keys
from flask_restful.representations import json

app = Flask(__name__)
CORS(app)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
                          aws_access_key_id=keys.ACCESS_KEY_ID,
                          aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                          aws_session_token=keys.AWS_SESSION_TOKEN
                          )

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='eventdatas',
    KeySchema=[
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        }

    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='eventdatas')

# Print out some data about the table.
print(table.item_count)

@app.route('/storedata', methods=['GET', 'POST'])
def storedata():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        for data in request.get_json():
            title = data['title']
            start = data['start']
            print(title)
            response = table.put_item(
                Item = {
                    'title':title,
                    'start':start,
                }
            )
            print("Put item succeeded")
            print(json.dumps(response, indent=4))
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')
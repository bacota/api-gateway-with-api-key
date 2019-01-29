import boto3
import configparser
import json
import os
import psycopg2

configBucket = os.environ['CONFIG_BUCKET_NAME']
configFile = os.environ['CONFIG_FILE_NAME']

def configInfo():
    s3 = boto3.client('s3')
    body = s3.get_object(Bucket=configBucket, Key=configFile)['Body']
    configData = body.read().decode('utf-8')
    parser = configparser.ConfigParser()
    parser.read_string(configData)
    return parser
    

config = configInfo()
apiKeyHeader = 'x-api-key'

def get_connection():
    #Check this in cloudwatch to verify that it's only called once per runtime
    print("Acquiring connection to the database")
    cfg = config['pg_db']
    username=cfg['username']
    password=cfg['password']
    database=cfg['database']
    host=cfg['host']
    return psycopg2.connect(dbname=database, user=username, password=password, host=host)

#This should hang around between invocations
connection = get_connection()

def lambda_handler(event, context):
    headers = event['headers'] 
    if not apiKeyHeader in headers:
        return {
            'statusCode': 400,
            'body': "No api key found"
        }
    apiKey = headers[apiKeyHeader]
    #If this throws an error, we should try to get another connection
    cursor = connection.cursor()
    cursor.execute(f"select id from api_key_test where api_key='{apiKey}'")
    #Shoudl probably return 403 of zero rows are found
    id = cursor.fetchone()
    return {
        'statusCode': 200,
        'body': f"Retieved id {id}"
    }

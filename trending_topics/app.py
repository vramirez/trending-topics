##TO DO
## ADD TO GIT
## ADD S3 PERMISSIONS IN THE TEMPLATE (NO FUCKING IDEA)

import json
from twython import Twython
import boto3
import datetime
import os


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    API_KEY=os.environ['API_KEY']
    API_SECRET=os.environ['API_SECRET']
    ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
    ACCESS_SECRET=os.environ['ACCESS_SECRET']
    IDS=os.environ['IDS']
    s3 = boto3.resource('s3')
    bucket_name = "vicdata"
    
    tw =Twython(API_KEY, API_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    cur_date=datetime.datetime.now()
    for wid in IDS.split(','):
        resp=tw.get_place_trends(id=wid)
        file_name = "trends_"+cur_date.strftime('%Y%m%d_%H%M')+"_"+wid+".json"
        s3_path = "trends/" + file_name
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=bytes(json.dumps(resp[0]).encode('UTF-8')))    
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            #"date":cur_date.isoformat(),
            #"out":resp[0]  ,
            "message2": "chao world"
                     
            # "location": ip.text.replace("\n", "")
        }),
    }

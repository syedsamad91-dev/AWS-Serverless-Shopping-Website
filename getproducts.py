import json
import boto3
from decimal import Decimal

def decimal_to_native(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Products')

    response = table.scan()
    items = decimal_to_native(response.get('Items', []))

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items)
    }

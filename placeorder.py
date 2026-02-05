import json
import uuid
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    if not event.get("body"):
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Missing request body"})
        }

    body = json.loads(event["body"])

    order_id = str(uuid.uuid4())

    item = {
        "orderId": order_id,
        "customerName": body["customerName"],
        "productId": body["productId"],
        "productName": body["productName"],
        "quantity": int(body["quantity"]),
        "price": Decimal(str(body["price"]))
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        "body": json.dumps({
            "message": "Order placed successfully!",
            "orderId": order_id
        })
    }

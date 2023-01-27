import boto3


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('triangles')
        items = table.scan()
        return items["Items"]
        
    except Exception:
        return []
        
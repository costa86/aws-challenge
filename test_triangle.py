import boto3
from moto import mock_dynamodb
from create import lambda_handler as triagle_create, get_response
from history import lambda_handler as triangle_history
from http import HTTPStatus
import unittest

STATUS = "status"
LENGTHS = "lenghts"
SUCCESS = "success"
STATUS_CODE = "status_code"
MESSAGE = "message"
ERROR = "error"


@mock_dynamodb
class TestTriangle(unittest.TestCase):
    def setUp(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.dynamodb.create_table(
            TableName="triangles",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        self.context = {}

    def test_create_equilateral(self):

        event = {LENGTHS: [4, 4, 4]}
        result = triagle_create(event, self.context)

        self.assertEqual(result[STATUS], SUCCESS)
        self.assertEqual(result[STATUS_CODE], HTTPStatus.CREATED)
        self.assertEqual(result[MESSAGE], "equilateral")

    def test_create_scalene(self):

        event = {LENGTHS: [3, 5, 4]}
        result = triagle_create(event, self.context)

        self.assertEqual(result[STATUS], SUCCESS)
        self.assertEqual(result[STATUS_CODE], HTTPStatus.CREATED)
        self.assertEqual(result[MESSAGE], "scalene")

    def test_create_isosceles(self):

        event = {LENGTHS: [3, 4, 4]}
        result = triagle_create(event, self.context)

        self.assertEqual(result[STATUS], SUCCESS)
        self.assertEqual(result[STATUS_CODE], HTTPStatus.CREATED)
        self.assertEqual(result[MESSAGE], "isosceles")

    def test_invalid_shape(self):

        event = {LENGTHS: [1, 4, 10]}
        result = triagle_create(event, self.context)

        self.assertEqual(result[STATUS], ERROR)
        self.assertEqual(result[STATUS_CODE], HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_history(self):

        table = self.dynamodb.Table("triangles")
        table.put_item(Item={"id": "1", "t_type": "isosceles", "lenghts": [1, 1, 1]})
        table.put_item(Item={"id": "2", "t_type": "isosceles", "lenghts": [1, 1, 1]})

        event = {}
        result = triangle_history(event, self.context)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "1")
        self.assertEqual(result[1]["id"], "2")

    def test_get_response(self):
        self.assertEqual(
            get_response(),
            {STATUS: SUCCESS, MESSAGE: "ok", STATUS_CODE: HTTPStatus.OK},
        )
        self.assertEqual(
            get_response(False, ERROR),
            {STATUS: ERROR, MESSAGE: ERROR, STATUS_CODE: HTTPStatus.OK},
        )
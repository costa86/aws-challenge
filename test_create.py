import boto3
from moto import mock_dynamodb
from .create import lambda_handler as triagle_create
from .history import lambda_handler as triangle_history
from http import HTTPStatus
import unittest


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

    def test_create_equilateral(self):

        event = {"lenghts": [4, 4, 4]}
        context = {}
        result = triagle_create(event, context)

        assert result["status"] == "success"
        assert result["status_code"] == HTTPStatus.CREATED
        assert result["message"] == "equilateral"

    def test_create_scalene(self):

        event = {"lenghts": [3, 5, 4]}
        context = {}
        result = triagle_create(event, context)

        assert result["status"] == "success"
        assert result["status_code"] == HTTPStatus.CREATED
        assert result["message"] == "scalene"

    def test_create_isosceles(self):

        event = {"lenghts": [3, 4, 4]}
        context = {}
        result = triagle_create(event, context)

        assert result["status"] == "success"
        assert result["status_code"] == HTTPStatus.CREATED
        assert result["message"] == "isosceles"

    def test_invalid_shape(self):

        event = {"lenghts": [1, 4, 10]}
        context = {}
        result = triagle_create(event, context)

        assert result["status"] == "error"
        assert result["status_code"] == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_history(self):

        table = self.dynamodb.Table("triangles")
        table.put_item(Item={"id": "1", "t_type": "isosceles", "lenghts": [1,1,1]})
        table.put_item(Item={"id": "2", "t_type": "isosceles", "lenghts": [1,1,1]})

        event = {}
        context = {}
        result = triangle_history(event, context)

        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["id"] == "2"


import boto3
from pydantic import BaseModel, PositiveFloat, Field, ValidationError, validator
import uuid
from http import HTTPStatus
from datetime import datetime


DYNAMO_DB = boto3.client("dynamodb")
TABLE_NAME = "triangles"
TRIANGLE_SIDES = 3

class Triangle(BaseModel):
    lenghts: list[PositiveFloat] = Field(max_items=TRIANGLE_SIDES, min_items=TRIANGLE_SIDES)

    def get_type(self) -> str:
        unique_values = len(set(self.lenghts))
        return (
            "equilateral"
            if unique_values == 1
            else "scalene"
            if unique_values == TRIANGLE_SIDES
            else "isosceles"
        )

    @validator('lenghts')
    def must_be_valid_shape(cls, v):
        first, second, third = v
        if (first + second) < third or (first + third) < second or (second + third) < first:
            raise ValueError('invalid triangle shape')
        return v

    def save(self, db = DYNAMO_DB, table_name: str = TABLE_NAME):
        triangle_id = str(uuid.uuid1())
        created_at = datetime.now().isoformat()[:-7]
    
        db.put_item(
            TableName=table_name,
            Item={
                "id": {"S": triangle_id},
                "created_at": {"S": created_at},
                "lenghts": {"L": [{"N": str(i)} for i in self.lenghts]},
                "t_type": {"S": self.get_type()},
            },
        )


def get_response(success: bool = True, message: str = "ok", status_code: int = HTTPStatus.OK) -> dict:
    return {
        "status": "success" if success else "error",
        "message": message,
        "status_code": status_code,
    }


def lambda_handler(event, context):
    try:
        triangle = Triangle(**event)
        triangle.save()
        return get_response(True, triangle.get_type(), HTTPStatus.CREATED)

    except ValidationError as e:
        return get_response(False, f"validation failed: {e}", HTTPStatus.UNPROCESSABLE_ENTITY)

    except Exception:
        return get_response(False, "could not process request", HTTPStatus.BAD_REQUEST)

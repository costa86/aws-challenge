## Description
This project consists of a REST API to validate triangle types.
The types can be:

| Type       | Description                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------|
| Equilateral | All three sides are of equal length.                                                                                    |
| Isosceles   | Two sides are of equal length.                                                                                         |
| Scalene     | No sides are of equal length.                                                     |


## Usage and documentation
The project is deployed to AWS. Click [here](https://documenter.getpostman.com/view/22809238/2s8ZDeUz3r#e2800e17-50f3-4609-b41f-603039dc7340) for a description of the endpoints.

## Testing
>An activated python virtual environment is recommended
### Install dependencies

    pip install -r requirements.txt

### Run tests
    python -m unittest

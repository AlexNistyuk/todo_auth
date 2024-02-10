import pytest
import schemathesis

from main import app

app.openapi_version = "3.0.0"
schema = schemathesis.from_dict(app.openapi())


@pytest.mark.schemathesis
@schema.parametrize()
def test_api(case):
    response = case.call_asgi(app)
    case.validate_response(response)

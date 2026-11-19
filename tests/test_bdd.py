from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from app import create_app


feature_file = Path(__file__).resolve().parent / "features" / "szamosszegzo.feature"
scenarios(str(feature_file))


@given("egy üres számösszegző", target_fixture="client")
def empty_calculator():
    return create_app().test_client()

@when(parsers.parse("beküldöm a {number:d} egész számot"))
def submit_integer(client, number):
    response = client.post("/api/numbers", json={"number": number})
    assert response.status_code == 201


@when("beküldök egy tört számot", target_fixture="submission_response")
def submit_fraction(client):
    return client.post("/api/numbers", json={"number": 2.5})


@then("a beküldés 400-as hibakódot ad")
def check_rejection(submission_response):
    assert submission_response.status_code == 400


@when("lekérdezem az összeget", target_fixture="sum_response")
def request_sum(client):
    return client.get("/api/sum")


@then(parsers.parse("az összeg {expected:d}"))
def check_sum(sum_response, expected):
    assert sum_response.status_code == 200
    assert sum_response.get_json() == {"sum": expected}

@given(
    parsers.parse("a számösszegző már tárol két számot: {first:d} és {second:d}"),
    target_fixture="client",
)
def calculator_with_stored_numbers(first, second):
    client = create_app().test_client()

    for number in (first, second):
        response = client.post("/api/numbers", json={"number": number})
        assert response.status_code == 201

    return client

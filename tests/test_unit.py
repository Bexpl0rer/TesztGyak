from app import add_number, get_total


def test_add_number_appends_number_and_returns_updated_sum():
    numbers = [4, 6]

    total = add_number(numbers, -3)

    assert numbers == [4, 6, -3]
    assert total == 7


def test_get_total_returns_zero_for_empty_list():
    assert get_total([]) == 0


def test_get_total_sums_positive_and_negative_numbers():
    assert get_total([8, -3, 2]) == 7


def test_add_number_accepts_duplicate_number():
    numbers = [5]

    total = add_number(numbers, 5)

    assert numbers == [5, 5]
    assert total == 10


def test_get_total_can_return_negative_sum():
    numbers = [2, -6, -3]

    assert get_total(numbers) == -7

from app import create_app


def test_post_number_rejects_fraction_without_changing_sum():
    client = create_app().test_client()

    valid_response = client.post("/api/numbers", json={"number": 5})
    assert valid_response.status_code == 201

    invalid_response = client.post("/api/numbers", json={"number": 2.5})

    assert invalid_response.status_code == 400
    assert client.get("/api/sum").get_json() == {"sum": 5}
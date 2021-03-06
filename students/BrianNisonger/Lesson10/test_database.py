import os
import pytest

from database import Database
from database import MongoDBConnection
import pymongo


@pytest.fixture
def setup_db(request):
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.furniture
        db.product_data.drop()
        db.customer_data.drop()
        db.rental_data.drop()
        files = ["customer_data.csv", "product_data.csv", "rental_data.csv"]
        test_import_result = [
            Database.import_data("dat", file) for file in files
        ]

        def cleanup():
            db.product_data.drop()
            db.customer_data.drop()
            db.rental_data.drop()

        request.addfinalizer(cleanup)


@pytest.fixture
def test_import_data_results():
    return [(3, 0), (3, 0), (5, 0)]


@pytest.fixture
def _show_available_products():
    product_dict = {
        'prd1001': {
            'description': '60 inch TV stand',
            'product_type': 'livingroom',
            'quantity_available': 2
        },
        'prd1003': {
            'description': 'Hobart Stand Mixer',
            'product_type': 'kitchen',
            'quantity_available': 10
        }
    }
    return product_dict


@pytest.fixture
def _show_rentals():
    rental_dict = {
        'user1001': {
            'name': 'Elisa Miles',
            'address': '4490 Union Street',
            'phone_number': '206-922-0882',
            'email': 'elisa.miles@yahoo.com'
        },
        'user1002': {
            'name': 'Maya Data',
            'address': '4936 Elliot Avenue',
            'phone_number': '206-777-1927',
            'email': 'mdata@uw.edu'
        }
    }
    return rental_dict


def test_connection():
    with pytest.raises(AttributeError):
        mongo_test = MongoDBConnection(host='')
        with mongo_test:
            db = mongo_test.connection.furniture


def test_import_data(test_import_data_results):
    files = ["customer_data.csv", "product_data.csv", "rental_data.csv"]
    test_import_result = [Database.import_data("dat", file) for file in files]
    assert test_import_data_results == test_import_result


def test_calculate_availability():
    rental_list = [{
        "user": 1001,
        "product_id": "prd1001"
    }, {
        "user": 1002,
        "product_id": "prd1002"
    }]
    product_list = [{
        "product_id": "prd1001",
        "quantity_available": "10"
    }, {
        "product_id": "prd1002",
        "quantity_available": "2"
    }]
    product_calculated = Database.calculate_availability(
        product_list, rental_list)
    for product in product_calculated:
        if product["product_id"] == "prd1001":
            assert product["quantity_available"] == 9


def test_make_product_dict():
    product_dict_list = product_list = [{
        "product_id": "prd1001",
        "quantity_available": 10,
        "description": "blah",
        "product_type": "yes",
        "garbage_field": "yuck"
    }]
    assert Database.make_product_dict(product_dict_list) == {
        'prd1001': {
            "description": "blah",
            "product_type": "yes",
            "quantity_available": 10
        }
    }
    product_dict_list = product_list = [{
        "product_id": "prd1001",
        "quantity_available": 0,
        "description": "blah",
        "product_type": "yes",
        "garbage_field": "yuck"
    }]
    assert Database.make_product_dict(product_dict_list) == {}


def test_return_user_ids():
    rental_list = rental_list = [{
        "user_id": '1001',
        "product_id": "prd1001"
    }, {
        "user_id": '1002',
        "product_id": "prd1002"
    }]
    assert Database.return_user_ids(rental_list) == ['1001', '1002']


def test_make_customer_dict():
    user_list = [{
        "user_id": "1001",
        "name": "Jim",
        "address": "1234",
        "phone_number": "555",
        "email": "something",
        "stuff": "stuff"
    }]
    assert Database.make_customer_dict(user_list) == {
        '1001': {
            "name": "Jim",
            "address": "1234",
            "phone_number": "555",
            "email": "something"
        }
    }


def test_show_available_products(setup_db, _show_available_products):
    available_dict = Database.show_available_products()
    assert available_dict == _show_available_products


def test_show_rentals(setup_db, _show_rentals):
    rental_dict = Database.show_rentals('prd1002')
    assert rental_dict == _show_rentals

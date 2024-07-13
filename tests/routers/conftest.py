import pytest

from app import database


@pytest.fixture(scope="module", autouse=True)
def recreate_database():
    database.drop_database()
    database.create_database()

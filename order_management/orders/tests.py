from django.test import TestCase

import pytest 
from django.urls import reverse


@pytest.mark.django_db
def test_database_connection():
    from django.db import connection
    try:
        connection.ensure_connection()
        assert connection.is_usable() is True
    except Exception:
        assert False, "Database connection failed!"


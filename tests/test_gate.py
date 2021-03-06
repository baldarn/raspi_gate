import pytest
from raspi_gate.db import get_db
import pytest
from flask import g, session
from raspi_gate.db import get_db


@pytest.mark.parametrize('path', (
    '/open'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

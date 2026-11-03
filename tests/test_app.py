import pytest
from entities.monster import Monster



class FakeCursor:
    """A fake cursor that simulates database operations for testing purposes"""
    def __init__(self, results=None):
        self.results = results or []
        self.executed_query = None
        self.executed_params = None
        self.closed = False

    def execute(self, query, params=None):
        self.executed_query = query
        self.executed_params = params

    def fetchall(self):
        return self.results

    def close(self):
        self.closed = True


class FakeConnection:
    """A fake connection that simulates database operations for testing purposes"""
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.closed = False
        self.cursor_options = None

    def cursor(self, **kwargs):
        self.cursor_options = kwargs
        return self._cursor

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True



@pytest.fixture
def database_connection(monkeypatch):
    """Fixture that provides a fake database connection and cursor for testing purposes"""
    cursor = FakeCursor(
        [{"id": 1, "name": "Chihuahua", "power": "Ladrido"}]
    )
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "entities.monster.get_connection", lambda: connection
    )
    return connection, cursor


def test_monster_get_all(database_connection):
    """Test the get_all method of the Monster class"""
    connection, cursor = database_connection

    result = Monster.get_all()

    assert len(result) >= 1
    assert result == [{"id": 1, "name": "Chihuahua", "power": "Ladrido"}]
    assert cursor.executed_query == "SELECT id, name, power FROM monster"
    assert connection.cursor_options == {"dictionary": True}
    assert cursor.closed
    assert connection.closed


def test_monster_save(database_connection):
    """Test the save method of the Monster class"""
    connection, cursor = database_connection
    monster = Monster(name="Chihuahua", power="Ladrido")

    monster.save()

    assert cursor.executed_query == (
        #"INSERT INTO monster (name, power) VALUES (%s, %s)"
        "INSERT INTO monsters (name, power) VALUES (%s, %s)"
    )
    assert cursor.executed_params == ("Chihuahua", "Ladrido")
    assert connection.committed
    assert cursor.closed
    assert connection.closed

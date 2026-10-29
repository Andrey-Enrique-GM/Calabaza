from persistence.db import get_connection


class Monster:

    def __init__(self, name, power, id=None):
        self.id = id
        self.name = name
        self.power = power

    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT id, name, power FROM monster')
        monsters = cursor.fetchall()
        cursor.close()
        connection.close()
        return monsters

    def save(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO monster (name, power) VALUES (%s, %s)',
                       (self.name, self.power))
        connection.commit()
        cursor.close()
        connection.close()

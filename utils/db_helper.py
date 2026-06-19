"""4. ХЕНДЛЕР
инструмент для работы с базой
Мы передаем туда конфиг БД, к которой хотим подключиться и все
"""
from pprint import pprint

from hpack import table
from psycopg2.extras import RealDictCursor

from mysql import connector
import psycopg2
import sqlite3
from mysql.connector.cursor import MySQLCursor

from auth.credentials import Credentials
from config.db_config import MyLocalDBConfig

creds = Credentials()


class DataBaseHandler:

    def __init__(self, config):
        self.db_name = config.db_name
        self.config = config
        self.connection = None
        self.cursor: MySQLCursor = None
        self.sslmode = None

    def _get_connection_params(self):
        if self.db_name in ['local_db']:
            return {
                'host': self.config.server,
                'database': self.config.database,
                'user': self.config.user,
                'password': self.config.password,
                'port': self.config.port
            }

        else:
            raise ValueError("Поддерживаются только local_db")

    def connect(self):
        params = self._get_connection_params()
        if self.db_name == 'mysql':
            # self.connection = connector.connect() #<-- здесь надо сделать распаковку параметров
            """connector.connect() принимает args и kwars
            мы в connect получим словарь
            ** распакует следующим образом
            connector.connect(**params), т. е. ключ подставится в качестве аргумента, а значение - в качестве значения
            **params автоматом разобъет на ключ/значение. и вот словарь такого вида
            {
                'host':self.config.server,
                'database':self.config.database,
                'user':self.config.user,
                'password':self.config.password,
                'port':self.config.port
            }
            он раскидает  в таком виде 

            host='',
            user='',
            password='',
            database='',
            port=1234
            """
            self.connection = connector.connect(**params)

        elif self.db_name in ['postgres', 'local_db']:
            self.connection = psycopg2.connect(**params)
        elif self.db_name == 'sqlite':
            self.connection = sqlite3.connect(params["database"])
        """и также в этом методе можно возвращать connect
            в этом методе тогда создается объект курсора - тот, что запишется в self.cursor
        """
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    """ В реальных БД 2 метода ниже использоваться не будут
    Хендлер должен упрощать работу с БД
    например fetchall есть, но все равно в объекте хендлера должны писать запрос
    """

    # def execute(self, query, params=None): # <-- query = SQL запрос, params - это те же параметры, что и в этом примере cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("John", 22))
    #         self.cursor.execute(query, params)
    #
    # def fetchall(self, query):
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()
    """Лучше для конкретного действия писать соответствующий метод, что делает запрос и возвращает данные """
    # def get_all_users(self):
    #     self.cursor.execute("SELECT * FROM users")
    #     return self.cursor.fetchall()

    """Можно улучшить и добавить флаг, например, если надо вернуть только 1 результат"""

    def get_all_users(self, table: str = "persons", fetchone=False):
        self.cursor.execute(f"SELECT * FROM {table} ORDER By id")
        if fetchone:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def add_user(self, table, name, age, hobby=None):
        self.cursor.execute(f"INSERT INTO {table} (name, age, hobby) VALUES ('{name}', {age}, {hobby})")
        self.connection.commit()

    def delete_user(self, id, table: str = "persons"):
        # self.cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        self.cursor.execute(f"DELETE FROM {table} WHERE id = {id}")
        self.connection.commit()

    """Запрос на получение данных с конкретной таблицы, что передастся в метод"""

    def select_all(self, table, **kwargs):
        query = f"SELECT * FROM {table}"
        if kwargs:
            query += " WHERE "
            conditions = []
            for key, value in kwargs.items():
                if isinstance(value, list):
                    variations = [str(item) for item in value]
                    conditions.append(f"{key} IN ('{'\',\''.join(variations)}')")
                else:
                    conditions.append(f"{key} = '{value}'")
            query += " AND ".join(conditions)
            print(query)
        self.cursor.execute(f"{query}")
        return self.cursor.fetchall()

    def _table_name_verification(self, table_name):
        existed_tables = ['users', 'refresh_tokens', 'follows', 'posts', 'hashtags', 'post_hashtags', 'comments',
                          'likes', 'bookmarks', 'conversations', 'conversation_participants', 'messages',
                          'notifications']
        if table_name not in existed_tables:
            raise Exception(f"Table {table_name} does not exist")

    def get_all_local_users(self, table: str = "users"):
        self._table_name_verification(table)
        self.cursor.execute(
            f"SELECT * FROM {table} ORDER By id")
        return self.cursor.fetchall()

    def get_user_by_name(self, user_alias: str = None, table: str = "users"):
        self._table_name_verification(table)
        user_id = creds.get_user(elias=user_alias)
        self.cursor.execute(
            f"SELECT username FROM {table} WHERE id = '{user_id}'")
        return self.cursor.fetchone()["username"]

    def get_conversation_id_between_users(self, user_alias1: str, user_alias2: str,
                                          table: str = "conversation_participants"):
        user_id1 = creds.get_user(user_alias1).user_id
        user_id2 = creds.get_user(user_alias2).user_id

        self._table_name_verification(table)
        self.cursor.execute(
            f"""SELECT conversation_participants.conversation_id FROM conversation_participants INNER JOIN conversations ON conversations.id = conversation_participants.conversation_id WHERE conversation_participants.user_id IN ('{user_id1}', '{user_id2}') AND conversations.is_group IS False GROUP BY 1 HAVING COUNT(*) = 2
            """
        )
        if self.cursor.rowcount > 0:
            return self.cursor.fetchone()["conversation_id"]
        return None

    def check_conversation_by_id(self, id: str, table: str = "conversations"):
        self._table_name_verification(table)
        self.cursor.execute(
            f"""SELECT id FROM {table} WHERE id = '{id}'"""
        )
        return self.cursor.rowcount

    def set_role(self, role: str, user_name: str, table: str = "users"):
        self._table_name_verification(table)
        self.cursor.execute(
            f"""UPDATE {table} SET role = '{role}' WHERE display_name = '{user_name}'"""
        )
        self.connection.commit()

    def mark_all_notifications_unread(self, for_user: str = "Admin"):
        self.cursor.execute(
            f"""UPDATE notifications SET is_read = false
                WHERE user_id IN (
                    SELECT id FROM users WHERE display_name = '{for_user}')"""
        )
        self.connection.commit()

    def delete_conversation(self, id: str, table: str = "conversations"):
        self._table_name_verification(table)
        self.cursor.execute(
            f"""DELETE FROM {table} WHERE id = '{id}'"""
        )
        self.connection.commit()

    def get_comment_with_replies(self, table: str = "comments"):
        self._table_name_verification(table)
        self.cursor.execute(
            """
            SELECT parent_comment_id
            FROM (SELECT parent_comment_id, COUNT(id) as "reply_count" 
                FROM comments 
                WHERE parent_comment_id IS NOT NULL 
                GROUP BY 1 ORDER BY 1) AS "count"
            WHERE "count"."reply_count" > 1
            """
        )
        return self.cursor.fetchone()


    def close_connection(self):
        self.connection.close()

#
# data_base = DataBaseHandler(MyLocalDBConfig)
#
# data_base.connect()
#
# data = data_base.get_conversation_id_between_users("Alice Developer", "Admin")
#
# print(data)
# data_base.close_connection()

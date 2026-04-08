from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import TextClause


class PostgresConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string)
        self.connection = None

    def __enter__(self):
        self.connection = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: dict = None) -> list:
        try:
            result = self.connection.execute(text(query), params or {})
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            return data
        except SQLAlchemyError as e:
            return []

    def execute_modify(self, query, params: dict = None):
        try:
            with self.engine.begin() as connection:
                if isinstance(query, TextClause):
                    connection.execute(query, params or {})
                else:
                    connection.execute(text(query), params or {})
        except SQLAlchemyError as e:
            print(e)

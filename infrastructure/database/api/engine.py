from importlib import reload
from typing import Iterable
from typing_extensions import Any

from . import session
import infrastructure.database.api as reload_session
from sqlalchemy import Select, Update, select, Row, and_, text, String

class BEngine:

    def reload_session(self):
        reload(reload_session)

    def query_statement(self, select_query: Select[Any]) -> Row[Any]:
        with session as s:
            for row in s.execute(select_query):
                yield row

    def insert_objects(
            self,
            objects: Iterable[Any]
    ) -> Iterable[Any]:
        with session as s:
            s.add_all(objects)
            s.commit()
        return objects

    def _update_statement(self, upd: Update[Any]):
        with session as s:
            s.execute(upd).scalar()
            s.commit()

import abc
import logging
from importlib import reload
from typing_extensions import Any
from typing import Sequence, Iterable, Generator, Iterator, List
from sqlalchemy import exc

from infrastructure.database.sql.api import session
import infrastructure.database.sql.api as reload_session
from sqlalchemy import Select, Update, Row

from infrastructure.database.sql.api.pagination import Pagination
from infrastructure.database.sql.models.base import Base
from infrastructure.database.sql.api.exception.generic_exception import RawStatementHttpException

logger = logging.getLogger("root")

class DBEngineAbstract(abc.ABC):


    def reload_session(self):
        raise NotImplemented()

    def query_statement(
            self,
            select_query: Select[Any],
            model: type[Base] = None,
            page: int = None
    ) -> Iterator[Any]:
        raise NotImplemented()

    def insert_objects(
            self,
            objects: Iterable[Any]
    ) -> Iterable[Any]:
        raise NotImplemented()

    def _update_statement(self, upd: Update[Any]):
        raise NotImplemented()


class DBEngine(DBEngineAbstract):

    def reload_session(self):
        reload(reload_session)

    def query_statement(
            self,
            select_query: Select[Any],
            model: Base = None,
            page: int = None
    ) -> Iterator[Any]:
        if page:
            pagination = Pagination(select_query, model)
            select_query = pagination.get_page(page)

        with session as s:
            for row in s.execute(select_query).unique():
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

    def raw_query(
            self,
            select_query: Select[Any],
    ) -> Sequence[Row]:
        try:
            return list(self.query_statement(select_query))
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select raw statement "
                f"custom select statement -> {e}"
            )
            raise RawStatementHttpException(
                detail="Can not create select raw statement",
                status_code=400
            )

    def raw_query_generator(
            self,
            select_query: Select[Any],
    ) -> Iterator[Any]:
        try:
            return self.query_statement(select_query)
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select "
                f"custom select statement -> {e}"
            )
            raise RawStatementHttpException(
                detail="Can not select raw statement",
                status_code=400
            )

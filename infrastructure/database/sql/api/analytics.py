import sqlalchemy as db

from infrastructure.database.sql.api.engine import DBEngine
from infrastructure.database.sql.models.base import Base


class AnalyticsSQLMixin(DBEngine):

    def _count_model_sql(self, model: type[Base]):
        db.select(
            db.func.count()
        ).select_from(model)
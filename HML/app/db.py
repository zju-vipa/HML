from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import sqlalchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute


def auto_alter_tables(flask_app):
    """
    自动修改表结构
    :param flask_app:
    :return:
    """
    with flask_app.app_context():
        metadata = sqlalchemy.MetaData()
        tables = {table_name: {column.name: column for column in
                               sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=db.engine).c}
                  for table_name in db.engine.table_names()}
        models = db.Model.__subclasses__()
        for model_class in models:
            table_name = model_class.__table__.name
            if table_name in tables:
                table = tables[table_name]
                for attr_name in dir(model_class):
                    attr = getattr(model_class, attr_name)
                    if isinstance(attr, InstrumentedAttribute) \
                            and hasattr(attr, 'type') \
                            and hasattr(attr, 'compile'):
                        attr_name = attr.name
                        # 添加新字段
                        if attr_name not in table:
                            column_type = attr.type.compile(dialect=db.engine.dialect)
                            db.engine.execute(
                                'ALTER TABLE %s ADD COLUMN %s %s' % (table_name, attr_name, column_type))


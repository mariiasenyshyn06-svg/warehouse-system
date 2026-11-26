from flask_sqlalchemy import SQLAlchemy


class Database:
    """Шаблон Singleton: єдине підключення до бази даних на весь застосунок.

    Скільки б разів не викликали Database() чи Database.get_instance(),
    повертається той самий об'єкт.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._orm = SQLAlchemy()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    @property
    def orm(self):
        return self._orm

    @property
    def session(self):
        return self._orm.session

    def commit(self):
        self._orm.session.commit()

    def rollback(self):
        self._orm.session.rollback()


# Скорочення, через яке моделі описують таблиці: db.Model, db.Column ...
db = Database.get_instance().orm
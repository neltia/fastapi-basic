from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from common.get_conn import get_mariadb_engine
from app_mariadb.models import Base, Item

engine = get_mariadb_engine()


class MariaDBRepository:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.initialize_database()

    def initialize_database(self):
        """
        Check if the 'items' table exists. If not, create it.
        """
        inspector = inspect(self.engine)
        if 'items' not in inspector.get_table_names():
            print("Table 'items' does not exist. Creating...")
            Base.metadata.create_all(self.engine)
            print("Table 'items' created successfully.")

    def get_all(self):
        session = self.SessionLocal()
        return session.query(Item).all()

    def create(self, item: dict):
        with self.SessionLocal() as session:
            new_item = Item(**item)
            session.add(new_item)
            session.commit()
            session.refresh(new_item)
            return new_item

    def get_by_id(self, item_id: int):
        with self.SessionLocal() as session:
            return session.query(Item).filter(Item.id == item_id).first()

    def update(self, item_id: int, updates: dict):
        with self.SessionLocal() as session:
            item = session.query(Item).filter(Item.id == item_id).first()
            if not item:
                return None
            for key, value in updates.items():
                setattr(item, key, value)
            session.commit()
            session.refresh(item)
            return item

    def delete(self, item_id: int):
        with self.SessionLocal() as session:
            item = session.query(Item).filter(Item.id == item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

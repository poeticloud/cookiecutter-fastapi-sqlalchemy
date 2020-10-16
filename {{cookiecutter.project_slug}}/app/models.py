from datetime import datetime

from sqlalchemy import Column, String, DateTime, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr, declarative_base

Base = declarative_base()


class ModelMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Animal(ModelMixin, Base):
    name = Column(String(50))
    age = Column(Integer)

from sqlalchemy import Integer, String, BigInteger, VARCHAR, ForeignKey, Text
from sqlalchemy.future import select
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db import Base
from db.utils import CreatedModel, db, AbstractClass


class User(CreatedModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class Book(CreatedModel):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    icon: Mapped[str] = mapped_column(VARCHAR(10), nullable=True)
    photo: Mapped[str] = mapped_column(VARCHAR(255))
    units: Mapped[list['Unit']] = relationship("Unit", back_populates="book", )


class Unit(CreatedModel):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit: Mapped[int] = mapped_column(Integer, nullable=False)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    book: Mapped['Book'] = relationship("Book", back_populates="units")
    vocabularies: Mapped[list['Vocabulary']] = relationship("Vocabulary", back_populates="unit")

    @classmethod
    async def get_book_id(cls, id_):
        query = select(cls).where(cls.book_id == id_)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result


class Vocabulary(Base, AbstractClass):
    __tablename__ = "vocabularies"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    eng: Mapped[str] = mapped_column(VARCHAR(255))
    uzb: Mapped[str] = mapped_column(VARCHAR(255))
    unit_id: Mapped[int] = mapped_column(Integer, ForeignKey("units.id", ondelete="CASCADE"))
    unit: Mapped['Unit'] = relationship("Unit", back_populates="vocabularies")

    @classmethod
    async def get_unit_id(cls, id_):
        query = select(cls).where(cls.unit_id == id_)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result


class TestSection(CreatedModel):
    __tablename__ = "test_section"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    tests: Mapped[list['Test']] = relationship('Test', back_populates="test_section")


# class Grammar(CreatedModel):
#     __tablename__ = "grammars"
#     id : Mapped[int] = mapped_column(Integer , primary_key=True ,autoincrement=True)
#     title : Mapped[str] = mapped_column(VARCHAR(255))
#     level : Mapped[str] = mapped_column(VARCHAR(255))
#     tests: Mapped[list['Test']] = relationship('Test',back_populates="test_section")


class Test(Base, AbstractClass):
    __tablename__ = "tests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text)
    a: Mapped[str] = mapped_column(VARCHAR(255))
    b: Mapped[str] = mapped_column(VARCHAR(255))
    c: Mapped[str] = mapped_column(VARCHAR(255))
    d: Mapped[str] = mapped_column(VARCHAR(255))
    right: Mapped[str] = mapped_column(VARCHAR(1))
    test_section_id: Mapped[int] = mapped_column(Integer, ForeignKey("test_section.id", ondelete="CASCADE"))
    test_section: Mapped['TestSection'] = relationship('TestSection', back_populates="tests")

    @classmethod
    async def get_test_section_id(cls, id_):
        query = select(cls).where(cls.test_section_id == id_)
        objects = await db.execute(query)
        result = []
        for i in objects.all():
            result.append(i[0])
        return result


class EverestVocab(Base, AbstractClass):
    __tablename__ = "everest_vocab"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    eng: Mapped[str] = mapped_column(VARCHAR(255))
    uzb: Mapped[str] = mapped_column(VARCHAR(255))



from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Member(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    national_id: Mapped[str]
    phone: Mapped[str]
    residence_address: Mapped[str]
    mailing_address: Mapped[str]
    bank: Mapped[str]
    bank_account: Mapped[str]
    id_card_back: Mapped[str]
    id_card_front: Mapped[str]

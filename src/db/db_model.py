"""
This module defines the database models for the application using SQLAlchemy ORM.

Classes:
    Base: Declarative base class for SQLAlchemy models.
    TaxFix: Represents the TaxFix table in the database, containing user-related tax filing data.
"""

from sqlalchemy import REAL, INTEGER, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.config.config import settings


class Base(DeclarativeBase):
    """
    Declarative base class for all SQLAlchemy models.

    This class serves as a base for defining ORM models using SQLAlchemy's declarative approach.
    """

    pass


class TaxFix(Base):
    """
    SQLAlchemy ORM model for the TaxFix table.

    This model represents user data related to tax filing, including demographic details,
    platform usage behavior, and tax-filing history.

    Attributes:
        age (int): The age of the user (Primary Key).
        income (float): The annual income of the user.
        employment_type (str): The employment type of the user (e.g., full-time, part-time).
        marital_status (str): The marital status of the user.
        time_spent_on_platform (float): The total time the user spent on the platform.
        number_of_sessions (int): The number of sessions the user had on the platform.
        fields_filled_percentage (float): The percentage of fields completed by the user.
        previous_year_filing (int): Whether the user filed taxes in the previous year (1 = Yes, 0 = No).
        device_type (str): The type of device the user used (e.g., mobile, desktop).
        referral_source (str): The source from which the user was referred (e.g., friend, ad).
        completed_filing (int): Whether the user completed the tax filing process (1 = Yes, 0 = No).
    """

    __tablename__ = settings.table_name

    age: Mapped[int] = mapped_column(INTEGER(), primary_key=True)
    income: Mapped[float] = mapped_column(REAL())
    employment_type: Mapped[str] = mapped_column(VARCHAR())
    marital_status: Mapped[str] = mapped_column(VARCHAR())
    time_spent_on_platform: Mapped[float] = mapped_column(REAL())
    number_of_sessions: Mapped[int] = mapped_column(INTEGER())
    fields_filled_percentage: Mapped[float] = mapped_column(REAL())
    previous_year_filing: Mapped[int] = mapped_column(INTEGER())
    device_type: Mapped[str] = mapped_column(VARCHAR())
    referral_source: Mapped[str] = mapped_column(VARCHAR())
    completed_filing: Mapped[int] = mapped_column(INTEGER())

from sqlalchemy import REAL, INTEGER, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings

class Base(DeclarativeBase):
    pass

class TaxFix(Base):
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
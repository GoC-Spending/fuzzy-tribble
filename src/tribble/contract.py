from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255))
    vendor_name = Column(TEXT, nullable=True)
    reference_number = Column(TEXT, nullable=True)
    contract_date = Column(String(255), nullable=True)
    contract_period_start = Column(String(255), nullable=True)
    contract_period_end = Column(String(255), nullable=True)
    delivery_date = Column(String(255), nullable=True)
    contract_value = Column(String(255), nullable=True)
    department = Column(TEXT, nullable=True)
    source_fiscal = Column(String(255), nullable=True)

    def __repr__(self):
        return f'<Contract(id={self.id}, uuid={self.uuid})>'

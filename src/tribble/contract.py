from sqlalchemy import Column, Integer, String, TEXT, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


class Contract(Base):  # type: ignore
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255))
    vendor_name = Column(TEXT, nullable=True)
    reference_number = Column(TEXT, nullable=True)
    contract_date = Column(Date, nullable=True)
    contract_period_start = Column(Date, nullable=True)
    contract_period_end = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)
    contract_value = Column(String(255), nullable=True)
    department = Column(TEXT, nullable=True)
    source_fiscal = Column(Date, nullable=True)
    object_code = Column(TEXT, nullable=True)

    def __repr__(self):
        data_string = ', '.join([f'{key}={getattr(self, key)}'
                                 for key in self.metadata.tables[self.__tablename__].columns.keys()])
        return f'<Contract({data_string})>'

    def __eq__(self, other):
        if not isinstance(other, Contract):
            return False
        return all([getattr(self, key) == getattr(other, key)
                    for key in self.metadata.tables[self.__tablename__].columns.keys()])

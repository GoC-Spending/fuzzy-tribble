from sqlalchemy import Column, Integer, String, TEXT, Date, INTEGER, NUMERIC
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
    contract_date = Column(Date, nullable=False)
    contract_period_start = Column(Date, nullable=False)
    contract_period_end = Column(Date, nullable=False)
    contract_value = Column(NUMERIC(20, 2), nullable=True)
    department = Column(TEXT, nullable=True)
    source_fiscal = Column(Date, nullable=True)
    object_code = Column(TEXT, nullable=True)
    reporting_period_start = Column(Date, nullable=False)
    reporting_period_end = Column(Date, nullable=False)

    def __repr__(self):
        data_string = ', '.join([f'{key}={getattr(self, key)}'
                                 for key in self.metadata.tables[self.__tablename__].columns.keys()])
        return f'<Contract({data_string})>'

    def __eq__(self, other):
        if not isinstance(other, Contract):
            return False
        return all([getattr(self, key) == getattr(other, key)
                    for key in self.metadata.tables[self.__tablename__].columns.keys()])


class RawContract(Base):  # type: ignore
    __tablename__ = 'raw_contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255))
    vendorName = Column(TEXT, nullable=True)
    referenceNumber = Column(TEXT, nullable=True)
    contractDate = Column(TEXT, nullable=True)
    description = Column(TEXT, nullable=True)
    extraDescription = Column(TEXT, nullable=True)
    contractPeriodStart = Column(TEXT, nullable=True)
    contractPeriodEnd = Column(TEXT, nullable=True)
    startYear = Column(INTEGER, nullable=True)
    endYear = Column(INTEGER, nullable=True)
    deliveryDate = Column(TEXT, nullable=True)
    originalValue = Column(NUMERIC(20, 2), nullable=True)
    contractValue = Column(NUMERIC(20, 2), nullable=True)
    comments = Column(TEXT, nullable=True)
    ownerAcronym = Column(TEXT, nullable=True)
    sourceYear = Column(INTEGER, nullable=True)
    sourceQuarter = Column(INTEGER, nullable=True)
    sourceFiscal = Column(TEXT, nullable=True)
    sourceFilename = Column(TEXT, nullable=True)
    sourceURL = Column(TEXT, nullable=True)
    objectCode = Column(TEXT, nullable=True)
    vendorClean = Column(TEXT, nullable=True)

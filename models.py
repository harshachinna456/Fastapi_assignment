from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime, JSON
from database import Base
from sqlalchemy.sql import func

class Trade(Base):
    __tablename__ = "Trade"

    id = Column(Integer, primary_key = True, index = True)
    trade_id = Column(String, unique=True)
    trader = Column(String, nullable = False, index=True)
    trade_details = Column(JSON, default={})
    trade_date_time =  Column(DateTime(timezone=True), server_default=func.now())
    instrument_name = Column(String)
    instrument_id = Column(String)
    counterparty = Column(String, nullable=True)
    asset_class = Column(String, nullable = True)

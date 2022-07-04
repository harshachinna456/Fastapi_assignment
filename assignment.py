from fastapi import FastAPI,Depends
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")


@app.get("/retrieve-trades")
def get_trade_details(db: Session = Depends(get_db)):
    return db.query(models.Trade).all()

@app.post("/post-new-trades")
def new_trade(trade: Trade, db: Session = Depends(get_db)):
    trade_model = models.Trade()
    trade_model.trade_id = trade.trade_id
    trade_model.trader = trade.trader
    trade_model.trade_details = trade.trade_details
    trade_model.trade_date_time = trade.trade_date_time
    trade_model.instrument_name = trade.instrument_name
    trade_model.instrument_id = trade.instrument_id
    trade_model.counterparty = trade.counterparty
    trade_model.asset_class = trade.asset_class

    db.add(trade_model)
    db.commit()

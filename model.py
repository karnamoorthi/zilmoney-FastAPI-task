from sqlalchemy import Integer, String, Float, Column, Boolean, TIMESTAMP, func
from configuration import *

class Expense(base):
    __tablename__ = "Expense"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    category = Column(String)
    create_at = Column(TIMESTAMP)
    is_delete = Column(Boolean, default=False)
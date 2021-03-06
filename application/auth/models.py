from application import db
from application.models import Base

from sqlalchemy.sql import text


class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    transactions = db.relationship("Transaction", backref='account', lazy=True)
    portfolio = db.relationship("Portfolio", backref='account', lazy=True)
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id
  
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    # @staticmethod
    # def find_user_with_largest_BTC_transaction():
    #     stmt = text("SELECT Account.name FROM Account"
    #                 " LEFT JOIN Transaction ON Transaction.account_id = Account.id"
    #                 " GROUP BY Account.id"
    #                 " HAVING COUNT(Portfolio.btc_amount) > 127")
    #     res = db.engine.execute(stmt)
    #     return res
    
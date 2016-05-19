from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

# Relationships
#Users should be able to auction multiple items - One(user) to Many(items)
#Users should be able to bid on multiple items - One(user) to Many(bids)
#Multiple users should be able to place a bid on an item - One(item) to One(bid)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid",backref="items")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items = relationship("Item",uselist=False, backref="users")
    bids = relationship("Bid",backref="users")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'),nullable=False)

Base.metadata.create_all(engine)

#Add three users to the database
tyler = User(username="tyler",password="thinkful")
lila = User(username="lila",password="thinkful")
kyle = User(username="kyle",password="thinkful")

#Make one user auction a baseball
baseball = Item(name="baseball", users=tyler)

#Have each other user place two bids on the baseball
bid1 = Bid(price=10,users=lila,items=baseball)
bid2 = Bid(price=20,users=kyle,items=baseball)
bid3 = Bid(price=30,users=lila,items=baseball)
bid4 = Bid(price=40,users=kyle,items=baseball)

session.add_all([tyler, lila, kyle, baseball, bid1, bid2, bid3, bid4])
session.commit()

#Perform a query to find out which user placed the highest 
highBid = session.query(Bid.price).order_by(Bid.price.desc()).first()
highBidUserID = session.query(Bid.user_id).filter(Bid.price==highBid[0]).first()
highBidUser = session.query(User.username).filter(User.id==highBidUserID[0]).first()

print("And the winner is: ")
print(highBidUser[0])
# select username from users where id = (select user_id from bids where price = (select max(price) from bids))

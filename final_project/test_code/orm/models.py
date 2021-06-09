from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import Null

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<UserDB(" \
               f"id='{self.id}'," \
               f"username='{self.username}', " \
               f"password='{self.password}', " \
               f"email='{self.email}', " \
               f"access='{self.access}', " \
               f"active='{self.active}', " \
               f"start_active_time='{self.start_active_time}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, default=Null)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    access = Column(Integer, nullable=True)
    active = Column(Integer, nullable=True)
    start_active_time = Column(Date, nullable=True)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AllRequests(Base):
    __tablename__ = 'all_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<AllRequests(" \
               f"id='{self.id}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class RequestsByType(Base):
    __tablename__ = 'requests_by_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<RequestsByType(" \
               f"id='{self.id}'," \
               f"type='{self.type}', " \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False)
    count = Column(Integer, nullable=False)


class MostFrequentRequests(Base):
    __tablename__ = 'most_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<MostFrequentRequests(" \
               f"id='{self.id}'," \
               f"url='{self.url}', " \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)


class ClientErrRequests(Base):
    __tablename__ = 'client_err_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<ClientErrRequests(" \
               f"id='{self.id}'," \
               f"url='{self.url}', " \
               f"status_code='{self.status_code}'" \
               f"size='{self.size}'" \
               f"ip='{self.ip}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256), nullable=False)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(String(15), nullable=False)


class ServerErrRequests(Base):
    __tablename__ = 'server_err_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<ServerErrRequests(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'" \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15), nullable=False)
    count = Column(Integer, nullable=False)

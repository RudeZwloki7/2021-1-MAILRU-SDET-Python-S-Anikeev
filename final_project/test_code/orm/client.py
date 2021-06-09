import logging
import sqlalchemy

from sqlalchemy.orm import sessionmaker
from api.client.vk_api_client import VkApiClient
from orm.models import UserDB
from utils.builder import User

logger = logging.getLogger('test')


class MysqlClient:

    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = 'mysql'
        self.port = 3306

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self):
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.connection = self.connection.execution_options(
            isolation_level="READ COMMITTED"
        )
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=True,  # use autocommit on session.add
                                    expire_on_commit=True  # expire model after commit (requests data from database)
                                    )()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def add_user(self, user: User, access=1, active=0, with_vk_id=True):
        user_db = UserDB(username=user.username, password=user.password, email=user.email, access=access, active=active)
        self.session.add(user_db)
        logger.debug(f'Add {user_db} in database')
        if with_vk_id:
            client = VkApiClient()
            client.create_vk_id(user.username, user.vk_id)
        return user_db

    def find_user(self, username=None, email=None):
        if username:
            user = self.session.query(UserDB).filter(UserDB.username == username).first()
            logger.debug(f'Find {user} in database')
        elif email:
            user = self.session.query(UserDB).filter(UserDB.email == email).first()
            logger.debug(f'Find {user} in database')
        else:
            user = None
            logger.debug(f'{user} not found in database')

        return user

    def delete_user(self, username=None, email=None):
        if username:
            self.session.query(UserDB).filter(UserDB.username == username).delete()
        elif email:
            self.session.query(UserDB).filter(UserDB.email == email).delete()

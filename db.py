# Step 1: Import the necessary modules

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


database_url = 'sqlite:///ghUsers.db'

engine = create_engine(database_url)

Base = declarative_base()

class ghUser(Base):
    __tablename__ = "ghusers"
     
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    profile_pic = Column(String(100), unique=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    html_url = Column(String(100), unique=True, nullable=False)
    public_repo_count = Column(Integer)
    top_languages = Column(Integer)
    activity_count = Column(Integer)
    r_without_issues = Column(Integer)
    no_readme = Column(Integer)
    total_team_project = Column(Integer)

    def __repr__(self):
        return (
            '<ghUser {}>'.format(
                self.username, self.profile_pic,
                self.login, self.html_url, self.public_repo_count,
                self.top_languages, self.activity_count,
                self.r_without_issues, self.no_readme,
                self.total_team_project
                )
        )

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
#session = Session()

# Example: Inserting a new user into the database
#new_user = User(username='Sandy', email='sandy@gmail.com')
#session.add(new_user)
#session.commit()

# Step 6: Query data from the database
# Example: Querying all users from the database
"""
all_users = session.query(User).all()

# Example: Querying a specific user by their username
user = session.query(User).filter_by(username='Sandy').first()

# Step 7: Close the session
session.close()
"""
# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import CarInfoNotFoundError
from models import UserInfo, UserListening
from sqlalchemy import func


# Function to get list of car info
def get_all_users(session: Session, limit: int, offset: int) -> List[UserInfo]:
    return session.query(UserInfo).offset(offset).limit(limit).all()

# Function to  get info of particular user
def get_user_info_by_username(session: Session, _username: str) -> UserInfo:
    user_info = session.query(UserInfo).get(_username)
    count_plays = session.query(UserListening).filter_by(user=_username).count()
    favorite_artist = session.query(UserListening.artist, func.count(UserListening.artist)).filter_by(user=_username).group_by(UserListening.artist).order_by(func.count(UserListening.artist).desc()).first()
    favorite_track = session.query(UserListening.track, func.count(UserListening.track)).filter_by(user=_username).group_by(UserListening.track).order_by(func.count(UserListening.track).desc()).first()
    user_info2 = user_info.__dict__

    user_dict = {'user_info': user_info2, 'total_plays' : count_plays, 'favorite_artist' : str(favorite_artist[0]), 'favorite_track' : str(favorite_track[0])}

    if user_dict is None:
        raise CarInfoNotFoundError

    return user_dict

# Function to get total user plays
def count_plays_by_username(session: Session, _username: str) -> UserListening:
    count_plays = session.query(UserListening).filter_by(user=_username).count()

    if count_plays is None:
        raise CarInfoNotFoundError

    count_dict = {'username': _username, 'plays': count_plays}
    return count_dict

# Function to get recently active users
def recent_active_users(session: Session, limit: int, offset: int) -> List[UserListening]:
    return session.query(UserListening).order_by(UserListening.timestamp.desc()).offset(offset).limit(limit).all()
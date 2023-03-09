# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_users, get_user_info_by_username, count_plays_by_username, recent_active_users
from database import get_db
from exceptions import CarInfoException
from schemas import User, CreateAndUpdateCar, PaginatedUserInfo, CountPlays, UserFindClass, RecentlyActive, PaginatedRecentUserInfo

router = APIRouter()
    
# API to get the list of user info
@router.get("/users", response_model=PaginatedUserInfo)
def list_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_db)):

    users_list = get_all_users(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": users_list}

    return response

# API endpoint to get info of a particular user
@router.get("/users/username", response_model=UserFindClass)
def get_user_info(username: str, session: Session = Depends(get_db)):

    try:
        user_info = get_user_info_by_username(session, username)
        return user_info
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

# API endpoint to get info of a particular user
@router.get("/users/totalplays", response_model=CountPlays)
def get_total_plays_for_username(username: str, session: Session = Depends(get_db)):

    try:
        count_plays = count_plays_by_username(session, username)
        return count_plays
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
# API endpoint to get info of a particular user
@router.get("/users/recently-active", response_model=PaginatedRecentUserInfo)
def get_recent_active_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_db)):

    try:
        recent_users = recent_active_users(session, limit, offset)
        response = {'limit':limit, 'offset':offset, 'data': recent_users}
        return response
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
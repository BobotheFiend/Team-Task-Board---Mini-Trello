from fastapi import APIRouter, HTTPException, Depends

from app.schemas.requests.register_user_request import RegisterUserRequest
from app.schemas.requests.login_user_request import LoginUserRequest
from app.schemas.requests.logout_user_request import LogoutUserRequest
from app.schemas.responses.team_member_response import TeamMemberResponse
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service

router = APIRouter()


@router.post("/register", response_model=TeamMemberResponse)
def register_user(request: RegisterUserRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        new_member = auth_service.register(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return TeamMemberResponse.from_team_member(new_member)


@router.post("/login", response_model=TeamMemberResponse)
def login_user(request: LoginUserRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        member = auth_service.login(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return TeamMemberResponse.from_team_member(member)


@router.post("/logout", response_model=TeamMemberResponse)
def logout_user(request: LogoutUserRequest, auth_service: AuthService = Depends(get_auth_service)):
    try:
        member = auth_service.logout(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return TeamMemberResponse.from_team_member(member)`
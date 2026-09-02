from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_team_service
from app.exceptions.team_service_exception import TeamServiceException
from app.schemas.models.team import Team
from app.schemas.requests.create_team_request import CreateTeamRequest
from app.schemas.responses.create_team_response import CreateTeamResponse
from app.services.team_service import TeamService

router = APIRouter()

@router.post("/TeamCreation", response_model=Team)
def create_team(request: CreateTeamRequest, team_service: TeamService = Depends(get_team_service)):
    try:
        team = team_service.create_team(request)
    except TeamServiceException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return team.__str__()

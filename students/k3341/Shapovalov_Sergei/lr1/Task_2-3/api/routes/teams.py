from fastapi import APIRouter, Depends, HTTPException
from connection import get_session
from services.deps import get_current_user
from services.team_service import TeamService
from schemas.teams import TeamCreate, TeamRead, TeamUpdate
from models import Team, User, UserTeamLink
from models import Team
from typing import List

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamRead)
def create_team(data: TeamCreate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TeamRead:
    result = TeamService.create(session, data, user_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])
    return result


@router.get("/", response_model=List[TeamRead])
def get_teams(session=Depends(get_session)) -> List[TeamRead]:
    return session.query(Team).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, session=Depends(get_session)) -> TeamRead:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, data: TeamUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TeamRead:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Only owner can update team")

    if data.name:
        team.name = data.name
    if data.description is not None:
        team.description = data.description

    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.patch("/{team_id}", response_model=TeamRead)
def patch_team(team_id: int, data: TeamUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TeamRead:    
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Only owner can update team")

    if data.name:
        team.name = data.name
    if data.description is not None:
        team.description = data.description
    
    if data.members is not None:
        session.query(UserTeamLink).filter(UserTeamLink.team_id == team_id).delete()
        
        for member_id in data.members:
            user = session.get(User, member_id)
            if user:
                link = UserTeamLink(team_id=team_id, user_id=member_id)
                session.add(link)

    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete("/{team_id}")
def delete_team(team_id: int, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Only owner can delete team")

    session.delete(team)
    session.commit()
    return {"message": "Team deleted successfully"}


@router.post("/{team_id}/join")
def join_team(team_id: int, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    return TeamService.add_member(session, team_id, user_id)

from models import Team, Project, UserTeamLink


class TeamService:

    @staticmethod
    def create(session, data, user_id: int):
        project = session.get(Project, data.project_id)

        if not project:
            return {"error": "project not found"}

        if project.owner_id != user_id:
            return {"error": "only owner can create team"}

        team = Team(
            name=data.name,
            description=data.description,
            project_id=data.project_id,
            owner_id=user_id
        )

        session.add(team)
        session.commit()
        session.refresh(team)
        return team

    @staticmethod
    def get_all(session):
        return session.query(Team).all()

    @staticmethod
    def get_by_id(session, team_id: int):
        return session.get(Team, team_id)

    @staticmethod
    def add_member(session, team_id: int, user_id: int):
        link = UserTeamLink(
            team_id=team_id,
            user_id=user_id
        )

        session.add(link)
        session.commit()

        return {"message": "joined team"}

from models import Project, UserProjectLink


class ProjectService:

    @staticmethod
    def create(session, data, user_id: int):
        project = Project(
            title=data.title,
            description=data.description,
            owner_id=user_id,
            status="active"
        )

        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    @staticmethod
    def get_all(session):
        return session.query(Project).all()

    @staticmethod
    def get_by_id(session, project_id: int):
        return session.get(Project, project_id)

    @staticmethod
    def update(session, project_id: int, data, user_id: int):
        project = session.get(Project, project_id)

        if not project:
            return {"error": "project not found"}

        if project.owner_id != user_id:
            return {"error": "only owner can update project"}

        if data.title:
            project.title = data.title
        if data.description is not None:
            project.description = data.description
        if data.status:
            project.status = data.status

        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    @staticmethod
    def delete(session, project_id: int, user_id: int):
        project = session.get(Project, project_id)

        if not project:
            return {"error": "project not found"}

        if project.owner_id != user_id:
            return {"error": "only owner can delete project"}

        session.delete(project)
        session.commit()

        return {"message": "project deleted"}

    @staticmethod
    def add_member(session, project_id: int, user_id: int):
        link = UserProjectLink(
            project_id=project_id,
            user_id=user_id
        )

        session.add(link)
        session.commit()

        return {"message": "joined project"}

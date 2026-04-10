from models import Task, Project


class TaskService:

    @staticmethod
    def create(session, data, user_id: int):
        project = session.get(Project, data.project_id)

        if not project:
            return {"error": "project not found"}

        if project.owner_id != user_id:
            return {"error": "only owner can create tasks"}

        task = Task(
            title=data.title,
            description=data.description,
            project_id=data.project_id,
            status="active"
        )

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_all(session):
        return session.query(Task).all()

    @staticmethod
    def get_by_id(session, task_id: int):
        return session.get(Task, task_id)

    @staticmethod
    def update_status(session, task_id: int, status: str, user_id: int):
        task = session.get(Task, task_id)

        if not task:
            return {"error": "task not found"}

        task.status = status

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete(session, task_id: int, user_id: int):
        task = session.get(Task, task_id)

        if not task:
            return {"error": "task not found"}

        session.delete(task)
        session.commit()

        return {"message": "task deleted"}

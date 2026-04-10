from models import Skill, UserSkillLink


class SkillService:

    @staticmethod
    def create(session, data):
        skill = Skill(
            name=data.name,
            description=data.description
        )

        session.add(skill)
        session.commit()
        session.refresh(skill)
        return skill


    @staticmethod
    def add_to_user(session, user_id: int, skill_id: int):
        link = UserSkillLink(
            user_id=user_id,
            skill_id=skill_id
        )

        session.add(link)
        session.commit()

        return {"message": "skill added"}
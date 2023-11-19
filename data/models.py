from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from data.database import engine

Base = automap_base()

Base.prepare(engine)

Professional = Base.classes.professional
Company = Base.classes.company
JobAd = Base.classes.jobad

CompanyAd = Base.classes.companyad
Skill = Base.classes.skill


Base_declarative = declarative_base()


class CompanyAdSkill(Base_declarative):
    __tablename__ = "companyadskill"
    CompanyAdID = Column(Integer, primary_key=True)
    SkillID = Column(Integer, primary_key=True)
    Level = Column(String)

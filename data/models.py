from sqlalchemy.ext.automap import automap_base
from data.database import engine

Base = automap_base()

Base.prepare(engine)

Professional = Base.classes.professional

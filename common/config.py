from dotenv import load_dotenv
import os

load_dotenv()


#in .env there should be the JWT_SECRET_KEY=*****
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


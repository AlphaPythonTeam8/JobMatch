from pydantic import BaseModel, constr
from common.oauth2 import generate_verification_token
TUsername = constr(max_length=30, min_length=2)


class Company(BaseModel):
    id: int
    username: TUsername
    company_name: str
    password: str

    @classmethod
    def from_query_result(cls, id, username, company_name, password):
        return cls(
            id=id,
            username=username,
            company_name=company_name,
            password=password)
    
class Professional(BaseModel):
    id: int
    username: TUsername
    first_name: str
    last_name: str
    professional_email: str
    password: str

    @classmethod
    def from_query_result(cls, id, username, first_name, last_name, professional_email, password):
        return cls(
            id=id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            professional_email=professional_email,
            password=password)

def check_username_exist(nickname:str) -> bool:

    data = read_query(
        'SELECT Username FROM company WHERE Username = ?',
        (nickname,)
    )

    return bool(data)

def check_username_exist_professional(nickname:str) -> bool:

    data = read_query(
        'SELECT Username FROM professional WHERE Username = ?',
        (nickname,)
    )

    return bool(data)

def create_company(username: str, company_name: str, email: str, password: str) -> Company | None:
        verification_token = generate_verification_token()
        generated_id = insert_query(
            'INSERT INTO company(Username, CompanyName, Password, Description, Location, PictureURL, Contact, Email, VerificationToken, EmailVerified) VALUES (?,?,?,?,?,?,?,?,?,?)',
            (username, company_name, password, None, None, None, None, email, verification_token, False))

        return Company(id=generated_id, username=username, company_name=company_name, email=email, password="")


def create_professional(username: str, first_name: str, last_name: str, professional_email: str, password: str) -> Professional | None:
        verification_token = generate_verification_token()
        generated_id = insert_query(
            'INSERT INTO professional(Username, FirstName, LastName, Password, BriefSummary, Location, Status, PhotoURL, CVURL, Contact, Email, ProfessionalEmail, VerificationToken, EmailVerified, MainAd) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (username, first_name, last_name, password, None, None, 'Active', None, None, None, None, professional_email, verification_token, False, None))

        return Professional(id=generated_id, username=username, first_name=first_name, last_name=last_name, professional_email=professional_email, password=password)


from mariadb import connect
from mariadb.connections import Connection


def _get_connection() -> Connection:
    return connect(
        user='alphateam8@jobmatchserver',
        password= 'C8buB7CHulGiVhPCup9W',
        host='jobmatchserver.mariadb.database.azure.com',
        port=3306,
        database='jobmatch'
    )

def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)
    
def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid

def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0
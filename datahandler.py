from pydantic import BaseModel
from pydantic import ValidationError


class Data(BaseModel):
    platform : str
    program_name: str
    company_name: str
    program_url: str
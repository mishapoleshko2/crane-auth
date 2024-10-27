from pydantic import BaseModel, EmailStr, SecretStr

class User(BaseModel):
	id: int
	email: EmailStr | None
	pasword: SecretStr
	company_id: int

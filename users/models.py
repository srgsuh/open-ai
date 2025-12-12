from pydantic import BaseModel

ADMIN_ROLE: str = "ADMIN"
USER_ROLE: str = "USER"

class User(BaseModel):
    username: str
    role: str

    def is_admin(self) -> bool:
        return self.role == ADMIN_ROLE
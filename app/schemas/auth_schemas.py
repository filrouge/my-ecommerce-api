from pydantic import BaseModel, Field, ConfigDict, EmailStr


class RegisterSchema(BaseModel):
    email: EmailStr
    nom: str = Field(..., min_length=1)
    password: str = Field(..., min_length=5)
    role: str = Field(default="client")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "admin@admin.com",
                "nom": "administrateur",
                "password": "admin123456",
                "role": "admin",
            }
        }
    )

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=5)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "admin@admin.com",
                "password": "admin123456",
            }
        }
    )

class UserRespSchema(BaseModel):
    id: int
    email: str
    nom: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "admin@admin.com",
                "nom": "administrateur",
                "role": "admin",
            }
        }
    )

class RegisterRespSchema(BaseModel):
    message: str
    user: UserRespSchema

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Client inscrit",
                "user": UserRespSchema.model_json_schema()["example"]
            }
        }
    )


class TokenRespSchema(BaseModel):
    token: str
    message: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                'message': 'Connexion réussie',
                'token': 'eyJhbGciOiJIUzI1NiIs...'
            }
        }
    )

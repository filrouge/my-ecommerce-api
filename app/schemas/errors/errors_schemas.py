from pydantic import BaseModel, ConfigDict
from app.core.exceptions.errors_maps import APP_ERROR_MAP, ORM_ERROR_MAP


class ErrorRespSchema(BaseModel):
    """Schema de base pour toutes les erreurs."""
    error: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"error": "Message d'erreur générique"}
        }
    )


class ErrorClassFactory:
    """Gestion centralisée des classes d'erreurs Swagger/Spectree."""

    def __init__(self):
        self._classes = {}
        self._generate_errors(APP_ERROR_MAP, is_orm=False)
        self._generate_errors(ORM_ERROR_MAP, is_orm=True)

    def _create_class(self, name: str, code: int, example: dict, is_orm: bool):
        """
        Crée une classe d'erreur APP / ORM (ex.: OrderError403 / IntegrityError)
        """
        class_name = name if is_orm else f"{name.capitalize()}Error{code}"
        return type(
            class_name,
            (ErrorRespSchema,),
            {"model_config": ConfigDict(json_schema_extra={"example": example})},
        )

    def _generate_errors(self, error_map: dict, is_orm: bool):
        """
        Génère et stocke les classes d'erreurs selon le type ('app', 'orm') 
        """
        for key, codes in error_map.items():
            for code, example in codes.items():
                self._classes[(key, code)] = self._create_class(key, code, example, is_orm)

    def __call__(self, key: str, code: int):
        """Retourne la classe d'erreur Swagger/Spectree correspondante."""
        return self._classes.get((key, code))


ErrorClass = ErrorClassFactory()

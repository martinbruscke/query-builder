from typing import Any, ClassVar, Dict
from pydantic import BaseModel, RootModel, field_validator



class Condition(BaseModel):
    entity: str
    attribute: str
    operator: str
    values: list

class LogicalModel(BaseModel):
    allowed_keys : ClassVar[set] = {"and_", "or_", "not_"}

    @classmethod
    def validate_structure(cls, values: Dict[str, Any]):
        if not isinstance(values, dict):
            raise ValueError("Debe ser un diccionario con una clave lógica (and_, or_, not_).")

        # Extraemos la clave principal (debe haber solo una)
        keys = set(values.keys())
        if len(keys) != 1:
            raise ValueError("Debe haber exactamente una clave lógica (and_, or_, not_).")

        key = keys.pop()
        if key not in cls.allowed_keys:
            raise ValueError(f"Clave '{key}' no permitida. Debe ser una de {cls.allowed_keys}")

        clause_data = values[key]
        if not isinstance(clause_data, dict):
            raise ValueError(f"El operador '{key}' debe contener un diccionario.")

        # Validar not_ → Debe tener un solo "operand" como objeto
        if key == "not_":
            if "operand" not in clause_data:
                raise ValueError(f"El operador 'not_' debe contener un campo 'operand'.")
            if not isinstance(clause_data["operand"], dict):
                raise ValueError(f"'operand' en 'not_' debe ser un objeto.")
        # Validar and_ y or_ → Deben tener "operands" como lista
        elif key in {"and_", "or_"}:
            if "operands" not in clause_data:
                raise ValueError(f"El operador '{key}' debe contener un campo 'operands'.")
            if not isinstance(clause_data["operands"], list):
                raise ValueError(f"'operands' en '{key}' debe ser una lista.")

        return values

    # def __init__(self, **data):
    #     validated_data = self.validate_structure(data)
    #     super().__init__(validated_data)


class Criteria(BaseModel):
    criteria :  LogicalModel
    

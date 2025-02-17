# query_builder.py
from typing import Dict
from sqlalchemy import UUID, and_, or_, not_, between, select
from sqlalchemy.orm import aliased

from models import Assignment, Course, StudentCourse, Submission, TeacherCourse, User
from schema import Condition, Criteria, LogicalModel

class QueryBuilder:
    operator_mapping = {
        "is Greater than": "__gt__",
        "is Less than": "__lt__",
        "is Equal to": "__eq__",
        "is Not Equal to": "__ne__",
        "Contains": "contains",
        "In": "in_",
        "Between": "between"
    }
    
    model_mapping = {
        "User": User,
        "Course": Course,
        "StudentCourse": StudentCourse,
        "TeacherCourse": TeacherCourse,
        "Assignment": Assignment,
        "Submission": Submission
    }

    def __init__(self, model_class):
        self.model_class = model_class
        # self.query = select(
        #     self.model_class.name,
        #     self.model_class.email,
        #     self.model_class.phone)
        self.query = select(self.model_class)   
        self.joins = set()


    def build(self, criteria):
        print(f"\nEn build, antes de parsear criteria {criteria} \n")
        
        where_clause = self._parse_criteria(criteria)
        
        print(f"\nEn build, el where_clause es: {where_clause}\n")
        return self.query.where(where_clause)


    def _parse_criteria(self, criteria: Dict):                  # Primer paso
        print(f"\n _parse_criteria {criteria} \n")
                
               
       # Verificamos si existen las claves dentro del diccionario usando 'in'
        if "and_" in criteria and criteria["and_"]:
            return self._build_logical(criteria["and_"], and_)  # Se pasa 'and' como string, no como operador
        elif "or_" in criteria and criteria["or_"]:
            return self._build_logical(criteria["or_"], or_)
        elif "not_" in criteria and criteria["not_"]:
            return self._build_not(criteria["not_"])
        elif "condition" in criteria and criteria["condition"]:
            return self._build_condition(criteria["condition"])
        else:
            raise ValueError("Invalid criteria structure")

    def _build_condition(self, condition):
        print(f"\n _build_condition {condition} \n")
        
        model = self.model_mapping[condition["entity"]]
        column = getattr(model, condition["attribute"])
        operator = self.operator_mapping[condition["operator"]]
        
        # Ver los valores antes de la conversión a UUID
        print(f"Valores originales: {condition['values']}")
        
        # Verificar el tipo de datos del primer valor
        print(f"Tipo de datos del primer valor: {type(condition['values'][0])}")  # Aquí ves el tipo de dato
    

        # Convertir los valores a UUID si es necesario
        values = condition["values"]
        # if isinstance(values[0], str) and len(values[0]) >= 30:  # Suponiendo que el UUID es una cadena en formato estándar
        #     try:
        #         values = [str(UUID(value)) for value in values]  #  Convertimos a string
        #         # Ver los valores después de la conversión
        #         print(f"Valores convertidos a UUID: {values}")
        #     except ValueError as e:
        #         print(f"Error al convertir a UUID: {e}")
        
        if model not in self.joins and condition["entity"] != self.model_class.__name__:
            model_alias = aliased(model)
            self.query = self.query.join(model_alias, isouter=True)
            self.joins.add(model)
        
        if operator == "between":
            # return column.between(*condition["values"])
            return column.between(*values)
        
        if operator == "in_":
            # return column.in_(condition["values"])
            return column.in_(values)
        
        # return getattr(column, operator)(*condition["values"])
        return getattr(column, operator)(*values)


    def _build_logical(self, clause, operator):
        print(f"\n _build_logical {clause} \n")
        
        list_operands=clause["operands"]
        clauses = [self._parse_criteria(op) for op in list_operands]
        return operator(*clauses)


    def _build_not(self, clause):
        print(f"\n _build_not {clause} \n")
        
        clause_not = clause["operand"]
        return not_(self._parse_criteria(clause_not))
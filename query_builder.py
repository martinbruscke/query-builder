# query_builder.py
from typing import Any, Dict, List
from sqlalchemy import UUID, ScalarSelect, and_, case, func, or_, not_, between, select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import Select
from sqlalchemy.types import TypeEngine

from models.assignmentModel import AssignmentModel
from models.courseModel import Course 
from models.courseTag import CourseTagModel
from models.studentCourseModel import StudentCourseModel
from models.teacherModel import TeacherCourseModel
from models.submissionModel import Submission
from models.userModel import UserModel


class QueryBuilder:
    operator_mapping = {
        "is Greater than": "__gt__",
        "is Greater than or Equal to": "__ge__",
        "is Less than": "__lt__",
        "is Less than or Equal": "__le__",
        "is Equal to": "__eq__",
        "is Not Equal to": "__ne__",
        "Contains": "contains",
        "In": "in_",
        "Between": "between"
    }
    
    model_mapping = {
        "UserModel": UserModel,
        "Course": Course,
        "CourseTagModel": CourseTagModel,
        "StudentCourseModel": StudentCourseModel,
        "TeacherCourseModel": TeacherCourseModel,
        "AssignmentModel": AssignmentModel,
        "Submission": Submission
    }
    
    metrics_mapping = {
        "UserModel": {
            "query": {
                "id": "id",
                "Student Name": "uuid",  # columna uuid de users
                "Student Email": "student_email",  # columna uuid de users
                "Student Last Login": "student_last_login",  # columna last_login_at de users
                "Tags": "registry_id",  # request a data_access registry_id con tag vinculado -> columna registry_id de users #veo q esta listo
            }
        },
        
        "subquery": {
                "Student Activity Percentage": "student_activity_percentage",  # subquery, total de assignments activos sobre total de submissions unicas entregadas -> porcentaje
                "Overall Course Risk Percentage": "overall_course_risk_percentage",  # subquery, traer usuarios en cursos con (promedio de current_risk de student_course activos de cada curso) 
                "Percentage of Assignments Delivered": "percentage_of_assignments_delivered",  # traer todas assigments de un curso, traer submissions que matcheeen con course_uuid y calcular
                "Percentage of Assignments Pending": "percentage_of_assignments_pending",  # """"
                
                "Percentage of Assignments Delivered": "percentage_of_assignments_delivered",  # traer todas assigments de todos los cursos de un usuario y comparar con submissions de ese usuario, traer submissions que matcheeen con course_uuid y calcular
                "Percentage of Assignments Pending": "percentage_of_assignments_pending",  # """"
                "Average Grade": "average_grade",  # avg de submissions de un usuario
                "Final Grade": "final_grade",  # columna final score grade student_course
                "Final Score": "final_score",  # columna final score student_course
                
                "Number of Courses Taught by Professor": "number_of_courses_taught_by_professor",  # traer profesores con count de teachercourse group by course_uuid
                "Number of Sections Taught by Professor": "number_of_sections_taught_by_professor",  # traer profesores con count de cathedra group by cathedra_uuid
                "Number of Students Taught by Professor": "number_of_students_taught_by_professor",  # studentcourse de course_uuid
        },
        "Course": {
            "query": {
                "Course Name": "uuid",  # columna uuid de course
                "Status": "status",  # columna lms_state_uuid de course
            }
        },
        "CourseTagModel": {
            "query": {
                "Tag": "tag_uuid",  # courseTag tag_uuid -> course_uuid  #veo q esta listo
            }
        },
        "cathedra": {
            "query": {
                "Section Name": "uuid",  # columna uuid de cathedras
                
            },
        },
        "StudentCourseModel": {
            "query": {
                "Final Grade": "final_score", # columna final score student_course
                "Student Last Contact": "student_last_contact",  # no
                "Student Status": "student_status",  # no
                "Risk Percentage": "risk_percentage",  # columna current_risk de studentcourse
            },
        },
        "TeacherCourseModel": {
            "query": {
                "Tags": "tags",  # request a data_access registry_id con tag vinculado -> columna registry_id de users
                "Professor Name": "professor_name",  # columna uuid de users
                "Professor Last Login": "professor_last_login",  # columna last_login_at de users
            }
        },
        "assignment": {
            "query": {
                "Assignment Name": "uuid",  # columna uuid de assignments
                "Assignment Due Date": "assignment_due_date",  # columna due_at de assignments 
            } 
        },
        "submission": {
            "query": {
                "Assignments Grade": "score",  # columna score de submissions
            },
        },
    }
    
    def build(self, criteria) -> Select:
        print(f"\nEn build, antes de parsear criteria {criteria} \n")
        where_clause = self._parse_criteria(criteria)
        
        # Aseguramos que seleccionamos User y aplicamos los joins necesarios
        final_query = (
            select(UserModel)
            .distinct()
            .join(StudentCourseModel, UserModel.uuid== StudentCourseModel.user_uuid)
            .join(Course, StudentCourseModel.course_uuid == Course.uuid)
            .join(AssignmentModel, AssignmentModel.course_uuid == Course.uuid)
            .join(Submission, and_(
                Submission.assignment_id == AssignmentModel.id,
                Submission.user_id == UserModel.uuid
            ))
            .where(where_clause)
        )
        
        print(f"\nEn build, la query final es: {final_query}\n")
        return final_query


    def _parse_criteria(self, criteria: Dict):                  # Primer paso
        print(f"\n _parse_criteria {criteria} \n")
                
        if "and_" in criteria and criteria["and_"]:
            return self._build_logical(criteria["and_"], and_)
        elif "or_" in criteria and criteria["or_"]:
            return self._build_logical(criteria["or_"], or_)
        elif "not_" in criteria and criteria["not_"]:
            return self._build_not(criteria["not_"])
        elif "condition" in criteria and criteria["condition"]:
            return self._build_condition(criteria["condition"])
        else:
            raise ValueError("Invalid criteria structure")



    def _build_logical(self, clause, operator):
        print(f"\n _build_logical {clause} \n")
        operands = [self._parse_criteria(op) for op in clause["operands"]]
        return operator(*operands)



    def _build_not(self, clause):
        print(f"\n _build_not {clause} \n")
        clause_not = clause["operand"]
        return not_(self._parse_criteria(clause_not))
    
    
    def _build_condition(self, condition):
        print(f"\n _build_condition {condition} \n")
        model = self.model_mapping.get(condition["entity"])
        if not model:
            raise ValueError(f"Modelo '{condition['entity']}' no encontrado en model_mapping")

        attribute = condition["attribute"]
        operator = self.operator_mapping.get(condition["operator"])
        if not operator:
            raise ValueError(f"Operador '{condition['operator']}' no soportado")
        values = condition["values"]
        
        # Verificar si el atributo es una métrica
        metric_info = self.metrics_mapping.get(condition["entity"], {})
        
        if attribute in metric_info.get("subquery", {}):
            # Es una subquery
            subquery = self._build_subquery(attribute, model, operator, values)
            # Correlacionamos la subquery con la query principal
            return self._correlate_subquery(subquery, operator, values)
        else:
            # Es una columna normal
            column_name = metric_info.get("query", {}).get(attribute, attribute)
            if not hasattr(model, column_name):
                raise ValueError(f"Columna {column_name} no encontrada en {model.__name__}")
            column = getattr(model, column_name)
            
            # Convertir valores según el tipo de columna
            converted_values = self._convert_values_based_on_type(column, values)
            
            # Aplicar el operador
            return self._apply_operator(column, operator, converted_values)

    def _correlate_subquery(self, subquery, operator, values):
        """
        Correlaciona una subquery con la query principal y aplica la condición.
        """
        if operator == "between":
            return subquery.between(values[0], values[1])
        elif operator == "in_":
            return subquery.in_(values)
        else:
            return getattr(subquery.scalar_subquery(), self.operator_mapping[operator])(values[0])

    
        
    
    def _add_required_joins(self, target_model: Any) -> None:
        if target_model == User:
            return
        
        join_path = self._find_join_path(self.model_class, target_model)
        for step in join_path:
            if step not in self.joins:
                self.base_query = self.base_query.join(*step)
                self.joins.add(step)
                
                
    
    def _get_column_or_subquery(self, model: Any, attribute: str, condition: Dict) -> Any:
        metric_info = self.metrics_mapping.get(model.__name__.lower(), {})
        
        if attribute in metric_info.get("subquery", {}):
            return self._build_subquery(model, attribute, condition)
        else:
            column_name = metric_info.get("query", {}).get(attribute, attribute)
            if not hasattr(model, column_name):
                raise ValueError(f"Columna {column_name} no encontrada en {model.__name__}")
            return getattr(model, column_name)



    def _apply_operator(self, column: Any, operator: str, values: List) -> Any:
            if operator == "in_":
                return column.in_(values)
            elif operator == "between":
                return column.between(values[0], values[1])
            elif operator == "contains":
                return column.contains(values[0])
            else:
                if len(values) != 1:
                    raise ValueError(f"Operador {operator} requiere un solo valor")
                return getattr(column, operator)(values[0])



    def _build_subquery(self, metric, model, operator, values):
        """
        Construye subqueries correlacionadas según la métrica solicitada.
        """
        if metric == "student_activity_percentage":
            subquery = (
                select(
                    (func.count(Submission.id) * 100.0 / func.count(Assignment.id))
                    .label("student_activity_percentage")
                )
                .select_from(Course)
                .join(Assignment)
                .outerjoin(Submission, and_(
                    Submission.assignment_id == Assignment.id,
                    Submission.user_id == User.id
                ))
                .where(Course.id == StudentCourse.course_id)
                .correlate(User)
                .scalar_subquery()
            )

        elif metric == "overall_course_risk_percentage":
            subquery = (
                select(
                    (func.count(case((Submission.score < 50, 1), else_=0)) * 100.0 / func.count(Submission.id))
                    .label("overall_course_risk_percentage")
                )
                .select_from(Course)
                .join(Assignment)
                .join(Submission)
                .where(Course.id == StudentCourse.course_id)
                .correlate(User)
                .scalar_subquery()
            )

        elif metric == "percentage_of_assignments_delivered":
            subquery = (
                select(
                    (func.count(Submission.id) * 100.0 / func.count(Assignment.id))
                    .label("percentage_of_assignments_delivered")
                )
                .select_from(Course)
                .join(Assignment)
                .outerjoin(Submission, and_(
                    Submission.assignment_id == Assignment.id,
                    Submission.user_id == User.id
                ))
                .where(Course.id == StudentCourse.course_id)
                .correlate(User)
                .scalar_subquery()
            )

        elif metric == "percentage_of_assignments_pending":
            subquery = (
                select(
                    ((func.count(Assignment.id) - func.count(Submission.id)) * 100.0 / func.count(Assignment.id))
                    .label("percentage_of_assignments_pending")
                )
                .select_from(Course)
                .join(Assignment)
                .outerjoin(Submission, and_(
                    Submission.assignment_id == Assignment.id,
                    Submission.user_id == User.id
                ))
                .where(Course.id == StudentCourse.course_id)
                .correlate(User)
                .scalar_subquery()
            )

        elif metric == "assignments_grade":
            subquery = (
                select(func.avg(Submission.score).label("assignments_grade"))
                .select_from(Course)
                .join(Assignment)
                .join(Submission)
                .where(and_(
                    Course.id == StudentCourse.course_id,
                    Submission.user_id == User.id,
                    Submission.score.isnot(None)
                ))
                .correlate(User)
                .scalar_subquery()
            )

        else:
            raise ValueError(f"Métrica {metric} no implementada en subqueries")

        return subquery

        
        
    def _find_join_path(self, source: Any, target: Any) -> List[tuple]:
        # Implementar lógica para encontrar la ruta de unión entre modelos
        # Ejemplo simplificado:
        if (source == User and target == StudentCourse):
            return [(StudentCourse, User.student_courses)]
        
        elif (source == User  and target == TeacherCourse):
            return [(TeacherCourse, User.teacher_course)]
        elif (source == StudentCourse and target == Course):
            return [(Course, StudentCourse.course)]
        # Añadir más rutas según sea necesario
        else:
            raise ValueError(f"No se encontró ruta de unión de {source} a {target}")
        
    
    def _convert_values_based_on_type(self, column: Any, values: List) -> List:
        column_type = column.type
        converted = []
        for v in values:
            if isinstance(column_type, UUID):
                converted.append(UUID(v))
            elif isinstance(column_type, TypeEngine):
                converted.append(column_type.python_type(v))
            else:
                converted.append(v)
        return converted
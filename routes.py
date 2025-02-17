from typing import Dict
from fastapi import APIRouter, HTTPException, Depends

from database import get_db
from models import User
# from query_builder import QueryBuilder
from query_builder import QueryBuilder
from schema import Criteria
from sqlalchemy.orm import Session



query_builder_routes = APIRouter()

@query_builder_routes.post("/query")
def execute_query(criteria: Dict, db: Session = Depends(get_db)):
    try:
        print(criteria)
    
        qb = QueryBuilder(User)  # Partimos del User por default
        
        criteria = criteria["criteria"]  # Extraemos el contenido real
        
        query = qb.build(criteria) # Realizamos la construccion de la query
        
        print(f"Antes de buscar en BBDD,  query es : {query}")
        result = db.scalars(query).all() # ejecutamos la query
        print(f"Desp de buscar en BBDD,  result es : {result}")
        
        clean_results = []
        for row in result:
            row_dict = row.__dict__
            row_dict.pop("_sa_instance_state", None)  # Eliminamos metadata interna de SQLAlchemy
            clean_results.append(row_dict)
            print(f"Iteracion clean_result es : {clean_results}")

        return {"results": clean_results}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

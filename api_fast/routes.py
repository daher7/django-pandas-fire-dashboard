from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from api_fast.database import get_db

router = APIRouter()

@router.get("/query")
def run_query(
    q: str = Query(
        ..., 
        description="Consulta SQL a ejecutar (Solo SELECT)",
        openapi_examples={
            "ejemplo_basico": {
                "summary": "Consulta de prueba",
                "description": "Retorna los primeros 5 registros de la tabla incendios.",
                "value": "SELECT * FROM incendios LIMIT 5"
            }
        }
    )
):
    """
    Ejecuta una consulta SQL SELECT sobre la base de datos de incendios.
    Aplica restricciones de seguridad y límites de rendimiento automáticos.
    """
    
    # 1. Limpieza y validación básica
    query_clean = q.strip()
    query_lower = query_clean.lower()

    # 2. Filtros de seguridad (Evitar inyecciones maliciosas)
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "truncate", "exec", "attach", "benchmark", "sleep"]
    
    if any(word in query_lower for word in forbidden):
        raise HTTPException(
            status_code=403, 
            detail="Operación no permitida. Solo se admiten consultas de lectura (SELECT)."
        )

    if not query_lower.startswith("select"):
        raise HTTPException(
            status_code=400, 
            detail="La consulta debe comenzar con la palabra clave SELECT."
        )

    # 3. Control de rendimiento (Forzar LIMIT 100 si no existe)
    query_to_execute = query_clean.rstrip(';')
    
    if "limit" not in query_lower:
        query_to_execute += " LIMIT 5000"

    # 4. Ejecución en Base de Datos
    conn = None
    try:
        conn = get_db()
        # Nota: Se asume que get_db() configura row_factory = sqlite3.Row 
        cursor = conn.execute(query_to_execute)
        rows = cursor.fetchall()
        
        # Convertimos cada fila a un diccionario para la respuesta JSON
        return [dict(row) for row in rows]

    except Exception as e:
        # Captura errores de sintaxis SQL o tablas inexistentes
        raise HTTPException(
            status_code=400, 
            detail=f"Error en la ejecución de SQL: {str(e)}"
        )
    
    finally:
        # Garantizamos el cierre de la conexión pase lo que pase
        if conn:
            conn.close()
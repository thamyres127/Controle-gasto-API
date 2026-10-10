import os
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


DATABASE_URL = os.environ["DATABASE_URL"].strip().strip("'\"")
_host = DATABASE_URL.split("@")[-1].split("/")[0] if "@" in DATABASE_URL else "SEM ARROBA"
print(f"DIAGNOSTICO: tamanho={len(DATABASE_URL)} comeco={DATABASE_URL[:13]} host={_host}", flush=True)

def executar(sql, params=(), buscar=False):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            if buscar:
                return cur.fetchall()
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    executar(
        """CREATE TABLE IF NOT EXISTS gastos (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            valor NUMERIC(10, 2) NOT NULL,
            categoria TEXT NOT NULL,
            data DATE NOT NULL DEFAULT CURRENT_DATE
        )"""
    )
    yield


app = FastAPI(title="Controle de Gastos API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://thamyres127.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GastoNovo(BaseModel):
    descricao: str
    valor: float = Field(gt=0)
    categoria: str
    data: Optional[date] = None


@app.get("/gastos")
def listar_gastos():
    linhas = executar(
        "SELECT id, descricao, valor, categoria, data FROM gastos "
        "ORDER BY data DESC, id DESC",
        buscar=True,
    )
    return [
        {"id": i, "descricao": d, "valor": float(v), "categoria": c, "data": dt.isoformat()}
        for i, d, v, c, dt in linhas
    ]


@app.post("/gastos", status_code=201)
def adicionar_gasto(gasto: GastoNovo):
    if gasto.categoria not in CATEGORIAS:
        raise HTTPException(status_code=400, detail="Categoria inválida")
    data_gasto = gasto.data or date.today()
    linhas = executar(
        "INSERT INTO gastos (descricao, valor, categoria, data) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (gasto.descricao, gasto.valor, gasto.categoria, data_gasto),
        buscar=True,
    )
    return {"id": linhas[0][0]}


@app.delete("/gastos/{gasto_id}")
def apagar_gasto(gasto_id: int):
    linhas = executar(
        "DELETE FROM gastos WHERE id = %s RETURNING id", (gasto_id,), buscar=True
    )
    if not linhas:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")
    return {"apagado": gasto_id}


@app.get("/gastos/resumo")
def resumo_por_categoria(dias: int = 30):
    inicio = date.today() - timedelta(days=dias)
    linhas = executar(
        "SELECT categoria, SUM(valor) FROM gastos WHERE data >= %s "
        "GROUP BY categoria ORDER BY SUM(valor) DESC",
        (inicio,),
        buscar=True,
    )
    return [{"categoria": c, "total": float(t)} for c, t in linhas]

from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "E-commerce AI Agent API is running!"}

@app.get("/test-db")
def test_db():
    conn = sqlite3.connect("ecommerce.db")
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    return {"tables": [table[0] for table in result]}


@app.get("/total-sales")
def get_total_sales():
    conn = sqlite3.connect("ecommerce.db")
    result = conn.execute("SELECT SUM(total_sales) FROM total_sales").fetchone()
    conn.close()
    total_sales = result[0] if result and result[0] else 0
    return {"total_sales": total_sales}

@app.get("/roas")
def get_roas():
    conn = sqlite3.connect("ecommerce.db")
    result = conn.execute("SELECT SUM(ad_sales), SUM(ad_spend) FROM ad_sales").fetchone()
    conn.close()
    ad_sales, ad_spend = result if result else (0, 0)
    roas = (ad_sales / ad_spend) if ad_spend else None
    return {"ad_sales": ad_sales, "ad_spend": ad_spend, "roas": roas}

@app.get("/highest-cpc")
def highest_cpc():
    conn = sqlite3.connect("ecommerce.db")
    result = conn.execute("""
        SELECT item_id, ad_spend * 1.0 / NULLIF(clicks, 0) as cpc
        FROM ad_sales
        WHERE clicks > 0
        ORDER BY cpc DESC
        LIMIT 1;
    """).fetchone()
    conn.close()
    if result:
        return {"item_id": result[0], "max_cpc": result[1]}
    else:
        return {"message": "No product with clicks"}
from fastapi import Request

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body.get("question", "").lower()
    if "total sales" in question:
        sql = "SELECT SUM(total_sales) FROM total_sales"
    elif "roas" in question or "return on ad spend" in question:
        sql = "SELECT SUM(ad_sales) / SUM(ad_spend) FROM ad_sales"
    elif "highest cpc" in question or "cost per click" in question:
        sql = """
        SELECT item_id, ad_spend * 1.0 / NULLIF(clicks, 0) as cpc
        FROM ad_sales
        WHERE clicks > 0
        ORDER BY cpc DESC
        LIMIT 1;
        """
    else:
        return {"answer": "Sorry, I don't understand the question."}
    conn = sqlite3.connect("ecommerce.db")
    result = conn.execute(sql).fetchone()
    conn.close()
    return {"answer": result}
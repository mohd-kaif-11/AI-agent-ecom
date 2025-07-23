from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine
import pandas as pd
from llm_wrapper import SQLTranslator

app = FastAPI()
engine = create_engine("sqlite:///db/ecom.db")
sql_translator = SQLTranslator(model_path="models/your-llm-model.bin")

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data["question"]

    # Example: Generate schema summary for prompt
    schema = "ad_sales_metrics(product_id, campaign_id, ad_spend, clicks, ... ), ..."
    sql_query = sql_translator.nl_to_sql(question, schema)
    result = pd.read_sql(sql_query, con=engine).to_dict(orient="records")

    # Optional: Visualization
    if "chart" in question.lower() or "plot" in question.lower():
        # code to create image and return as attachment
        pass

    def stream_response():
        intro = f"Answer to: {question}\n"
        for c in intro:
            yield c
        yield str(result)
    return StreamingResponse(stream_response(), media_type="text/plain")

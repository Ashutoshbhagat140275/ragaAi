from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf
import time
from yahooquery import Ticker
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import json
import uuid
from langdetect import detect
from deep_translator import GoogleTranslator
from fastapi.responses import JSONResponse
from fastapi import status
import shutil
import os
from nsetools import Nse


app=FastAPI()
GEMINI_API_KEY="AIzaSyBikd912A40qz1gxBMazdwrKaKSzK6GzJk"
CHROMA_PATH = "chroma"
class Item(BaseModel):
    name:str
    price:float
    is_offer:bool=None

my_global_index = "initial value"
# nse = Nse()
# all_stock_codes = nse.get_stock_codes()
# tickers = [code + ".NS" for code in all_stock_codes if code != 'SYMBOL']

# Add indices to tickers
indices = ["^GSPC", "^IXIC", "^DJI", "^NSEI", "^BSESN"]

context_template = """You are a financial AI assistant. You have access to the following up-to-date stock and market statistics:

{context}

A user has asked the following question about the market or specific stocks:

Question: {question}

Using only the information provided in the context above, generate a clear, concise, and accurate answer to the user's question. If the context does not contain enough information, say "I don't have enough data to answer that specifically, but here's what I can tell you:" and provide a general insight.

Your response should be professional, factual, and easy to understand for someone interested in financial markets."""
# if os.path.exists(CHROMA_PATH):
#          shutil.rmtree(CHROMA_PATH)  
@app.post("/items/")
def create_item(item:Item):
    return{"item":item}

@app.get("/get_data")
def get_data():
    indices= ["^GSPC", "^IXIC", "^DJI", "^NSEI", "^BSESN"]
    data = yf.download(indices, start="2020-01-01", end="2024-05-27", interval="1d")
    data.columns=['_'.join(col).strip() for col in data.columns.values]
    return data.tail(5).fillna(0).to_dict(orient="index")

@app.get("/Scraping_data")
def Scraping_data():
    indices = ["^GSPC", "^IXIC", "^DJI", "^NSEI", "^BSESN"]
    t = Ticker(indices)
    print(indices)
    history = t.history(period="5d", interval="1d")
    # Reset index to flatten MultiIndex (symbol, date) to columns
    history = history.reset_index()
    # Optionally flatten columns if needed
    history.columns = [
        '_'.join(col).strip() if isinstance(col, tuple) else str(col)
        for col in history.columns.values
    ]
    # Convert to list of dicts for JSON compatibility
    history['date'] = history['date'].astype(str)
    data= history.fillna(0).to_dict(orient="records")
    bool=store_the_data(data)
    print("yess")
    if bool:
       return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Data scraped and stored successfully."}
        )
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Failed to store data."}
    )

def store_the_data(data):
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            
            is_separator_regex=False
        )
    docs=[Document(page_content=json.dumps(row)) for row in data]
    chunks=splitter.split_documents(docs)
    for index, chunk in enumerate(chunks):
        chunk.metadata["index"]=index

    # Store the chunks in the Chroma database

    for chunk in chunks:
        print("chunk=>",chunk)
    settings = chromadb.Settings(
        persist_directory=CHROMA_PATH,
        is_persistent=True
    )
    client = chromadb.Client(settings)
    
    db = Chroma(
        client=client,
        collection_name=f"user_{index}",
        embedding_function=get_embedding_function()
    )
    global my_global_index
    my_global_index=f"user_{index}"
    print(my_global_index)
    batch_id = str(uuid.uuid4())
    chunk_ids = [f"{batch_id}_{chunk.metadata['index']}" for chunk in chunks]
    db.add_documents(chunks, ids=chunk_ids)
    docs=db.get(limit=5)
    return True

    

class GeminiEmbeddingFunction:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = "models/embedding-001"

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = genai.embed_content(model=self.model, content=text, task_type="retrieval_document")
            embeddings.append(response["embedding"])
        return embeddings

    def embed_query(self, text):
        response = genai.embed_content(model=self.model, content=text, task_type="retrieval_query")
        return response["embedding"]

    def __call__(self, texts):
        return self.embed_documents(texts)


def get_embedding_function():
    return GeminiEmbeddingFunction(GEMINI_API_KEY)


@app.get("/")
def read_root():
    return {"message":"Hello, from FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id:int,q:str=None,name:str=None):
    return {"item_id":item_id,"q":q,"name":name}

@app.get("/ask_question")
def ask_question(question:str):
    question1=question
    detected_lang=detect(question1)
    query_text=question1
    if detected_lang!="en":
        query_text = GoogleTranslator(source=detected_lang, target='en').translate(question1)

    settings=chromadb.Settings(
        persist_directory=CHROMA_PATH,
        is_persistent=True
    )
    client=chromadb.Client(settings)
    collections=client.list_collections()
    if not collections:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status":"error","message":"Collection not present"}
        )
    db = Chroma(
        client=client,
        collection_name=f"user_24",
        embedding_function=get_embedding_function()
    )
    results = db.similarity_search_with_score(query=query_text, k=3)
    prompt = context_template.format(context=results, question=question1)
    llm = get_llm()
    response = llm.invoke(prompt)
    response_text = str(response).strip()
    print(response_text)
    print(results)
    return response_text
    




def get_llm():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    def invoke(prompt):
        response = model.generate_content(prompt)
        return response.text.strip()
    return type("GeminiLLM", (), {"invoke": staticmethod(invoke)})()
# @app.get("/delete_collection")
# def delete_collection():
#     if os.path.exists(CHROMA_PATH):
#         shutil.rmtree(CHROMA_PATH)
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={"status": "success", "message": "Chroma vector database deleted."}
#         )
#     else:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"status": "error", "message": "Database folder does not exist."}
#         )     



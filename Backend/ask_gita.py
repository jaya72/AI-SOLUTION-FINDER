from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import chromadb
from sentence_transformers import SentenceTransformer


# Setup
app = FastAPI()
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("gita_verses")

# Request schema
class AskRequest(BaseModel):
    question: str

@app.post("/api/ask")
async def ask_gita(data: AskRequest):
    try:
        print("📨 Received question:", data.question)
        print("📦 ChromaDB count:", collection.count())

        q_embedding = embed_model.encode(data.question).tolist()
        print("🔍 Embedding done")

        results = collection.query(query_embeddings=[q_embedding], n_results=5)

        if not results["documents"] or not results["documents"][0]:
            return {"answer": "⚠️No sandeep verses found in the database."}

        print("📚 Top matches:", results["documents"][0])
        return {"answer": f"(DEBUG) Top match: {results['documents'][0][0]}"}

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print("Python Exception:", err)
        return {"error": err}

# Run server directly
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

import chromadb
from sentence_transformers import SentenceTransformer

# Load Gita Data (example: you must have it in gita.json or gita.csv)
import json

with open("gita.json", "r", encoding="utf-8") as f:
    gita_data = json.load(f)

# Initialize embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup Chroma client

client = chromadb.PersistentClient(path="./chroma_store")

collection = client.get_or_create_collection(name="gita_verses")

# Add verses to ChromaDB
for i, verse in enumerate(gita_data):
    text = verse["text"]
    chapter = str(verse.get("chapter", "")) if verse.get("chapter") is not None else ""
    verse_num = str(verse.get("verse", "")) if verse.get("verse") is not None else ""
    metadata = {
        "chapter": chapter,
        "verse": verse_num
    }
    embedding = embed_model.encode(text).tolist()

    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[f"verse_{i}"],
        embeddings=[embedding]
    )

print("✅ Gita verses added to ChromaDB!")
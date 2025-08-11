from flask import Flask, request, jsonify
import chromadb

app = Flask(__name__)

client = chromadb.Client()
collection = client.get_or_create_collection(name="gita")

@app.route('/api/ask', methods=['POST'])
def query_verse():
    data = request.json
    question = data.get("question", "")

    results = collection.query(query_texts=[question], n_results=3)
    
    response = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        response.append({
            "verse": doc,
            "chapter": meta.get("chapter"),
            "verse_number": meta.get("verse_number")
        })

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=8000)

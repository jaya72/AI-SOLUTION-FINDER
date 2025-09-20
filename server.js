const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/ask", async (req, res) => {
  const { question } = req.body;

  try {
    const response = await axios.post("http://localhost:8000/api/ask", { question });

    res.json(response.data);
  } catch (err) {
    console.error("Error querying ChromaDB:", err.message);
    res.status(500).json({ error: "Failed to get answer from ChromaDB" });
  }
});

app.listen(3000, () => {
  console.log("Node.js API running on http://localhost:3000");
});

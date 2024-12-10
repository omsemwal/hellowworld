const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// Replace with your actual API key
const API_KEY = "AIzaSyDZR6__W9vQ0utqMVLHTJWbiPF8ixEeDio";
const MODEL_ID = "gemini-1.5-flash-latest";
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent?key=${API_KEY}`;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Route for home page
app.get("/", (req, res) => {
  res.render("index.ejs");
});

// Route for summarizing short text
app.post("/search", async (req, res) => {
  const userInput = req.body.user_input;

  try {
    const response = await axios.post(
      API_URL,
      {
        contents: [{ parts: [{ text: userInput }] }],
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    const generatedText = response.data.candidates[0].content.parts[0].text;
    // Render the result template with the output
    res.json({ output: generatedText });
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .send(`Error: ${error.response.status} - ${error.response.data}`);
  }
});

// Route for summarizing long text
app.post("/summarize", async (req, res) => {
  const userInput = req.body.long_user_input;
  const prompt = `Please summarize the following text in 50-100 words:\n\n${userInput}`;

  try {
    const response = await axios.post(
      API_URL,
      {
        contents: [{ parts: [{ text: prompt }] }],
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    const generatedText = response.data.candidates[0].content.parts[0].text;
    // Render the result template with the output
    res.json({ output: generatedText });
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .send(`Error: ${error.response.status} - ${error.response.data}`);
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

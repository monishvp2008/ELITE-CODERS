import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
app.use(cors());

const GEMINI_API_KEY = "AIzaSyCuR0NuECD4o53gNss4Nudf9HDROEVEs_w";

app.get("/quiz", async (req, res) => {
    const { exam, subject } = req.query;

    const prompt = `
    Create 5 multiple choice questions for ${exam} exam
    on the subject ${subject}.
    Give options A, B, C, D and mark the correct answer.
    `;

    const response = await fetch(
        `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{ parts: [{ text: prompt }] }]
            })
        }
    );

    const data = await response.json();
    const quiz = data.candidates[0].content.parts[0].text;

    res.json({ quiz });
});

app.listen(3000, () =>
    console.log("Server running on http://localhost:3000")
);
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Serve frontend files
app.use(express.static(path.join(__dirname, "../frontend")));

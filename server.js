const express = require("express");
const axios = require("axios");
const cors = require("cors");
const { exec } = require("child_process"); // ✅ Keep only this one
require("dotenv").config(); // Load API keys

const app = express();
app.use(cors({ origin: "*" }));

const PORT = 5000;

// ✅ Route to fetch YouTube search results
app.get("/api/songs", async (req, res) => {
    console.log("📡 Received request for songs:", req.query);
    
    const { query, pageToken } = req.query;
    const apiKey = process.env.YOUTUBE_API_KEY;

    if (!apiKey) {
        console.error("❌ Missing YouTube API Key!");
        return res.status(500).json({ error: "Server misconfiguration: API key is missing." });
    }

    const apiUrl = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=20&q=${query}+audio&key=${apiKey}${pageToken ? `&pageToken=${pageToken}` : ""}`;

    try {
        const response = await axios.get(apiUrl);
        console.log("✅ Fetched Data Successfully:", response.data);
        res.json(response.data);
    } catch (error) {
        console.error("🔥 Axios Error:", error.response?.data || error.message);
        res.status(500).json({ error: error.response?.data?.error?.message || "Failed to fetch songs" });
    }
});

// ✅ Route to stream YouTube audio
app.get("/stream", async (req, res) => {
    const { videoId } = req.query;

    if (!videoId) {
        return res.status(400).json({ error: "Missing videoId parameter" });
    }

    console.log(`🎵 Streaming Audio for Video ID: ${videoId}`);

    // 🔥 Use yt-dlp to force MP3 format & stream output directly
    const command = `yt-dlp -f bestaudio --extract-audio --audio-format mp3 -o - "https://www.youtube.com/watch?v=${videoId}"`;

    try {
        const process = exec(command, { maxBuffer: 1024 * 1024 * 10 });

        // ✅ Correct Content-Type for MP3 Streaming
        res.setHeader("Content-Type", "audio/mpeg");
        res.setHeader("Content-Disposition", `inline; filename="${videoId}.mp3"`);

        process.stdout.pipe(res);
    } catch (error) {
        console.error("🔥 Error Streaming Audio:", error.message);
        res.status(500).json({ error: "Failed to stream audio" });
    }
});

// ✅ Start the server
app.get("/favicon.ico", (req, res) => res.status(204));
app.listen(PORT, () => console.log(`🔥 Backend running at http://localhost:${PORT}`));

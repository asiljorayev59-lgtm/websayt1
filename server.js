const express = require("express");
const fs = require("fs");

const app = express();

// Static fayllar
app.use(express.static("."));

/**
 * SIGNALS LIST
 */
app.get("/signals", (req, res) => {
  try {
    const data = fs.readFileSync("data/signals.json", "utf-8");
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(500).json({ error: "signals.json o‘qilmadi" });
  }
});

/**
 * HISTORY
 */
app.get("/history", (req, res) => {
  try {
    const data = fs.readFileSync("data/history.json", "utf-8");
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(500).json({ error: "history.json o‘qilmadi" });
  }
});

/**
 * SINGLE SIGNAL ✅ (FAKAT BITTA)
 */
app.get("/signal", (req, res) => {
  try {
    const data = fs.readFileSync("signals.json", "utf-8");
    res.json(JSON.parse(data));
  } catch (err) {
    res.status(500).json({ error: "signal topilmadi" });
  }
});

/**
 * SERVER
 */
app.listen(3000, () => {
  console.log("🚀 Server running on http://localhost:3000");
});

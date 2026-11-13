
import "dotenv/config";
import express from "express";
import searchRouter from "./routes/search";

const app = express();
const PORT = process.env.PORT || 5000;

app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", process.env.FRONTEND_ORIGIN || "http://localhost:5173");
  res.header("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.header("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});
app.use(express.json({ limit: "14mb" }));

app.get("/", (_req, res) => {
  res.json({
    message: "BITBYTE API is running",
  });
});

app.use("/api/search", searchRouter);

app.listen(PORT, () => {
  console.log(`BITBYTE backend running on port ${PORT}`);
});

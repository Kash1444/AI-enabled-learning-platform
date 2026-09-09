import "dotenv/config";
import express from "express";
import cors from "cors";
import { binsRouter } from "./routes/bins.js";

const app = express();
app.use(cors());
app.use(express.json({ limit: "5mb" })); // images from ESP-CAM need headroom

app.use("/api/bins", binsRouter);

app.get("/health", (req, res) => res.json({ status: "ok" }));

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`InnovaMesh backend listening on port ${port}`);
});

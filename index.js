import express from 'express'
import dotenv from 'dotenv'
import cors from 'cors'
import { createToken, refreshToken, validate } from './jwt.js'

const app = express();

dotenv.config();

app.use(express.json());
app.use(cors());

app.post('/token', async (req, res) => {
    try {
        res.json(await createToken(req.body))
    } catch (error) {
        res.status(500).json({ error : error.message })
    }
})

app.post('/validate', async (req, res) => {
    try {
        res.json({ data: await validate(req.body.token)})
    } catch (error) {
        res.status(500).json({ error : error.message })
    }
})

app.post("/refresh", async (req, res) => {
    try {
        res.json(await refreshToken(req.body.token))
    } catch (error) {
        res.status(500).json({ error : error.message })
    }
})

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0"
app.listen(PORT, HOST, () => {
    console.log(`Server is running on ${HOST}:${PORT}.`);
});
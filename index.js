import express from 'express'
import jwt from 'jsonwebtoken'
import fs from 'fs'
import dotenv from 'dotenv'

const app = express();

dotenv.config();

app.use(express.json());

async function validateToken(token) {
    var cert = fs.readFileSync('./keys/certificate.crt')
    return new Promise((resolve, reject) => {
        jwt.verify(token, cert, { algorithms: ['RS256'] }, (err, decoded) => {
            if (err) reject(err)
            else resolve(decoded)
        })
    })
}

app.post('/token', (req, res) => {
    let privateKey = fs.readFileSync('./keys/priv');
    let expired = 60 * 60
    let token = jwt.sign(req.body, privateKey, { algorithm: 'RS256', expiresIn: expired })
    res.json({ token: token, expired: expired })
})

app.post('/validate', async (req, res) => {
    let token = req.body.token
    try {
        let decodedToken = await validateToken(token)
        decodedToken.exp = new Date(decodedToken.exp * 1000)
        decodedToken.iat = new Date(decodedToken.iat * 1000)
        res.json({ data : decodedToken })
    } catch (err) {
        res.json({ error : err.message })
    }
})

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0"
app.listen(PORT, HOST, () => {
    console.log(`Server is running on ${HOST}:${PORT}.`);
});
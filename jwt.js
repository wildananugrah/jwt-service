import jwt from 'jsonwebtoken'
import fs from 'fs'
import dotenv from 'dotenv'
dotenv.config();

export async function validate(token) {
    var cert = fs.readFileSync(process.env.CERITIFICATE)
    return new Promise((resolve, reject) => {
        jwt.verify(token, cert, { algorithms: ['RS256'] }, (err, decoded) => {
            if (err) reject(err)
            else resolve(decoded)
        })
    })
}

export async function createToken(data) {
    let privateKey = fs.readFileSync(process.env.PRIVATE_KEY);
    let expired = 60 * 60 // an hour
    let token = jwt.sign(data, privateKey, { algorithm: 'RS256', expiresIn: expired })
    return { token: token, expired: expired }
}

export async function refreshToken(token) {
    const data = await validate(token)
    delete data.iat
    delete data.exp
    return await createToken(data)
}
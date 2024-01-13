# How to

Membuat aplikasi JWT

## NPM Libraries
1. express
2. jsonwebtoken
3. nodemon (optional)
4. dotenv (optional)
5. cors (optional)

- Create npm init

```sh
npm init -y
```

- Install dependencies

```sh
npm i --save nodemon express jsonwebtoken cors dotenv
```

- Update package.json

```json
{
  "name": "jwt",
  "version": "1.0.0",
  "description": "",
  "type": "module",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "dev": "nodemon index.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.2",
    "nodemon": "^3.0.1"
  }
}
```

- Create folder keys
- Create certificate and private key

```sh
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout key.key -out certificate.crt
```

- Create .env

```
PORT=5000
HOST=0.0.0.0
CERITIFICATE=./keys/certificate.crt
PRIVATE_KEY=./keys/key
```

- Create jwt.js

```js
import jwt from "jsonwebtoken";
import fs from "fs";
import dotenv from "dotenv";
dotenv.config();

export async function validate(token) {
  var cert = fs.readFileSync(process.env.CERITIFICATE);
  return new Promise((resolve, reject) => {
    jwt.verify(token, cert, { algorithms: ["RS256"] }, (err, decoded) => {
      if (err) reject(err);
      else resolve(decoded);
    });
  });
}

export async function createToken(data) {
  let privateKey = fs.readFileSync(process.env.PRIVATE_KEY);
  let expired = 60 * 60; // an hour
  let token = jwt.sign(data, privateKey, {
    algorithm: "RS256",
    expiresIn: expired,
  });
  return { token: token, expired: expired };
}

export async function refreshToken(token) {
  const data = await validate(token);
  delete data.iat;
  delete data.exp;
  return await createToken(data);
}
```

- Create index.js

```javascript
import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import { createToken, refreshToken, validate } from "./jwt.js";

const app = express();

dotenv.config();

app.use(express.json());
app.use(cors());

app.post("/token", async (req, res) => {
  try {
    res.json(await createToken(req.body));
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/validate", async (req, res) => {
  try {
    res.json({ data: await validate(req.body.token) });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/refresh", async (req, res) => {
  try {
    res.json(await refreshToken(req.body.token));
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0";
app.listen(PORT, HOST, () => {
  console.log(`Server is running on ${HOST}:${PORT}.`);
});
```
- Run the app.
```
npm run dev
```

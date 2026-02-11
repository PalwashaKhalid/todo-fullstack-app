---
name: backend-routes-db
description: Generate backend routes, handle requests/responses, and connect to databases. Use for API and server-side development.
---

# Backend API & Database Skill

## Instructions

1. **Route setup**
   - Use RESTful or API route structure  
   - Define clear endpoints (GET, POST, PUT, DELETE)  
   - Group routes by resource (e.g., /users, /products)

2. **Request & Response handling**
   - Validate incoming data  
   - Use proper HTTP status codes  
   - Return JSON responses  
   - Handle errors gracefully  

3. **Database connection**
   - Connect to SQL or NoSQL databases  
   - Use environment variables for credentials  
   - Implement basic CRUD operations  
   - Ensure secure queries  

## Best Practices
- Use async/await for database operations  
- Keep controllers and routes separated  
- Validate input to prevent security issues  
- Use middleware for authentication & logging  
- Follow REST API standards  

## Example Structure
```js
import express from "express";
import { connectDB } from "./db.js";

const app = express();
app.use(express.json());

app.get("/users", async (req, res) => {
  const users = await db.collection("users").find().toArray();
  res.status(200).json(users);
});

app.post("/users", async (req, res) => {
  const user = req.body;
  await db.collection("users").insertOne(user);
  res.status(201).json({ message: "User created" });
});

connectDB();
app.listen(3000, () => console.log("Server running"));

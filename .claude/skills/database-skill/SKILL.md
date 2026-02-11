---
name: database-skill
description: Design database schemas, create tables, and manage migrations for scalable applications.
---

# Database Skill – Schema, Tables & Migrations

## Instructions

1. **Schema Design**
   - Identify entities and relationships  
   - Normalize data (avoid redundancy)  
   - Define primary and foreign keys  

2. **Table Creation**
   - Use clear, consistent naming  
   - Choose appropriate data types  
   - Add constraints (NOT NULL, UNIQUE, FK)  

3. **Migrations**
   - Version-controlled schema changes  
   - Separate up and down migrations  
   - Avoid breaking existing data  

## Best Practices
- Use snake_case for table and column names  
- Always define primary keys  
- Index frequently queried columns  
- Keep migrations small and reversible  
- Document schema changes  

## Example Structure

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

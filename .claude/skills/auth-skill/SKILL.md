---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate input (email, password, username)
   - Hash passwords before storing
   - Prevent duplicate accounts
   - Return safe, minimal responses

2. **User Signin**
   - Verify credentials securely
   - Compare hashed passwords
   - Handle invalid login attempts gracefully
   - Issue authentication tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply proper salt rounds
   - Never store plain-text passwords
   - Support password reset flows

4. **JWT Token Handling**
   - Generate access and refresh tokens
   - Use secure secrets and expiration times
   - Validate tokens on protected routes
   - Implement token revocation when needed

5. **Better Auth Integration**
   - Configure Better Auth providers
   - Integrate session management
   - Support OAuth and email/password flows
   - Sync user data with application database

## Best Practices
- Enforce strong password rules
- Use HTTPS for all auth endpoints
- Store secrets in environment variables
- Separate auth logic from business logic
- Implement rate limiting on auth routes
- Log auth events without sensitive data

## Example Structure
```ts
// Signup
POST /auth/signup
- validate input
- hash password
- save user
- return success response

// Signin
POST /auth/signin
- verify credentials
- generate JWT
- return token

// Protected Route
GET /profile
- verify JWT
- return user data

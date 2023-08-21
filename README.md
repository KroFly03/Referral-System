# Referral-System

# API Documentation


## Requirements

* Docker version 23.0.6
* Django 4.2.4
* Pytest 7.4.0

## Build

```bash
sudo docker-compose up --build -d
```

## Endpoints

The API offers the following endpoints:

- **POST /auth/login**: Log in a user and receive authentication tokens.
- **POST /auth/refresh**: Refresh the access token using a valid refresh token.
- **POST /auth/register**: Register a new user.
- **POST /auth/verify**: Verify a user's authorization code.
- **GET /schema**: Retrieve the OpenAPI schema for this API.
- **PATCH /users/activate_invite_code**: Activate an invite code for the user.
- **GET /users/invited_by**: List users who were invited by the authenticated user.
- **GET /users/me**: Retrieve the details of the authenticated user.
- **PATCH /users/me**: Update the details of the authenticated user.

## Schemas

The API uses the following schemas:

- **ActivateInviteCode**: Object representing an invite code to be activated.
- **PatchedActivateInviteCode**: Object for partially updating an invite code.
- **PatchedUserDetail**: Object for partially updating user details.
- **TokenRefresh**: Object representing token refresh data.
- **UserDetail**: Object representing user details.
- **UserList**: Object representing a list of users.
- **UserLogin**: Object representing user login data.
- **UserRegister**: Object representing user registration data.
- **VerifyCode**: Object representing user verification data.

## Response Formats

Responses are returned in JSON format.

## Getting OpenAPI Schema

To retrieve the OpenAPI schema for this API, make a GET request to the `/schema` endpoint. You can specify the format using the `format` parameter (json or yaml) and the language using the `lang` parameter.

## Security

The API uses JWT (JSON Web Token) for authentication. Include the token in the `Authorization` header of your requests.

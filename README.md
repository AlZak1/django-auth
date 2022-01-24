# django-auth
The app provides authentication system, using jwt token

There are 4 urls 
  1 Sing up - provides registration of users
  2 Sign in - check if user exists and return jwt token for access to next pages, put jwt token to the cookies
  3 User - you can retrieve user via jwt located in the cookies
  4 Logut - delete jwt token from cookies, so you can retrieve user without token in cookies

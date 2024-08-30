# Social Media
This api was made by https://github.com/VladyslavBazhyn in case of learning Django Rest Framework by task of https://github.com/mate-academy

## Features
In this social media you can:
- Create an account
- Take tokens (access and refresh) for getting access for all endpoints
- Change your user credentials like password and email on special pages
- Invalidate your tokens to logout from site
- Create posts and read posts of other users
- Delete, change and get list of all of your tokens
- Follow and unfollow to other users
- Search for current user and post by specific criteria

### To run this api on your computer you need:
- Install Docker
- in terminal: 
  - 'docker build -t docker-social-media .'
  - docker run -p 8001:8765 docker-social-media
- On page http://127.0.0.1:8001/users/register/ create a user
- On page http://127.0.0.1:8001/users/token/ take access token

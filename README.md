# ABDUL as Facebook Messenger Bot

Setting at https://dashboard.heroku.com/apps/<myappname>/settings
- Create Heroku App with Python buildpack

Config Variables 
- BOT_ID
- BOT_ACCESS_TOKEN
- PAGE_ACCESS_TOKEN (from your Facebook Application)
- VERIFY_TOKEN (from your Facebook Application)

Deploy
- $ heroku login
- $ git init
- $ heroku git:remote -a <myappname>
- $ git add .
- $ git commit -m "Initial commit"
- $ git push heroku master
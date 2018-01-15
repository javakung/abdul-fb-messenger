# ABDUL as Facebook Messenger Bot

Setting
- Create Heroku App with Python buildpack
- Config Variables 
	- BOT_ID
	- BOT_ACCESS_TOKEN
	- PAGE_ACCESS_TOKEN (from your Facebook Application)
	- VERIFY_TOKEN (from your Facebook Application)


Deploy to Heroku without edit anything 
- $ heroku login
- $ git init
- $ heroku git:remote -a <myappname>
- $ git add .
- $ git commit -m "Initial commit"
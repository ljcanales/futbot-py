[![GitHub license](https://img.shields.io/github/license/ljcanales/FutBot)](https://github.com/ljcanales/FutBot/blob/master/LICENSE)
[![Twitter Follow](https://img.shields.io/twitter/follow/FutBot_?style=social)](https://twitter.com/FutBot_)
# FutBot
![photo](https://github.com/ljcanales/futbot-py/blob/master/outputs/futbot_200x200.png)

Bot that posts matches via Twitter [Twitter](https://twitter.com/FutBot_) and [Instagram](https://www.instagram.com/futbot__/).

**TWITTER**
- Posts matches of the day (by tournament).
- Posts match (with image, if possible).
- Match reminder to followers.

**INSTAGRAM**
- Posts match (Instagram Story).

# Installation
Clone repository.
```
git clone https://github.com/ljcanales/futbot-py && cd futbot-py
```

(Optional) Create virtual environment and activate it.
```
python3 -m venv env
source env/bin/activate
```

Install dependencies.
```
pip3 install -r requirements.txt
```

# Configuration
Environment variables.
```
export API_MATCHES=...
export API_TEAMS=...
```

# Usage
```python
from futbot import Bot

bot_settings = {
    'instagram' : {
        'username' : '',
        'password' : ''
    },
    'twitter': {
        'api_key' : '',
        'api_secret' : '',
        'access_key' : '',
        'access_secret' : ''
    },
    'uri' : {
        'api_matches' : '',
        'api_teams' : ''
    },
    'config' : {
        "send_match_message": False,
        "tweet_match" : True,
        "post_story_match" : False,
        "update_config" : True
    }
}

bot = Bot(settings=bot_settings)
bot.save_settings('./bot-settings.json')
```
Next time
```python
from futbot import Bot

bot = Bot(settings_path='./bot-settings.json')
```
# Accounts

- Twitter: [@FutBot_](https://twitter.com/FutBot_)
- Instagram: [@futbot__](https://www.instagram.com/futbot__/)

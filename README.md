[![GitHub license](https://img.shields.io/github/license/ljcanales/FutBot)](https://github.com/ljcanales/FutBot/blob/master/LICENSE)
[![Twitter Follow](https://img.shields.io/twitter/follow/FutBot_?style=social)](https://twitter.com/FutBot_)
# FutBot

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
export API_KEY=...
export API_SECRET=...
export ACCESS_KEY=...
export ACCESS_SECRET=...
export UN_IG=...
export P_IG=...
export API_MATCHES=...
export API_TEAMS=...
```

Edit file `config_file.json` (true/false):

```
{
 "send_match_message": false,
 "tweet_match" : true,
 "post_story_match" : true,
 "update_config" : true
}
```

# Accounts

- Twitter: [@FutBot_](https://twitter.com/FutBot_)
- Instagram: [@futbot__](https://www.instagram.com/futbot__/)

[![Twitter Follow](https://img.shields.io/twitter/follow/FutBot_?style=social)](https://twitter.com/FutBot_)
# FutBot

Bot que publica en **Twitter** los partidos del día correspondientes a los torneos especificados. Además, recuerda antes de cada uno de ellos.

> Dependencias:
> 
> - [Tweepy](https://www.tweepy.org/) (para conectarse a [TwitterAPI](https://developer.twitter.com/en/docs/twitter-api))
> - [Requests](https://docs.python-requests.org/)
> - [Pillow](https://pillow.readthedocs.io/)
> - [...](https://github.com/ljcanales/FutBot/blob/master/requirements.txt)


### Twitter Account

Follow [@FutBot_](https://twitter.com/FutBot_)

### Sequence Diagram

```mermaid
	sequenceDiagram;
		participant F as FutBot;
		participant A as API_Sports;
		participant T as TwitterAPI;
		F->>+ A: getTournament();
		A-->>-F: Tournament;
		F->> T: publish(Tournament);

		F->> T: publish(Match);

		Note over F,T: Si falta menos de una hora;
```


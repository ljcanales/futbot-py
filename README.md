# FutBot

Bot que publica en **Twitter** los partidos del día de los torneos especificados. Y recuerda antes de cada uno de ellos.


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


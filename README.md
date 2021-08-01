[![GitHub license](https://img.shields.io/github/license/ljcanales/FutBot)](https://github.com/ljcanales/FutBot/blob/master/LICENSE)
[![Twitter Follow](https://img.shields.io/twitter/follow/FutBot_?style=social)](https://twitter.com/FutBot_)
# FutBot

Bot que publica partidos vía Twitter e Instagram.

**TWITTER**
- Publica los partidos del dia (por torneo).
- Publica partido (con imagen, en caso que sea posible).
- Recordatorio de partido a los seguidores.

**INSTAGRAM**
- Publica partido (Instagram Story).

# Instalación
Clonar repositorio
```
git clone https://github.com/ljcanales/futbot-py
cd futbot-py
```

(Opcional) Crear entorno virtual y activarlo
```
python3 -m venv env
source env/bin/activate
```

Instalar dependencias.
```
pip3 install -r requirements.txt
```

# Configuración
Variables de entorno.
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

Editar el archivo `config_file.json` (true/false):

```
{
 "send_match_message": false,
 "tweet_match" : true,
 "post_story_match" : true,
 "update_config" : true
}
```

# Cuentas

- Twitter: [@FutBot_](https://twitter.com/FutBot_)
- Instagram: [@futbot__](https://www.instagram.com/futbot__/)



[![GitHub license](https://img.shields.io/github/license/ljcanales/FutBot)](https://github.com/ljcanales/FutBot/blob/master/LICENSE)
[![Twitter Follow](https://img.shields.io/twitter/follow/FutBot_?style=social)](https://twitter.com/FutBot_)
# FutBot

Bot que publica partidos vía Twitter e Instagram.

**TWITTER**
- Publica tweet con los partidos del dia (un tweet por torneo).
- Publica tweet con imagen por partido (antes de cada partido).
- Envia mensaje directo como recordatorio a los seguidores (adjuntando url al tweet).

**INSTAGRAM**
- Publica story con imagen por partido (antes de cada partido).

# Instalación
Instalar paquetes.
```
pip3 install -r requirements.txt
```
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

# Configuración
Editar el archivo `config_file.json` con los valores deseados (true/false):

```
{
 "send_match_message": true,
 "tweet_match" : true,
 "post_story_match" : true,
 "update_config" : true
}
```

# Cuentas

- Twitter: [@FutBot_](https://twitter.com/FutBot_)
- Instagram: [@futbot__](https://www.instagram.com/futbot__/)



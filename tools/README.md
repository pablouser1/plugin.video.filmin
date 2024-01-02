# Desarrollo
En esta carpeta encontrarás diferentes utilidades para el desarrollo de este programa

Antes de emepezar, instala las dependencias de Python con:

```bash
pip3 install -r requirements.txt
```

## Checker
Puedes ejecutar manualmente los tests con el comando
```bash
kodi-addon-checker --branch matrix ..
```

NOTA: Usamos el path `..` para ir al directorio raíz donde está el addon

## Api
Puedes ejecutar la API manualmente copiando el script `api_m.example.py` a `api_m.py`.

Aquí puedes hacer todas las pruebas que quieras sin tener que usar Kodi

## Reversing
### Static
Todos los tokens `CLIENT_ID` y `CLIENT_ID_SECRET` se encontraron decompilando la aplicación de Android.

Personalmente uso [**jadx**](https://github.com/skylot/jadx) para la decompilación.

### Runtime
Gran parte de los endpoints del archivo `api.py` se han encontrado interceptando las peticiones HTTPS de la aplicación de Android

El setup que uso personalmente es:
- [**mitmproxy**](https://mitmproxy.org), para interceptar las solicitudes
- [**MagiskTrustCert**](https://github.com/NVISOsecurity/MagiskTrustUserCerts), módulo de [Magisk](https://github.com/topjohnwu/Magisk) para el tráfico HTTPS

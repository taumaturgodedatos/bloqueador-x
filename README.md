# Bloqueador de cuentas para Twitter X

Créditos e idea original: [@polariscopio](https://twitter.com/polariscopi0). Parte de este código fué adaptado a partir de su [trabajo](https://t.co/oaA5W8KlZm). La idea es facilitar la tarea a usuari@s mediante una interfaz amigable.

## 📢 Usar APP con Streamlit Cloud

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

## 📝 Descripción

Esta aplicación permite cargar una lista de usuarios en formato `.csv` (valores separados por coma).

El archivo `.csv` debe tener el siguiente formato:

```
usuario,id
usuario1,id_usuario1
usuario2,id_usuario2
usuario3,id_usuario3
...

```
**Notar que la primer fila (o línea) debe respetar los nombres: `usuario` y `id`.**
**Notar que no hay espacios entre `usuario` e `id`**

A modo de ejemplo puede usar el `.csv` de ejemplo que se encuentra [acá](https://github.com/taumaturgodedatos/bloqueador-lista-x/blob/main/example/blocklist.csv)
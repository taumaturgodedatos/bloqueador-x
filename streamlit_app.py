import streamlit as st
import os

import time
from tweety import Twitter
from tweety.exceptions_ import ActionRequired
import json
from datetime import date
import pandas as pd

"""
# Bloqueador de cuentas de twitter

Esta es una versión más fácil de utilizar 😉.
"""

def get_list_of_followers(file, app):
    print(file)
    #with st.spinner('Procesando cuentas ...'):  
    user_df = pd.read_csv(file)
    file.seek(0)

    user_list = user_df.to_dict('records')
    print('list: ', user_list)

    follower_list = []
    for user in user_list:
        print('==', user)
        try:
            followers = app.get_user_followers(user['usuario'])
            follower_list.append({'User': user, 'Follower list': followers})
        except Exception as e:
            print(e)
        

    return follower_list

def get_list_of_users(file):
    print(file)
    #with st.spinner('Procesando cuentas ...'):  
    user_df = pd.read_csv(file)
    file.seek(0)

    user_list = user_df.to_dict('records')
    print('list: ', user_list)

    users_list = []
    for user in user_list:
        print('==', user)
        try:
            users_list.append({'User': user})
        except Exception as e:
            print(e)

    return users_list


"""
### Cargar listado de cuentas

El archivo a procesar debe tener formato .csv (valores separados por coma), es decir, debe tener la siguiente pinta:

```
usuario,id  
usuario1,id_usuario1  
usuario2,id_usuario2  
usuario3,id_usuario3  
...
```  

Notar que la primera fila debe contener los nombres de las columnas: `usuario` e `id`. **¡No modifique estos nombres!**  
El dato del `id` es importante ya que es lo que se utiliza para bloquear una cuenta. 
"""

uploaded_file = st.file_uploader("A continuación cargue el listado de cuentas a bloquear (debe ser en formato .CSV como se indica arriba)", type=['csv'])


"""
### Ingrese sus datos de cuenta de Twitter X:
"""

user = st.text_input('USUARIO')
password = st.text_input('CONTRASEÑA', type='password')

def start_twitter(u, p):
    # Debemos chequear que no haya quedado guardado un archivo de sesión
    try:
        os.remove("session.tw_session")
    except:
        pass

    app = Twitter("session")

    try:
        
        app.sign_in(u, p)
        #print(app.user)
        #return app

    except ActionRequired as e:
        print('EXTRA: ', e)
        action = st.text_input(f"Action Required :> {str(e.message)} : ")
        if action:
            app.sign_in(u, p, action)
            #return app

    return app

def get_csv_of_followers(followers):

    follower_list = []
    for user in followers:
        for follower in user['Follower list']:
            follower_list.append({'usuario': follower['username'], 'id': follower['id'], 'verificado': follower['verified']})

    df = pd.DataFrame.from_records(follower_list, columns=['usuario', 'id', 'verificado'])

    #print(df)

    return df.to_csv(index=False).encode('utf-8')


def bloquear_simple(users, user, password, app):

    blocklist = {x['User']['usuario']: x['User']['id'] for x in users}

    print('BLOCKLIST: ', blocklist)

    TIME = 2
    large_wait = TIME*60

    success_block = []
    unsuccess_block = []
    errors_in_a_row = 0
    try:
        blocked_users = [i.id for i in app.get_blocked_users().users]
    except Exception as e:
        print(e)
        return

    print(blocked_users)

    for n, (k,v) in enumerate(blocklist.items()):
        if n%10 == 0:
            time.sleep(TIME)
        if n == 499:
            print(f"El script retoma su trabajo en {large_wait} segundos")
            time.sleep(TIME*60)
        if errors_in_a_row > 10:
            print("Es probable que se haya alcanzando el límite de blocks diarios. Se volverá a intentar volviendo a abrir la cuenta")
            try:
                app = start_twitter(user,password)
            except:
                print("Falló segundo intento... probá nuevamente mañana")
                break
        if v in success_block or v in blocked_users:
            continue
        try:
            app.block_user(f"{v}")
            print(f"{n}/{len(blocklist)}: {k} bloqueado correctamente")
            success_block.append(v)
            errors_in_a_row = 0
        except:
            print(f"{n}/{len(blocklist)}: {k} no pudo ser bloqueado")
            time.sleep(TIME)
            unsuccess_block.append(v)
            errors_in_a_row += 1


    print(f"Quedaron {len(unsuccess_block)} usuarios sin bloquear, si desea reintentar recursivamente corra la celda inferior. Si alcanzó el límite diario de bloqueos intente posteriormente, se podrá descargar una lista para continuar luego")


def bloquear_seguidores(followers):
    pass

def log_user(user, password):
    #with st.spinner('Logueando usuario ...'):
    try:
        app = start_twitter(user, password)
    except Exception as e:
        print(e)
        st.error('No se pudo loguear, revise usuario y/o contraseña!', icon="🚨")
        return

    return app


def click_button(user, password):

    if(user=="" or password==""):
        st.error('Usuario o contraseña vacios!', icon="🚨")
        return

    try:
        app = start_twitter(user, password)
    except Exception as e:
        st.write(e)
        return

   
    try:
        print('estoy acà', app)
        followers = get_list_of_followers(uploaded_file, app)
        users = get_list_of_users(uploaded_file)
    except Exception as e:
        print("Error in getting followers: ", e)
        st.error('No se encontró el archivo .csv. Asegurese de cargar un archivo con el formato adecuado!', icon="🚨")
        return

    for user in followers:
        st.write('##########################################################')
        st.write(f"Total de seguidores del usuario: {user['User']}:")
        st.write(f"{len(user['Follower list'])}")


    csv_2_export = get_csv_of_followers(followers)

    st.download_button(
        "Descargar listado de seguidores",
        csv_2_export,
        "lista_seguidores_export.csv",
        "text/csv",
        key='download-csv'
    )

    st.button('Bloquear cuentas del archivo inicial', on_click=bloquear_simple, args=(users, user, password, app))
    #st.button('Bloquear seguidores (¡ojo!)', on_click=bloquear_seguidores, args=(followers, user, password))



st.button('Procesar listado', on_click=click_button, args=(user, password))








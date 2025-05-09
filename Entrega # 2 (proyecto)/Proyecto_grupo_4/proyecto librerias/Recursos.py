import requests

def establecer_aut(usuario, contraseña):
    global auth
    auth = (usuario, contraseña)

def obtener_recursos():
    try:
        reponse = requests.get('http://localhost:5000/Recursos/',auth=auth)
        reponse.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'Error al obtener Recursos: {e}')
        return []
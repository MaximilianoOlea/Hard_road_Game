#Sirve para mostrar las hitboxs de los personajes, como ponerlo en modo admin
DEBUG = False

def change_mode ():
    global DEBUG
    DEBUG = not DEBUG

def get_mode():
    return DEBUG
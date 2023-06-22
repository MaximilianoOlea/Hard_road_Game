import pygame


def get_rectangles(rect_principal: pygame.Rect) -> dict:
    # un rectangulo principal se rodeará de rectangulos que serviran como colisionadores
    #Un rectangulo se dibuja a partir de la esquina superior izquierd
    diccionario = {}
    diccionario["main"] = rect_principal
    diccionario["bottom"] = pygame.Rect(
        rect_principal.left, rect_principal.bottom-10, rect_principal.width, 10) #Saco 6 pixeles al bottom principal para que se dibuje de forma inversa
    diccionario["right"] = pygame.Rect(
        rect_principal.right - 4, rect_principal.top, 4, rect_principal.height)
    diccionario["left"] = pygame.Rect(
        rect_principal.left, rect_principal.top, 4, rect_principal.height)
    diccionario["top"] = pygame.Rect(
        rect_principal.left, rect_principal.top, rect_principal.width, 10)
    
    return diccionario



def turn_images(images: list, flip_x: bool, flip_y: bool):
    rotated_image = []

    for image in images:
        rotated_image.append(pygame.transform.flip(image, flip_x, flip_y))
    return rotated_image


def resize_image(images: list, size: tuple):
    """_summary_
    Redimensiona una lista de imagenes
    Args:
        images (list): Lista de imagenes que va a cambiar de tamaño
        size (tuple): tamaño que va a tener la lista de imagenes
    """
    for i in range(len(images)):
        images[i] = pygame.transform.scale(images[i], size)



def resize_animations(animations:list,size:tuple):
    """_summary_
    Se redimensiona una lista de animaciones (tipo diccionario)
    Args:
        animations (list): Lista de animaciones que se va a redimensionar
        size (tuple): tamaño que va a tener la lista de animaciones
    """
    for key in animations:
        resize_image(animations[key],(size))


def obtener_rectangulos(rect_principal: pygame.Rect) -> dict:
    # un rectangulo principal se rodeará de rectangulos que serviran como colisionadores
    #Un rectangulo se dibuja a partir de la esquina superior izquierd
    diccionario = {}
    diccionario["main"] = rect_principal
    diccionario["bottom"] = pygame.Rect(
        rect_principal.left, rect_principal.bottom-10, rect_principal.width, 10) #Saco 6 pixeles al bottom principal para que se dibuje de forma inversa
    diccionario["right"] = pygame.Rect(
        rect_principal.right - 4, rect_principal.top, 4, rect_principal.height)
    diccionario["left"] = pygame.Rect(
        rect_principal.left, rect_principal.top, 4, rect_principal.height)
    diccionario["top"] = pygame.Rect(
        rect_principal.left, rect_principal.top, rect_principal.width, 10)
    
    return diccionario

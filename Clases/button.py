import pygame

class Button ():
    def __init__(self,position,image,size):

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.clicked = False


    def draw(self,surface): 
        surface.blit(self.image,(self.rect.x,self.rect.y))

        action = False
        pos_mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos_mouse):
            #Click izquierdo
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                self.clicked = True
                action = True
                print ("Clickeo")

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
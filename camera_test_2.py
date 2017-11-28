import pygame
import pygame.camera

pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1080,720))
cam.start()
img = cam.get_image()
pygame.image.save(img,"test_shot.jpg")

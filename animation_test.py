import pygame, os
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Animation Test")

dir = os.getcwd()
dir1 = os.path.join(dir, "exported")
dir2 = os.path.join(dir1, "new_char")
directory = os.path.join(dir2, "updown")
print(directory)

walkRight = [pygame.image.load(os.path.join(directory,'new_char0.png')), 
pygame.image.load(os.path.join(directory,'new_char1.png')), pygame.image.load(os.path.join(directory,'new_char2.png')), 
pygame.image.load(os.path.join(directory,'new_char3.png')), pygame.image.load(os.path.join(directory,'new_char4.png')), pygame.image.load(os.path.join(directory,'new_char5.png')), 
pygame.image.load(os.path.join(directory,'new_char6.png')), pygame.image.load(os.path.join(directory,'new_char7.png')), pygame.image.load(os.path.join(directory,'new_char8.png')),
pygame.image.load(os.path.join(directory,'new_char9.png')),pygame.image.load(os.path.join(directory,'new_char10.png'))
]
walkLeft = [pygame.image.load(os.path.join(directory,'new_char0.png')), 
pygame.image.load(os.path.join(directory,'new_char1.png')), pygame.image.load(os.path.join(directory,'new_char2.png')), 
pygame.image.load(os.path.join(directory,'new_char3.png')), pygame.image.load(os.path.join(directory,'new_char4.png')), pygame.image.load(os.path.join(directory,'new_char5.png')), 
pygame.image.load(os.path.join(directory,'new_char6.png')), pygame.image.load(os.path.join(directory,'new_char7.png')), pygame.image.load(os.path.join(directory,'new_char8.png')),
pygame.image.load(os.path.join(directory,'new_char9.png')),pygame.image.load(os.path.join(directory,'new_char10.png'))
]
char = pygame.image.load(os.path.join(directory,'new_char0.png'))
char = pygame.transform.scale(char,(6*26,6*42))
bg = pygame.image.load('bg.jpg')

for item in range(len(walkRight)):
    walkRight[item] = pygame.transform.scale(walkRight[item],(6*26,6*42))

for items in range(len(walkLeft)):
    walkLeft[items] = pygame.transform.scale(walkLeft[items],(6*26,6*42))

x = 50
y = 50
width = 40
height = 60
vel = 5

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0

def redrawGameWindow():
    # We have 9 images for our walking animation, I want to show the same image for 3 frames
    # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 9 images shown
    # 3 times each animation.
    global walkCount
    
    win.blit(bg, (0,0))  

    if walkCount + 1 >= 33:
        walkCount = 0
        
    if left:  # If we are facing left
        win.blit(walkLeft[walkCount//3], (x,y))  # We integer divide walkCounr by 3 to ensure each
        walkCount += 1                           # image is shown 3 times every animation
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x, y))  # If the character is standing still
        
    pygame.display.update() 
    
    


run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > vel: 
        x -= vel
        left = True
        right = False

    elif keys[pygame.K_RIGHT] and x < 500 - vel - width:  
        x += vel
        left = False
        right = True
    
    else: # If the character is not moving we will set both left and right false and reset the animation counter (walkCount)
        left = False
        right = False
        walkCount = 0
        
    if not(isJump): 
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 10
            isJump = False

    redrawGameWindow() 
    
    
pygame.quit()
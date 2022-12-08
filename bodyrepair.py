def body_craft(leftlimbx,rightlimbx,leftsidelimbx,rightsidelimbx,iteration):
    skin_display = blank_template.copy()
    skin_draw = ImageDraw.Draw(skin_display) # skin for game
    img_skin_display = blank_template.copy()
    img_skin_draw = ImageDraw.Draw(img_skin_display) # skin for the sprites
    skin_draw.rectangle((12,10,18,17), fill=color, outline=color) # head
    skin_draw.rectangle((11,17,19,31), fill=color, outline=color) # body
    img_skin_draw.rectangle((10,6,17,12), fill=color, outline=color) # head
    img_skin_draw.rectangle((9,13,18,26), fill=color, outline=color) # body
    # front body
    if iteration == 0:
        skin_draw.rectangle((8+leftlimbx,17,10+leftlimbx,27), fill=color, outline=color) # left arm
        skin_draw.rectangle((20+rightlimbx,17,22+rightlimbx,27), fill=color, outline=color) # right arm
        img_skin_draw.rectangle((5+leftlimbx,13,8+leftlimbx,26), fill=color, outline=color) # left arm
        img_skin_draw.rectangle((19+rightlimbx,13,22+rightlimbx,26), fill=color, outline=color) # right arm
        skin_draw.rectangle((11+leftlimbx,31,13+leftlimbx,43), fill=color, outline=color) # left leg
        skin_draw.rectangle((17+rightlimbx,31,19+rightlimbx,43), fill=color, outline=color) # right leg
        img_skin_draw.rectangle((9+leftlimbx,27,12+leftlimbx,40), fill=color, outline=color) # left leg
        img_skin_draw.rectangle((15+rightlimbx,27,18+rightlimbx,40), fill=color, outline=color) # right leg
    # side body
    else:
        img_skin_draw.rectangle((12+leftsidelimbx,17,15+leftsidelimbx,27), fill=color, outline=color) # side arm
        skin_draw.rectangle((14+leftsidelimbx,17,16+leftsidelimbx,27), fill=color, outline=color) # side arm
        img_skin_draw.rectangle((12+leftsidelimbx,27,15+leftsidelimbx,40), fill=color, outline=color) # left leg
        skin_draw.rectangle((14+leftsidelimbx,31,16+leftsidelimbx,40), fill=color, outline=color) # left leg
        img_skin_draw.rectangle((12+rightsidelimbx,27,15+rightsidelimbx,40), fill=color, outline=color) # right leg
        skin_draw.rectangle((14+rightsidelimbx,31,16+rightsidelimbx,40), fill=color, outline=color) # right leg
    return [skin_display,img_skin_display]

class skin_anim():
    def __init__(self,color,direction,animationnum):
        self.color = color
        if direction == 1:
            self.direction = "side"
        else:
            self.direction = "updown"
        self.sprites = []
        self.animation_num = animationnum

# goes through each of the skin colors and draws each of them

# DRAW ANIMATIONS FOR THE EXPORT??

#animations = [[0,0,0,0,1],[1,-1,1,-1,1],[2,-2,2,-2,1],[3,-3,3,-3,1],[2,-2,2,-2,1],[1,-1,1,-1,1],[0,0,0,0,1],[-1,1,-1,1,1],[-2,2,-2,2,1],[3,-3,3,-3,1],[2,-2,2,-2,1],[-1,1,-1,1,1],[0,0,0,0,0],[1,0,1,0,0],[2,0,2,0,0],[3,0,3,0,0],[2,0,2,0,0],[1,0,1,0,0],[0,0,0,0,0],[-1,0,-1,0,0],[-2,0,-2,0,0],[-1,0,-1,0,0],[0,0,0,0,0]]
for color in skincolors:
    new_skin = []
    # creates body
    for iteration in range(2):
        #for num, position in (enumerate(animations)): # for each animation
            #if position[4] == iteration:
                #skin_display = body_craft(position[0],position[1],position[2],position[3],iteration) # creates the skins 
                skin_display[0].save("gametemp.png") # saves the game version
                skin_display[1].save("imgtemp.png") # saves the image version
                width,height = skin_display[0].size
                name_storage = color
                new_skin.append(skin_anim(color,position[4],num)) # 1 means front/back, 0 means side
                new_skin[-1].sprites.append(orientation(pygame.image.load("gametemp.png"),Image.open("imgtemp.png")))
                new_skin[-1].sprites[-1].name = name_storage
                new_skin[-1].sprites[-1].gamefile = pygame.transform.scale(new_skin[-1].sprites[-1].gamefile,(12*width,12*height))
                side_arm = blank_template.copy()
                skin_draw = ImageDraw.Draw(side_arm)
                if position[4] == 1:
                    img_side_arm = blank_template.copy()
                    img_skin_draw = ImageDraw.Draw(img_side_arm)
                    skin_draw.rectangle((14,17,16,28), fill=color, outline=color) # arm
                    img_skin_draw.rectangle((12,13,15,26), fill=color, outline=color) # arm
                    img_side_arm.save("imgtemp.png")
                    skin_display[0].save("temp.png")
                    width,height = side_arm.size
                    name_storage = color
                    new_skin.append(skin_anim(color,position[4],num))
                    new_skin[-1].sprites.append(orientation(pygame.image.load("temp.png"),Image.open("imgtemp.png")))
                    new_skin[-1].sprites[-1].name = name_storage
                    new_skin[-1].sprites[-1].gamefile = pygame.transform.scale(new_skin[-1].sprites[-1].gamefile,(12*width,12*height))
                skins.append(new_skin)
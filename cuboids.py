# TO DO:

# Export sprites
# Delete temporary sprites

# Imports packages

import pygame, os, time, random
from PIL import Image, ImageFile, ImageDraw
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Initializes pygame window

pygame.init()

w = 900
h = 600

win = pygame.display.set_mode((w,h))

# Classes

# each instance of this stores a body part

class body_part:
    def __init__(self,part):
        self.part = part
        self.items = {}

# each instance of this stores a clothing item

class clothing_item:
    def __init__(self,name):
        self.name = name
        self.sprites = {}

# each instance of this stores a sprite of the clothing item

class orientation:
    def __init__(self,gamefile,imgfile):
        self.gamefile = gamefile
        self.imgfile = imgfile
        self.direction = None
        self.side = None
        self.x = None
        self.y = None
        self.gamex = None
        self.gamey = None
        self.iconx = None
        self.icony = None
        self.name = None

    def orientation(self,name):
        self.name = name
        if "f" in name: # element is on front side of body
            self.direction = 1 #front
        if "l" in name: # element is on left side of body
            self.direction = 2 # left
        if "b" in name: # element is on back side of body
            self.direction = 3 #back
        if "r" in name: # element is on right side of body
            self.direction = 4 #right
        if "g" in name: # limb is on left side of body
            self.side = 1 # left limb
        if "d" in name: # limb is on right side of body
            self.side = 2 # right limb
            
    # gets items into the correct coordinates        
    
    def coord(self,part):
        self.iconx = 10
        self.icony = 10
        if part == "arm":
            self.gamey = 120
            self.y = 30
            if self.direction == 1 or self.direction == 3: # if its the sides
                if self.side == 1: # if left side
                    self.gamex = -30
                    self.x = 3
                    self.iconx += 2
                else: # if right side
                    self.gamex = 120
                    self.x = 15
                    self.iconx += 53
                self.icony += 17
            else: # if its the front or back
                self.gamex = 45
                self.x = 9
        if part == "body":
            self.iconx -= 5
            self.icony -= 5
            self.gamex = 9
            self.gamey = 120
            self.x = 6
            self.y = 10
        if part == "1head":
            self.gamex = 9
            self.gamey = 0
            self.x = 6
            self.y = 0
        if part == "leg":
            self.gamey = 300
            self.y = 24
            if self.direction == 1 or self.direction == 3: # if its the sides
                if self.side == 1: # if left side
                    self.gamex = 9
                    self.x = 6
                    self.iconx -= 10
                else: # if right side
                    self.gamex = 81
                    self.x = 12
                    self.iconx += 10
            else: # if its the front or back
                self.gamex = 45
                self.x = 9
        # moves these items towards the center on game
        self.gamex += 130 
        self.gamey += 100

# responsible for the icons the button icons which allow player to customize features

class display_icon():
    def __init__(self,display_num,name):
        self.id = None
        self.part_id = None
        self.name = name
        self.x = None
        self.y = None
        self.display_num = display_num
        self.imgfile = None
        self.gamefile = None
        
    # adds an image file to be used with PIL
    
    def add_img(self,image):
        self.imgfile = image

    # adds an image file to be used with pygame

    def add_gimg(self,image):
        self.gamefile = image
    
    # gives the icon an id, which gives it a coordinate
    
    def init_id(self,identification,part_id,row,col,mode):
        self.id = identification
        self.part_id = part_id
        if mode == "icon":
            self.x = w-col*100-100
            self.y = row*100
        if mode == "button":
            self.x = 450
            self.y = identification*100
        if mode == "showright":
            self.x = 400
            self.y = 0
        if mode == "showleft":
            self.x = 0
            self.y = 0
        if mode == "export":
            self.x = 400
            self.y = 500
    
    # pasting arms and body together make its coordinates 5 off so it adjusts to make it look the same as others
    
    def coord_adjust(self):
        self.x -= 5
        self.y -= 5

# checks the wheel and allows scrolling of the side bars

def wheel_check(index_check):
    if maxy[display] > 0:
        wheel_y[index_check] += event.y
        if wheel_y[index_check] <= 0:
            wheel_y[index_check] = 0
        elif x >= 450 and x <= 500:
            if wheel_y[index_check] >= buttonmaxy:
                wheel_y[index_check] = buttonmaxy
        else:
            if wheel_y[1] >= maxy[display]:
                wheel_y[1] = maxy[display]
        for wheelnum in range(len(wheel_y)):
            if not wheelnum == 0:
                wheel_y[wheelnum] = 0

# creates skins

blank_template = Image.open("blanksprite.png")
skins = []
skincolors = []
skin_icons = []

# reads hex codes of skin colors that can be chosen

file = open("skintones.csv")
line = file.readline()
totaldata = []
for line in file:
    # Split by semi-colon
    linedata = line.split(",")
    skincolors.append(f"#{linedata[0]}")

blank_display = Image.open("blank_display.png")
row = 0
col = 0
part_id = 0
idcounter = 0

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

animations = [[0,0,0,0,1],[1,-1,1,-1,1],[2,-2,2,-2,1],[3,-3,3,-3,1],[2,-2,2,-2,1],[1,-1,1,-1,1],[0,0,0,0,1],[-1,1,-1,1,1],[-2,2,-2,2,1],[3,-3,3,-3,1],[2,-2,2,-2,1],[-1,1,-1,1,1],[0,0,0,0,0],[1,0,1,0,0],[2,0,2,0,0],[3,0,3,0,0],[2,0,2,0,0],[1,0,1,0,0],[0,0,0,0,0],[-1,0,-1,0,0],[-2,0,-2,0,0],[-1,0,-1,0,0],[0,0,0,0,0]]
for color in skincolors:
    new_skin = []
    # creates body
    for iteration in range(2):
        for num, position in (enumerate(animations)): # for each animation
            if position[4] == iteration:
                skin_display = body_craft(position[0],position[1],position[2],position[3],iteration) # creates the skins 
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
    
    # creates skin icon to change it
    skin_icon = blank_display.copy()
    skin_draw = ImageDraw.Draw(skin_icon)
    skin_draw.rectangle((20,20,80,80),fill=color, outline=color)
    skin_icon.save("temp.png")
    skin_icons.append(display_icon(0,color))
    skin_icons[-1].init_id(idcounter,part_id,row,col,"icon")
    skin_icons[-1].add_gimg(pygame.image.load("temp.png"))
    idcounter += 1
    part_id += 1
    col += 1
    if col >= 4:
        row += 1
        col = 0

# randomly chooses a skin color which will be the initial skin color

skincolor = random.choice(skins) # chooses a random skin color
skincolor = skincolor[-1].color # default skin color

# creating sprites
blank_button = Image.open("blank_button.png")
sprites = []
items_display = []
button_icon = []
display_iterator = 1
directory = os.getcwd()
directory = os.path.join(directory, "bodysprite")
# for each folder in the bodysprite directory (these are body parts)
for a in sorted(os.listdir(directory)): # if a = arm then combine them??
    items_display.append([])
    if not a == ".DS_Store": # will appear but references to .ds_store are so that program can properly iterate through folders on mac computers
        temp_dir = os.path.join(directory, a) # body part
        sprites.append(body_part(a))
        icon_dir = os.path.join(directory, a,"icon.png")
        button_icon.append(Image.open(icon_dir))
        piccounter = 0
        # for each folder in the body parts directory (these are clothing items)
        for b in sorted(os.listdir(temp_dir)):
            if not b == ".DS_Store" and not b == "icon.png":
                temp_dir_2 = os.path.join(temp_dir, b)
                sprites[-1].items[b] = clothing_item(b)
                image_icon = blank_display.copy()
                items_display[-1].append(display_icon(len(items_display),b))
                # for each folder in the clothing items directory (these are each images which can be turned into sprites)
                for c in sorted(os.listdir(temp_dir_2)):
                    if not c == ".DS_Store":
                        filename = os.path.join(temp_dir_2, c)
                        cname = c.replace(".png",'')
                        sprites[-1].items[b].sprites[cname] = orientation(pygame.image.load(filename),Image.open(filename)) # loads the file
                        width, height = sprites[-1].items[b].sprites[cname].imgfile.size # gets the size of those files
                        sprites[-1].items[b].sprites[cname].gamefile = pygame.transform.scale(sprites[-1].items[b].sprites[cname].gamefile,(12*width,12*height)) # makes them larger to be displayed on screen
                        sprites[-1].items[b].sprites[cname].orientation(c[:-4]) # determines the orientation, stripping the filename extension
                        sprites[-1].items[b].sprites[cname].coord(a) # coords it based on the type of body part it is
                        if "f" in cname:
                            temp_img = sprites[-1].items[b].sprites[cname].imgfile
                            if a == "body":
                                temp_img = temp_img.resize((60, 60))
                                image_icon.paste(temp_img,(sprites[-1].items[b].sprites[cname].iconx+15,sprites[-1].items[b].sprites[cname].icony+15),mask=temp_img) # pastes it
                            else:
                                temp_img = temp_img.resize((80, 80))
                                image_icon.paste(temp_img,(sprites[-1].items[b].sprites[cname].iconx,sprites[-1].items[b].sprites[cname].icony),mask=temp_img)
                image_icon.save(f"temp{a}{piccounter}.png")
                image = f"temp{a}{piccounter}.png"
                # updates and loads the images into the display icons
                if a == "arm":
                    items_display[-1][-1].add_img(Image.open(filename))
                    items_display[-1][-1].add_gimg(pygame.image.load(filename))
                else:
                    items_display[-1][-1].add_img(Image.open(image))
                    items_display[-1][-1].add_gimg(pygame.image.load(image))
                piccounter += 1
    else:
        items_display.remove(items_display[-1])

display_iterator = 1
# iterates through arm objects to combin it with body
for a in range(len(items_display[1])):
    image_icon = Image.new('RGBA', (105, 105), (255, 0, 0, 0))
    # pastes right arm
    image_icon.paste(items_display[2][display_iterator-1].imgfile,(sprites[2].items[items_display[2][display_iterator-1].name].sprites['f'].iconx,sprites[2].items[items_display[1][display_iterator-1].name].sprites['f'].icony),mask=items_display[2][display_iterator-1].imgfile)
    temp_img = sprites[1].items[items_display[1][display_iterator-1].name].sprites['df'].imgfile
    temp_img = temp_img.resize((35, 35))
    # pastes left arm
    image_icon.paste(temp_img,(sprites[1].items[items_display[1][display_iterator-1].name].sprites['df'].iconx,sprites[1].items[items_display[1][display_iterator-1].name].sprites['df'].icony),mask=temp_img)
    temp_img = sprites[1].items[items_display[1][display_iterator-1].name].sprites['gf'].imgfile
    temp_img = temp_img.resize((35, 35))
    # pastes body
    image_icon.paste(temp_img,(sprites[1].items[items_display[1][display_iterator-1].name].sprites['gf'].iconx,sprites[1].items[items_display[1][display_iterator-1].name].sprites['gf'].icony),mask=temp_img)
    image_icon.save("temp.png")
    image = "temp.png"
    # imports combined images
    items_display[2][display_iterator-1].add_img(Image.open(image))
    items_display[2][display_iterator-1].add_gimg(pygame.image.load(image))
    display_iterator += 1
# removes the old arm objects because they are stored within the body objects now
items_display.remove(items_display[1])
body_sprites = sprites[1]
sprites.remove(sprites[1])
button_icon.remove(button_icon[1])

idcounter = 0
maxy = []
# goes through each body part to determine its coordinates and when to display it
for body_part in items_display:
    row = 0
    col = 0
    part_id = 0
    for item in body_part:
        item.init_id(idcounter,part_id,row,col,"icon") #part_id is its number relative to the body part, id_counter is total
        if body_part == items_display[1]:
            item.coord_adjust()
        idcounter += 1
        part_id += 1
        col += 1
        if col >= 4:
            row += 1
            col = 0
    maxy.append(int(item.y-800)) # this is the maximum y that is allowed to prevent the user from scrolling infinitely

# minuses the display number by one because skin (which is not determine through the items_display) is display #0
for dis in items_display:
    for stuff in dis:
        if not dis == items_display[0]:
            stuff.display_num -= 1
 
# assigns a random clothing object as the one the player will be wearing on start-up
clothing = []
for items in items_display:
    clothing.append(random.randint(0,len(body_part)-1))

# this creates a button for the skin put through this function
def skin_icon_creator(part_buttons,parts,button_icon,isskin):
    image_icon = blank_button.copy()
    image_icon.paste(button_icon[parts],(0,25),mask=button_icon[parts])
    image_icon.save("temp.png")
    if isskin == False:
        part_buttons.append(display_icon(0,sprites[parts-1].part))
    else:
        part_buttons.append(display_icon(0,"skin"))
    part_buttons[-1].add_gimg(pygame.image.load("temp.png"))
    part_buttons[-1].init_id(parts,parts,0,0,"button")
    return part_buttons

# iterates through stuff to paste skin icons
part_buttons = []
button_icon.insert(0,Image.open("skins_icon.png"))
skin_icon_creator(part_buttons,0,button_icon,True)
for parts in range(len(clothing)):
    for a in sorted(os.listdir(directory)):
        if not a == ".DS_Store":
            skin_icon_creator(part_buttons,parts+1,button_icon,False) # creates a button for the skin icons

buttonmaxy = int((len(clothing)-1)*100-800) # this is the maximum y that is allowed to prevent the user from scrolling infinitely

# Imports the images for the left arrow and right arrow buttons

left_arrow = pygame.image.load("left_arrow.png")
right_arrow = pygame.image.load("right_arrow.png")

# Adds the right display button

rightshowbutton = display_icon(None,None)
rightshowbutton.add_gimg(pygame.image.load("blank_button.png"))
rightshowbutton.init_id(None,None,None,None,"showright")

# Adds the left display button

leftshowbutton = display_icon(None,None)
leftshowbutton.add_gimg(pygame.image.load("blank_button.png"))
leftshowbutton.init_id(None,None,None,None,"showleft")

# Adds the export display button

exportbutton = display_icon(None,None)
exportbutton.add_gimg(pygame.image.load("blank_button.png"))
exportbutton.init_id(None,None,None,None,"export")

# intializes text

base_font = pygame.font.Font("memesans.ttf", 60)
system_font = pygame.font.Font("memesans.ttf", 40)
user_text = ''
writingactive = False # determines if user can write

modifiery = 0
camerax = 450 # initial camera position
camxchange = 450 # camera will move to this position
rightshow = True # screen will show right tab
leftshow = False # screen will show left tab

# function redraws the game window, mostly responsible for the blitting or putting it on screen

#def clothing():
    

def redrawGameWindow():
    global clothing, items_display, display, displayupdate, camerax, changex, system_display
    win.blit(bg,(0-camerax,0)) # displays background
    win.blit(left_menu,(0-camerax,100)) # displays higher left menu
    win.blit(left_menu,(0-camerax,500)) # displays lower left menu
    win.blit(display_bar,(0-camerax,0)) # displays the typing bar
    
    # TURN THIS INTO GETTING THE CLOTHES TURNING INTO IMAGE THEN BLITTING THAT IMAGE
    
    # iterates through skins and displays current skin
    for bodies in skins:
        for skin_sprites in bodies:
            if skincolor == bodies[0].sprites[0].name:
                if direction == 1 or direction == 3:
                    win.blit(bodies[0].sprites[0].gamefile, (50-camerax+450, 52)) # shows skin
                else:
                    win.blit(bodies[1].sprites[0].gamefile, (50-camerax+450, 52)) # shows arm
                    win.blit(bodies[2].sprites[0].gamefile, (50-camerax+450, 52))  # shows skin
    # iterates through clothes and display current clothes
    for item in reversed(range(len(clothing))):
        value = list(sprites[item].items)[clothing[item]]
        for a in sprites[item].items[value].sprites:
            if sprites[item].items[value].sprites[a].direction == direction:
                win.blit(sprites[item].items[value].sprites[a].gamefile,(sprites[item].items[value].sprites[a].gamex-camerax+450,sprites[item].items[value].sprites[a].gamey-modifiery))
    value = list(body_sprites.items)[clothing[1]]
    # iterates through sprites for body and displays them
    for b in body_sprites.items[value].sprites:
        if body_sprites.items[value].sprites[b].direction == direction:
            win.blit(body_sprites.items[value].sprites[b].gamefile,(body_sprites.items[value].sprites[b].gamex-camerax+450,body_sprites.items[value].sprites[b].gamey-modifiery))
    
    # UP TO HERE
    
    # if the screen should be displaying the skin icons, it should be displaying them
    if display == 0:
        for skin_icon in skin_icons:
            win.blit(skin_icon.gamefile,(skin_icon.x-camerax+450,skin_icon.y-wheel_y[1]))
    # displays the item icons for the current screen
    for image in items_display:
        for items in image:
            if items.display_num == display:
                win.blit(items.gamefile,(items.x-camerax+450,items.y-wheel_y[1]))
    # displays the buttons
    for buttons in part_buttons:
        win.blit((buttons.gamefile),(buttons.x-camerax+450,buttons.y-wheel_y[0]))
    # displays the button that shows the right menu
    win.blit(rightshowbutton.gamefile,(rightshowbutton.x-camerax+450,rightshowbutton.y))
    # displays the button that shows the left menu
    win.blit(leftshowbutton.gamefile,(leftshowbutton.x-camerax+450,leftshowbutton.y))
    # displays export button
    win.blit(exportbutton.gamefile,(exportbutton.x-camerax+450,exportbutton.y))
    # shows left and right arrows
    if leftshow == True: # displaying the arrows
        win.blit(left_arrow,(leftshowbutton.x-camerax+450,leftshowbutton.y))
    else:
        win.blit(right_arrow,(leftshowbutton.x-camerax+450,leftshowbutton.y))
    if rightshow == True:
        win.blit(left_arrow,(rightshowbutton.x-camerax+450,rightshowbutton.y))
    else:
        win.blit(right_arrow,(rightshowbutton.x-camerax+450,rightshowbutton.y))
    # if the camera should move to a different position, it moves to a different position
    if changex == True:
        if camerax <= camxchange:
            camerax += 5
        else:
            camerax -= 5
        if changedir == "left" and camerax <= camxchange:
            changex = False
        if changedir == "right" and camerax >= camxchange:
            changex = False
    # displays text
    text_surface = base_font.render(user_text, True, (0,0,0))
    win.blit(text_surface, (10-camerax, 15))
    # displays system updates
    if system_display == True:
        text_surface = system_font.render(system_message, True, (0,0,0))
        win.blit(text_surface, (system_mes_x-camerax, system_mes_y))
        system_display = False
    # updates the screen with all these changes
    pygame.display.update()

# exports character into sprites
def export_char():
    global skincolor, sprites
    typechecker = ['side','updown']
    spritemakerindex = {'side': 0,'updown': 1}
    spritemaker = [[[0,0],[5,1],[38,2],[36,3],[5,4],[6,5],[5,6],[36,7],[38,8],[2,9],[0,10]],[[0,0],[5,1],[38,2],[36,3],[5,4],[6,5],[5,6],[36,7],[38,8],[2,9],[0,10]],[[0,0],[5,1]]] # temp solution
    # side animation - 12,13,14,15,24,15,14,13
    # good ones - 0, 2, 4, 6,18,8,10,12,
    if user_text == "":
        if not os.path.exists(f'exported/new_char/side'):
            os.makedirs(f'exported/new_char/side')
        if not os.path.exists(f'exported/new_char/updown'):
            os.makedirs(f'exported/new_char/updown')
    else:
        if not os.path.exists(f'exported/{user_text}/side'):
            os.makedirs(f'exported/{user_text}/side')
        if not os.path.exists(f'exported/{user_text}/updown'):
            os.makedirs(f'exported/{user_text}/updown')
    new_sprite = []
    for orientation in range(4):
        for skin in skins: # goes for each skin type
            for spritez in skin:
                for animations in spritez.sprites:
                    for item in typechecker:
                        if skincolor == spritez.color and spritez.direction == item:
                            new_sprite.append(blank_template.copy())
                            if (orientation == 1 or orientation == 3) and item == "side":
                                new_sprite[-1].paste(animations.imgfile,(0,0),mask=animations.imgfile)
                            else:
                                new_sprite[-1].paste(animations.imgfile,(0,0),mask=animations.imgfile)
        for clothes in reversed(range(len(clothing))): # goes for each clothing
            value = list(sprites[clothes].items)[clothing[clothes]]
            legmover = 0
            direction = 1
            for a in sprites[clothes].items[value].sprites:
                for item in typechecker:
                    counter = 0
                    for spriteee in new_sprite: # goes through each of the sprites
                        if sprites[clothes].items[value].sprites[a].direction == orientation+1:
                            if (direction == 2 and clothes == 2) or (direction == 4 and clothes == 2) and item == "side":
                                spriteee.paste(sprites[clothes].items[value].sprites[a].imgfile,(sprites[clothes].items[value].sprites[a].x-legmover,sprites[clothes].items[value].sprites[a].y),mask=sprites[clothes].items[value].sprites[a].imgfile)
                                #if legmover == 3 or legmover == -3:
                                    #direction *= -1
                                    #if direction == 1: # moving positive
                                        #legmover += 1
                                    #else: # moving negative
                                        #legmover -= 1
                                #else:
                                    #if direction == 1: # moving positive
                                        #legmover += 1
                                    #else: # moving negative
                                        #legmover -= 1
                            else:
                                spriteee.paste(sprites[clothes].items[value].sprites[a].imgfile,(sprites[clothes].items[value].sprites[a].x+legmover,sprites[clothes].items[value].sprites[a].y),mask=sprites[clothes].items[value].sprites[a].imgfile)
                            nest_count = 0
                            #for nested_sprites in spritemaker:
                                #for count, itemic in enumerate(nested_sprites):
                            if user_text == "": # exports multiple animation versions of them
                                if nest_count == 0:
                                    spriteee.save(f"exported/new_char/updown/new_char{counter}.png") # itemic[1]
                                else:
                                    spriteee.save(f"exported/new_char/side/new_char{counter}.png")
                            else:
                                if nest_count == 0:
                                    spriteee.save(f"exported/{user_text}/updown/{user_text}{counter}.png")
                                else:
                                    spriteee.save(f"exported/{user_text}/side/{user_text}{counter}.png")
                                nest_count = 1
                        counter += 1
direction = 1

bg = pygame.image.load('bg.jpg') # loads background
left_menu = pygame.image.load('left_menu.png') # loads left menu
input_rect = pygame.image.load('display_bar_use.png') # loads display bar while using
input_rect_alt = pygame.image.load('display_bar_unuse.png') # loads display bar while not using
display = 0
wheel_y = [0,0]
displayupdate = []
changex = False
changedir = ""
text = ""
system_message = ""
system_display = False
system_mes_x = 0
system_mes_y = 0
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60) # fps
    
    for event in pygame.event.get(): # gets events on keyboard
        if event.type == pygame.QUIT: # quits program
            run = False
        if event.type == pygame.KEYDOWN and writingactive == True: # if user wants to write, it writes that
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
            
    keys = pygame.key.get_pressed() # gets keys pressed
    
    # changes orientation of character
    if keys[pygame.K_UP]:
        direction = 3
    if keys[pygame.K_DOWN]:
        direction = 1
    if keys[pygame.K_LEFT]:
        direction = 2
    if keys[pygame.K_RIGHT]:
        direction = 4
    
    # if the mouse is pressed
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if display == 0:
            # checks to see if skin was changed
            for skin in skin_icons:
                skin_rect = skin.gamefile.get_rect(topleft=(skin.x-camerax+450, skin.y))
                if skin_rect.collidepoint(x,y):
                    skincolor = skin.name # changes skin to skin clicked
        else:
            # checks to see if any clothing was changed
            for items in items_display[display-1]:
                item_rect = items.gamefile.get_rect(topleft=(items.x-camerax+450,items.y))
                if item_rect.collidepoint(x,y):
                    clothing[display-1] = items.part_id # changes clothing to clothing clicked
        for buttons in part_buttons:
            # checks to see if a button was clicked and user wants to change to another menu
            button_rect = buttons.gamefile.get_rect(topleft=(buttons.x-camerax+450,buttons.y))
            if button_rect.collidepoint(x,y):
                display = buttons.part_id # changes menu to menu desired
        # if the right button was clicked, it opens or closes right menu
        right_clicked = rightshowbutton.gamefile.get_rect(topleft=(rightshowbutton.x-camerax+450,rightshowbutton.y))
        if right_clicked.collidepoint(x,y):
            if rightshow == False:
                rightshow = True
                leftshow = False
                changex = True
                changedir = "right"
                camxchange = 450
            else:
                rightshow = False
                leftshow = True
                changex = True
                changedir = "left"
                camxchange = 0
            time.sleep(0.1) # prevents spam
        # if the left button was clicked, it opens or closes left menu
        left_clicked = leftshowbutton.gamefile.get_rect(topleft=(leftshowbutton.x-camerax+450,leftshowbutton.y))
        if left_clicked.collidepoint(x,y):
            if leftshow == False:
                leftshow = True
                rightshow = False
                changex = True
                changedir = "left"
                camxchange = 0
            else:
                leftshow = False
                rightshow = True
                changex = True
                changedir = "right"
                camxchange = 450
            time.sleep(0.1) # prevents spam
        # if the export button as clicked, exports sprite
        export_clicked = exportbutton.gamefile.get_rect(topleft=(exportbutton.x-camerax+450,exportbutton.y))
        if export_clicked.collidepoint(x,y):
            export_char()
            system_message = "Exported!"
            system_mes_x = 675
            system_mes_y = 500
            system_display = True
        # if the writing box is clicked, allows writing or stops writing
        input_collision = input_rect.get_rect(topleft=(0-camerax,0))
        if input_collision.collidepoint(event.pos):
            writingactive = True
        else:
            writingactive = False
    
    # changes display bar sprite dependant on whether writing is allowed or not
    if writingactive:
        display_bar = input_rect
    else:
        display_bar = input_rect_alt
    
    # if the mouse wheel is moved
    if event.type == pygame.MOUSEWHEEL:
        x, y = pygame.mouse.get_pos()
        # moves right menu
        if x >= 500:
            if maxy[display] > 0:
                wheel_check(1)
        # moves button
        elif x >= 450:
             if maxy[display] > 0:
                wheel_check(0)
        else:
            pass

    # redraws game window
    redrawGameWindow()

# quits pygame
pygame.quit()
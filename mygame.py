import sys,pygame
import math
from random import randint

TILESIZE = 32
WIDTH = 640
HEIGHT = 480
WALL_WIDTH = 10
TILE_START = 5
TILE_STOP = 15
GRID_COLS = TILE_STOP - TILE_START
GRID_ROWS = 13

green = (0,255,0)
lightgrey = (224,224,224)
red = (255,0,0)
blue = (0,0,255)
cyan = (0,255,255)
yellow = (255,255,0)

class tile_property:
    def __init__(self, tileid, colour, x = -1, y = -1):
        self.ID = tileid
        self.color = colour
        self.x = x
        self.y = y
        
    def getColour(self):
        return self.color
    
    def getID(self):
        return self.ID
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

class GridManager:
   
    def __init__(self):
        # Creates a list containing 5 lists, each of 8 items, all set to 0
        w, h = GRID_COLS, GRID_ROWS;
        self.grid_map = [[tile_property(0,0) for x in range(w)] for y in range(h)]
        self.connectID_list = [] 
        
                
    def updateMap(self, col, row, tile_property):
        print("col_mgr: " + str(col))
        print("row_mgr: " + str(row))
        if col == 11:
            col -= 2
        self.grid_map[row-1][col-1] = tile_property
#         print("grid_property: " + str(self.grid_map[col-1][row]))
        GridManager.findConnectedBlocks(self,row-1, col-1)

    def findConnectedBlocks(self, x, y):
        tl = tile_property(-1,-1)
        tm = tile_property(-1,-1)
        tr = tile_property(-1,-1)
        ml = tile_property(-1,-1)
        mr = tile_property(-1,-1)
        bl = tile_property(-1,-1)
        bm = tile_property(-1,-1)
        br = tile_property(-1,-1)
        
        if x > 0 and y > 0 :
            tl = tile_property(self.grid_map[x-1][y-1].getID(),self.grid_map[x-1][y-1].getColour())
        if y > 0 :
            ml = tile_property(self.grid_map[x][y-1].getID(),self.grid_map[x][y-1].getColour())
            if x < GRID_ROWS:
                bl = tile_property(self.grid_map[x+1][y-1].getID(), self.grid_map[x+1][y-1].getColour())
        if x > 0 :
            tm = tile_property(self.grid_map[x-1][y].getID(), self.grid_map[x-1][y].getColour())
            if y < GRID_COLS -1:
                tr = tile_property(self.grid_map[x-1][y+1].getID(), self.grid_map[x-1][y+1].getColour())
        
        if x < GRID_ROWS -1:
            bm = tile_property(self.grid_map[x+1][y].getID(), self.grid_map[x+1][y].getColour())
        
        if y < GRID_COLS-1:
            mr = tile_property(self.grid_map[x][y+1].getID(), self.grid_map[x][y+1].getColour())
        
        if x < GRID_ROWS-1 and y < GRID_COLS-1:
            br = tile_property(self.grid_map[x+1][y+1].getID(), self.grid_map[x+1][y+1].getColour()) 
        
        bList = [tl,tm,tr,ml,mr,bl,bm,br]
        bList_name = ["tl","tm","tr","ml","mr","bl","bm","br"]
        print("This block value: " + str(self.grid_map[x][y].getColour()))
        
        curColor = self.grid_map[x][y].getColour()
        curID = self.grid_map[x][y].getID()
        j = 0
        ConnectedBlockFound = False
#         clist_ans = []
        self.connectID_list = []
        for i in bList:
            if i.getColour() > 0:
                print( bList_name[j] + "--> colour:" + \
                       GridManager.colorIntTostr(self,i.getColour()) \
                       + " ID: " + str(i.getID()))
                if curColor == i.getColour():
                    print ("same colour!")
                    self.connectID_list.append(i.getID())
#                     clist_ans.append(i.getID())
                    ConnectedBlockFound = True
                
            j+=1
          
        if ConnectedBlockFound and len(self.connectID_list) > 0 :
#             clist_ans.append(curID)
            self.connectID_list.append(curID)
            
#         return self.connectID_list
            
    def getConnectedList(self):
        return self.connectID_list 
    
    def printMap(self):
#         print(str(self.grid_map[6]))
#         for x in range(0,GRID_COLS):
#             print(str(self.grid_map[x]) ,",", end="")
        
        for x in range(0,GRID_ROWS):
            for y in range(0,GRID_COLS):
                print( "(" + str(self.grid_map[x][y].getID()) + " - " + str(self.grid_map[x][y].getColour()) + ")",",", end="")
            print("")
#                 if (x * y % 10) == 0:
#                     print("")
    
    def colorIntTostr(self,color_property):
        if color_property ==1:
            return "red"
        elif color_property == 2:
            return "blue" 
        elif color_property == 3:
            return "yellow"
        elif color_property == 4:
            return "cyan"

class GridBuilder:
    offset = 32
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def drawGrid(self):
        for x in range(TILESIZE*5, WIDTH - (TILESIZE*4), TILESIZE):
            pygame.draw.line(self.screen, lightgrey, (x, TILESIZE), (x,HEIGHT - TILESIZE))
        for y in range(TILESIZE * 1, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, lightgrey, (TILESIZE*5,y), (WIDTH - (TILESIZE*5) ,y))

class LineBuilder:
    def __init__(self, screen):
        self.screen = screen
        
    def drawLine(self, x1, y1, x2, y2):
        pygame.draw.line(self.screen, green, (x1,y1), (x2,y2), 5)

def drawline(x1, y1, x2, y2, screen):
    pygame.draw.line(screen, green, (x1,y1), (x2,y2), 5)
    

class directedLineBuilder(pygame.sprite.Sprite):
    objID = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        colorList = (red, blue, cyan, yellow)
        self.colour = colorList[randint(0,3)]
        self.image.fill(self.colour)
        self.xpos = TILESIZE*10 + 16
        self.ypos = 440
        self.angle = 210;
        self.rect.center = (self.xpos, self.ypos)
        self.enabled = False
        self.connectivity = 0;
        self.ID = directedLineBuilder.objID
        directedLineBuilder.objID +=1
        
        
    def update(self):
        if not self.enabled:
            return
        delta_val = 10.0
        dy = delta_val * math.cos(math.radians(self.angle))
        dx = delta_val * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.y < 10:
            self.rect.center = (640/2, 440)
            self.enabled = False
            
    def getColour(self):
        return self.colour
    
    def getColorStr(self):
        colorDict = { red : "red",
                      yellow : "yellow",
                      cyan : "cyan",
                      blue :  "blue"}
        
        return colorDict[self.colour]
        
    
    
    def getObjID(self):
        return self.ID
        

class wallBuilder(pygame.sprite.Sprite):
    def __init__(self, distfromLeft, wallImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WALL_WIDTH,1000))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = (distfromLeft, 480/2)
#         self.image = pygame.transform.scale(wallImg, (50,50))
#         self.rect = self.image.get_rect()

class roofBuilder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((350, WALL_WIDTH + 5))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center = (320, TILESIZE - WALL_WIDTH)
        
class roofPartsBuilder(pygame.sprite.Sprite):
    roofPartID = 1
    def __init__(self, blockCol):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE * 1, TILESIZE/2))
        red = (255,0,0)
        blue = (0,0,255)
        cyan = (0,255,255)
        yellow = (255,255,0)
        
        colorList = (red, blue, cyan, yellow)
        self.image.fill(colorList[roofPartsBuilder.roofPartID%4])
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE * blockCol 
        self.rect.y = TILESIZE*1  - TILESIZE/2
        self.id = roofPartsBuilder.roofPartID
        roofPartsBuilder.roofPartID += 1
        
    
class bottleBuilder(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bottle.png").convert()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.65), int(self.size[1]* 0.65)))
        self.rect = self.image.get_rect()
        self.rect.center = ( TILESIZE*10 + 16, 430)
        self.angle = 0
        self.orig_image = self.image
        self.direction = "x"
        self.maxLeft = False
        self.maxRight = False 
    
    def stopRotation(self):
        self.direction = "x"
        
    def rotateRight(self):
        self.direction = "l"
        
    def rotateLeft(self):
        self.direction = "r"

    def update(self):
        if self.direction == 'l' and not self.maxLeft:
            self.angle -= 5
            print ("current angle : " + str(self.angle)) 
        elif self.direction == 'r' and not self.maxRight:
            self.angle += 5
            print ("current angle : " + str(self.angle))
        else:
            self.angle += 0

        if self.angle > 80:
            self.maxRight = True
            self.maxLeft = False
        elif self.angle < -80:
            self.maxLeft = True
            self.maxRight = False
        else:
            self.maxLeft = False
            self.maxRight = False
            
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)        
    

connectedBlocks = []
def restructureConnectedList(connectList):
    result = []
#     for rlist in connectList:
    print ("element ")
    print (connectList)
    
    print("block")
    print(connectedBlocks)
    
    connectedBlocks.append(connectList)
    
    

#     if len(connectedBlocks) > 0:
#         for i in connectedBlocks[0:-1]:
#             if i[-1] == connectedBlocks[-1][0]:
#                 connectedBlocks.append(i + connectedBlocks[-1][1:])
#         for x in connectedBlocks:
#             for y in connectedBlocks[1:-1]:
#                 if len(x) <= len(y) and x.issubset(y):
#                     connectedBlocks.remove(x) 
                        
    
#     for r in len(connectList):
#         for s in connectedBlocks
    
#     connectedBlocks = []
    
#     if len(connectList) == 1:
#         connectedBlocks.append(connectList)
#     
#     for r in connectList[0:-1]:
#         if r[-1] == connectList[-1][0]:
#             print("add")
#             result.append(r + connectList[-1][1:])
#             connectedBlocks.append(r + connectList[-1][1:])
#         else:
#             connectedBlocks.append(r)
#     for s in connectedBlocks:
#         if s[-1] == connectList[-1][0]:
#             result.append(s + connectList[-1][1:])
#     for rnodes in connectList:
#         
#         if rnodes[-1] == curNode[0]:
#             result.append(rnodes + curNode[1:])
#         elif rnodes[0] == curNode[0]:
#             result.append(rnodes[1:] + curNode[1:])
#         else:
#             if curNode[0] == rnodes[0] and rnodes[1] == curNode[1]:
#                 continue
#             result.append(rnodes)
#     
#     print("====")
#     print(connectedBlocks)
#     print("====")
       
def main():
    pygame.init()
    size = 640, 480
    
    screen = pygame.display.set_mode(size)
    
    l1 = LineBuilder(screen);
    
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    
    rightWall_sprite = pygame.sprite.Group()
    leftWall_sprite = pygame.sprite.Group()
    
    roof_sprite = pygame.sprite.Group()
    
    newBalls_sprite = pygame.sprite.Group()
    
    roof_parts_sprite = pygame.sprite.Group()
    
    b1 = bottleBuilder();
    
    main_ball = directedLineBuilder();
    
    gridMgr = GridManager();
    
    wallImg = pygame.image.load("handpaintedwall2.png").convert()

    roofWall = roofBuilder()
    leftWall = wallBuilder(TILESIZE*5 - WALL_WIDTH ,wallImg)
    rightWall = wallBuilder(TILESIZE*15 + WALL_WIDTH ,wallImg)
    rightWall_sprite.add(rightWall);
    leftWall_sprite.add(leftWall);
    roof_sprite.add(roofWall)
    all_sprites.add(b1)
    all_sprites.add(leftWall)
    all_sprites.add(rightWall)
    all_sprites.add(roofWall)
    all_sprites.add(main_ball)
    
    list_of_old_balls= []
    old_ball_sprite = pygame.sprite.Group()

    roofpart_list = []
    
    for i in range(TILE_START,TILE_STOP):
        roofpart_list.append(roofPartsBuilder(i))
        
    for i in roofpart_list:        
        roof_parts_sprite.add(i)
    
    grid =  GridBuilder()
    
    list_of_connections = []
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    b1.rotateLeft()
                elif event.key == pygame.K_RIGHT:
                    b1.rotateRight()
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    if not main_ball.enabled:
                        main_ball.angle = b1.angle + 180;
                        main_ball.enabled = True
                
            if event.type == pygame.KEYUP:
                b1.stopRotation()
                #main_ball.angle = b1.angle + 180;
#                 if event.key == pygame.K_SPACE:
#                     main_ball.enabled = False

        
        all_sprites.update()
        screen.fill([0,0,0])
        grid.drawGrid()
        all_sprites.draw(screen)
        roof_parts_sprite.draw(screen)
        
        ball_hit_list = pygame.sprite.spritecollide(main_ball, rightWall_sprite, False)
        ball_hit_list_2 = pygame.sprite.spritecollide(main_ball, leftWall_sprite, False)
        ball_hit_roof = pygame.sprite.spritecollide(main_ball, roof_sprite, False)
        
        for b in ball_hit_list: 
            print (b)
#             all_sprites.remove(main_ball)
            main_ball.angle = -main_ball.angle 
#             all_sprites.add(main_ball)
        
        
        for b in ball_hit_list_2: 
            print ("ball angle: " + str(main_ball.angle))
            print ("bottle angle: " + str(b1.angle))
            
            main_ball.angle =  -main_ball.angle
            if main_ball.angle > 45 and main_ball.angle < 90:
                main_ball.angle = main_ball + 180
            elif main_ball.angle > 200:
                main_ball.angle = -main_ball.angle
                
        if ball_hit_roof:
            main_ball.enabled = False
            print( "main ball x: " + str(main_ball.rect.x))
            print( "main ball y: " + str(main_ball.rect.y))
            tileRow = int(main_ball.rect.x/TILESIZE) 
            tileCol = int(main_ball.rect.y/TILESIZE)
            
            print("TILE col: " +  str(int(main_ball.rect.x/TILESIZE) - TILE_START))
            print("TILE row: " +  str(int(main_ball.rect.y/TILESIZE)))
            print ("corrected x  : " + str(tileCol*TILESIZE))
            print ("corrected y  : " + str( (tileRow+1)*TILESIZE))
            main_ball.rect.x = (tileRow)*TILESIZE
                
            main_ball.rect.y = (tileCol+1)*TILESIZE
            color_property = 0
            if main_ball.getColour() == red:
                color_property = 1;
            elif main_ball.getColour() == blue:
                color_property = 2;
            elif main_ball.getColour() == yellow:
                color_property = 3;
            elif main_ball.getColour() == cyan:
                color_property = 4;

            
            gridMgr.updateMap(tileRow+1 - TILE_START , tileCol+1,  tile_property(main_ball.getObjID(),color_property))
            
            if len(gridMgr.getConnectedList()) > 0:
                resultL = gridMgr.getConnectedList()
                list_of_connections.append(resultL)
                print("list of connects")
                print(list_of_connections)                
            
#                 restructureConnectedList(resultL)

            gridMgr.printMap()
            
            
            
            if type(ball_hit_roof[0]).__name__ == "directedLineBuilder":
                if main_ball.colour == ball_hit_roof[0].getColour():
                    print ("both have same colour")
                    print ("objID main_ball: " + str(main_ball.getObjID()))
                    print ("objID collided with: " + str(ball_hit_roof[0].getObjID()))
            
            roof_sprite.add(main_ball)
            list_of_old_balls.append(main_ball)
            old_ball_sprite.add(main_ball)
            main_ball = directedLineBuilder();
            all_sprites.add(main_ball)
            
            print(list_of_connections)
            if len(list_of_connections) > 0 :
                for x in list_of_connections:
                    for y in list_of_connections[1:]:
                        if len(x) == 2 and len(y) == 2:
                            if x[-1] == y[0] or x[0] == y[1]:
                                print("found group: ")
                                print(x)
                                print(y)
                                list_of_connections.remove(x)
                                list_of_connections.remove(y)
                                for q in all_sprites:
                                    if type(q).__name__ == "directedLineBuilder":
                                        if q.getObjID() == x[0] or q.getObjID() == x[1] or q.getObjID() == y[1]:
                                            print(" deleting spirit!!")
                                            all_sprites.remove(q)
                                            roof_sprite.remove(q)
                                            if x in list_of_connections:
                                                list_of_connections.remove(x)
                    
                        
                for x in list_of_connections:
                    if len(x) > 2:
                        print("found")
                        print(x)
                        for t in x:
                            print ("t: " + str(t))
                            for q in all_sprites:
                                if type(q).__name__ == "directedLineBuilder":
                                    if  q.getObjID() == t:
                                        print(" deleting spirit!!!")    
                                        all_sprites.remove(q)
                                        roof_sprite.remove(q)
                        list_of_connections.remove(x)
                        print("del list")
                        print(list_of_connections)    
#             for i in all_sprites:
#                 if type(i).__name__ == "directedLineBuilder":
#                     print ("ID:" + str(i.getObjID()))
#                     print ("color:" + i.getColorStr())

        
        pygame.display.flip() 
        clock.tick(30)
    
if __name__ == '__main__':
    main()
    
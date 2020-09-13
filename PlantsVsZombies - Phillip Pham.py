#FSE Game - Plants vs Zombies - Phillip Pham (Period 9) - Grade 11

#IMPORTANT COMMENTS
#this goal of this game is to plant a variety of plants on the field to defend your house from the incoming zombies; you purchase plants
#using sun currency which you get from planting sunflowers or from it falling from the sky due to a timer; game is played with a mouse only; waves of zombies will be spawned
#with a timer and you have to use diff plants to try to defeat them. the goal of this game is to try to survive for as many waves as possible;
#all the main functions to fun the game are mostly called from the drawScene function; we animate the sprites of the zombies and plants and
#update the position of the zombies and bullets every frame, as well as check if user is placing or selecting a plant, if user right clicks
#to stop selecting or shovelling the plant, if bullet is hitting a zombie,if zombie is eating a plant and to reduce the plant's health if is is, if zombie is
#colliding with a lawnmower and if a lawnmower is moving across the screen, if player is currently losing, and we over all draw the entire scene using the drawScene
#function. we use other functions in the while running loop of the game as well, such as checking if user clicked on a sun.the game runs on a main while loop that
#contains many other while running loops, and the currentScreen of the game determines which while loop to run what aspect of the game (menu, help, main game screen).
#user can change to different screens though clicking buttons on the menu or losing in the main game.

#IMPORT LIBRARIES
from pygame import *
from random import *
from math import *


#FUNCTIONS

#FUNCTION TO HANDLE LOGIC AND DRAW SCENE EVERY FRAME
def drawScene(zombiesList, plantsActionList, bulletsList, plantsRechargeList, shovellingPlant, selectingPlant, sunAmount, plant, currentScreen, loseX):
    if currentScreen != "lose": #if the player is not losing
        screen.fill((0, 0, 0)) #clears screen with black
        
        screen.blit(back, (0, 0)) #blits background image
        
        blitLawnMower(lawnMowerPic, lawnMowerList) #function to blit remaining lawnmowers on screen

        if len(lawnMowerList) > 0: #if there are lawnmowers left, we check if a zombie collided with them
            checkLawnMower(zombiesList, lawnMowerList, runningMowerList)
            
        if len(runningMowerList) > 0: #if there are lawnmowers currently moving across screen, we run this function
            moveLawnMover(zombiesList, runningMowerList, length)
        
        plantAnimation(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, mineCheckList, plantsActionList, zombiesList, width, length) #animates plant sprites

        returnList = zombieAnimation(currentScreen, zombiesList, normalZombieList, normalZombieEat, zombieObjectList, plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, x, y, width, length)
        #function to animate zombies and move them across screen; also allows zombies to eat plants and check if player lost game
        zombiesList = returnList[0]
        currentScreen = returnList[1]
        
        if currentScreen == "lose": #if the player did lose the game (check the currentScreen var returned from zombieAnimation)
            #we have to stop the bg music and timers
            mixer.music.stop()
            zombieSpawnTimer = time.set_timer(ZOMBIEEVENT, 0)
            sunTimer = time.set_timer(SUNEVENT, 0)
            
        
        returnList = plantAction(plantsNameGrid, sunEnergyList, mineCheckList, plantsActionList, plantsActionTimesList, bulletsList, width, length)
        #function to perform plant action and check the timers for each plant on lawn
        
        plantsActionList = returnList[0]
        bulletsList = returnList[1]

        returnList = checkBullets(bulletsList, zombiesList) #function to check if bullets hit zombie
        bulletsList = returnList[0]
        zombiesList = returnList[1]
        
        sunAnimation(sunEnergyList, sunSpriteList, length) #function for sun sprite animation
        
        plantsRechargeList = plantRecharge(plantsRechargeList, plantsRechargeTimesList, selectedPlants) #function to recharge plants if they are used

        selectPlantBar(selectBar, selectedPlants, plantsRechargeList, plantsRechargeTimesList, sunAmount, sunAmountFont) #function to blit plant select ui on screen

        screen.blit(shovelPic, (shovelRect[0], shovelRect[1])) #blits shovel button on screen

        if shovellingPlant == True: #if user is currently shovelling a plant, we blit a shovel cursor and run the shovellingPlant function
            screen.blit(shovelCursor, (mx - shovelCursor.get_width() // 2, my - shovelCursor.get_height() // 2))
            shovellingPlant = shovelTool(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, shovellingPlant, x, y, width, length)

        if selectingPlant == True and plant != "" and shovellingPlant == False:
            #if user is currently selecting plant and is not shovelling plant
            pic = eval(plant + "List")[0] #get the respective plant sprite list and get the first image to use as a cursor when selecting plant 
            returnList = placePlant(plant, pic, sunAmount, plantsCostList, plantsNameGrid, plantsHealthGrid, plantsHealthList, plantsSpriteGrid, plantsActionList, plantsRechargeList, selectedPlants, selectingPlant, 50, 100, width, length)
            selectingPlant = returnList[0]
            plantsRechargeList = returnList[1]
            plantsActionList = returnList[2]
            sunAmount = returnList[3]
            #run function to place plant
            screen.blit(pic, (mx - pic.get_width() // 2, my - pic.get_height() // 2)) #blits cursor pic at mouse position
        else:
            plant = "" #if user is not selecting plant, we have to set the current plant var to empty string

        #displays the current wave amount on screen at  bottom right hand corner
        displayWaveAmount = sunAmountFont.render("Wave: " + str(waveCount), True, (0, 0, 0))
        screen.blit(displayWaveAmount, (1050, 750))

    elif currentScreen == "lose": #if the player is currently losing
        screen.fill((0, 0, 0))

        #we have to side scroll the background to the left so that we can see the house in the left of the background
        if loseX < 280: #if the loseX (x coor to subtract from x coor of background to move it to the left)
            loseX += 2 #increase the counter var
            screen.blit(back1.subsurface([290 - loseX, 0, 1200, 800]), (0, 0)) #blit the new section of background
        else: #if the loseX is already high enough that we can see the house, we have to end the game by changing the currentScreen to "lost"
            currentScreen = "lost"
            screamSound.play()

        returnList = zombieAnimation(currentScreen, zombiesList, normalZombieList, normalZombieEat, zombieObjectList, plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, x, y, width, length)
        zombiesList = returnList[0] #we also have to animate a zombie so that it moves towards the house while we are side scrolling
	
    display.flip() #updates screen
    
    return [zombiesList, plantsActionList, bulletsList, plantsRechargeList, shovellingPlant, selectingPlant, sunAmount, plant, currentScreen, loseX]
    # returns necessary variables to main game

    

#MISCELLANEOUS FUNCTIONS
def inList(item, twoDList):
    #function takes an item (usually 1-d list) and a 2-d list; if the item is in the 2-d list,
    #we return the index of the item in 2-d list
    for oneDList in twoDList:
        if item in oneDList:
            return twoDList.index(oneDList)
    return -1

def addSprites(folder, subfolder, group, name, start, end):
    #function to add and return group of sprites in one folder; i named all the sprites the same name in the same category
    #and added a number at the end starting from 1 and increasing by 1 for each new sprite in same category
    sprites = []
    if group == "nut" and name == "nut":
    #if the folder has sprites for nut plant, we have to use different path for file name since the use different sprites
    #depending on the nut's current health
        for i in range(end): #loops until we reach the end number
             sprites.append(image.load("%s/%s/%s/%s%i-%i.png" % (folder, subfolder, group, name, start, i + 1)).convert_alpha())
             #find file path of each sprite using parameters and append each seperate sprite 
    else:  
        for i in range(start, end + 1):
            sprites.append(image.load("%s/%s/%s/%s%i.png" % (folder, subfolder, group, name, i)).convert_alpha())
            #same logic as above for any other sprites in the game
    return sprites

def createGrid(cols, rows):
    #creates 2d-list to use to hold data about plant properties depending on their location
    #on the 9x5 lawn
    return [["" for a in range(cols)] for b in range(rows)]

def blit_alpha(target, source, location, opacity):
    #function found online at http://www.nerdparadise.com/programming/pygameblitopacity
    #takes an image and blits it on screen at a transparency that allows you to see
    #the surface behind the image; does this by blitting pic on another surface, setting alpha
    #on that surface, and blitting the surface on screen
    x = location[0]
    y = location[1]
    temp = Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)



        

#UI RELATED FUNCTIONS
def selectPlantBar(selectBar, selectedPlants,  plantsRechargeList, plantsRechargeTimesList, sunAmount, font):
    #function to blit the whole ui to allow user to select plants using bar on top of screen
    screen.blit(selectBar, (100, 0)) #blits empty bar
    for ind in range(len(selectedPlants)): #goes through each element in selected plants list
        alphaPacket = False #boolean used to check if we should use an alpha image if the plant is currentyl recharging
        listIndex = inList(selectedPlants[ind], plantsRechargeList) #get index of the 1-d list that contains the selected plant in the plantsRechargeList,
                                                                    #which contains info if the plant is currently recharging
        if listIndex != -1: #if the recharge list contains the plant
            alphaPacket = True #we set the boolean to true to indicate we should blit the alpha image
            currentPlant = plantsRechargeList[listIndex][0] #get the current plant name
            currentRechargeTime = time.get_ticks() - plantsRechargeList[listIndex][1] #get the recharge time by subtracting current time from time in that list
                
        pic = eval(selectedPlants[ind] + "Packet") #gets picture of the seed packet of respective plant
        pic = pic.copy()
        
        if alphaPacket == True: #if plant is recharging 
            picAlpha = pic.convert()
            picAlpha.set_alpha(50) #sets seed packet transparent
            screen.blit(picAlpha, (200 + 75 * ind, 10)) #blits the transparent packet on ui bar, using index value in selectedPlants list to figure out position on screen

            listIndex = inList(currentPlant, plantsRechargeTimesList)  
            rechargeTime = plantsRechargeTimesList[listIndex][1] #gets the normal recharge time (not current rechange time, just data telling how much
            #miliseconds should a plant recharge) of the plant 

            packetLength = int(currentRechargeTime / rechargeTime * 90) #gets the length of how much we should blit non-transparent packet
            #on screen to indicate how much plant recharged already by getting the ratio of current recharge time over data recharge time and multiplying it by
            #90 (seed packet length)
            picNormal = pic.subsurface([0, 0, 65, packetLength]) 
            screen.blit(picNormal, (200 + 75 * ind, 10)) #blits subsurface of normal seed packet at that position overtop alpha seed packet
        
        elif alphaPacket == False: #otherwise just blits seed packet normally
            screen.blit(pic, (200 + 75 * ind, 10))
    displaySunAmount = sunAmountFont.render(str(sunAmount), True, (0, 0, 0)) #renders current num value for sun amount 
    screen.blit(displaySunAmount, (120, 80)) #blits current sun amount on ui bar

def shovelTool(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, shovellingPlant, x, y, width, length):
    #function to shovel plant on screen if user is currently shovelling plant
    
    oneSpot = 0 #var used to check how many squares of the lawn the user is currently hovering over
                #(used so that user can only select one square at a time because user can sometimes
                # select 2 squares if they are hovering between them)

    #loops through each individual lawn square
    for row in range(len(plantsNameGrid)):
        for col in range(len(plantsNameGrid[row])):
            square = Rect([x + col * width, y + row * length, width, length])
            #gets rect of that lawn square

            #checks if mouse cursor is hovering over it and if only one square is selected
            if square.x < mx < (square.x + length) and square.y < my < (square.y + length) and oneSpot != 1:
                square = Rect([x + col * width, y + row * length, width, length]) #get rect of that square again since it is only selected square
                oneSpot = 1 #change oneSpot so that we know a square is already selected
                if mb[0] == 1 and plantsNameGrid[row][col] != "": #if user left clicks and there is currently a plant at the square 
                    shovelPlantSound.play() #plays sound effect
                    removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, row, col) #removes plant    
                    shovellingPlant = False #change shovellingPlant to false so user stops shovelling plant
                
            else:
                square = Rect([x + col * width, y + row * length, width, length])
                oneSpot = 0 #otherwise we change oneSpot back to 0 if user is not hovering over it 
                
    if mb[2] == 1: #if user right clicks, change shovellingPlant to false so user stops shovelling plant
        shovellingPlant = False
                    
    return shovellingPlant #returns current state of shovellingPlant boolean


                                
            


#LAWN MOWER RELATED FUNCTIONS
def blitLawnMower(picture, rowsList):
    #blits lawnmower picture on screen using their x and y coors
    #rowsList contains list of [x, y, rowIndex] 
    for row in rowsList:
        screen.blit(picture, (row[0], row[1]))        

def checkLawnMower(zombiesList, lawnMowerList, runningMowerList):
    #function to check if lawnmower collides with a zombie
    #loops through each lawn mower
    for mower in lawnMowerList:
        #loops through each zombie
        for zombie in zombiesList:
            if mower[2] == zombie[6]: #checks if mower and zombie are in same row
                if Rect(mower[0], mower[1], 90, 60).colliderect(zombie[1], zombie[2], 90, 100):
                    #if the mower sprite collides with the zombie sprite
                    #we check if the mower is in the lawnMowerList
                    if [mower[0], mower[1], mower[2]] in lawnMowerList:
                        runningMowerList.append([mower[0], mower[1], mower[2]]) #append x and y coor and rowIndex of lawnmower to runningMowerList
                        lawnMowerList.remove([mower[0], mower[1], mower[2]]) #remove lawnmower from lawnMowerList
                        lawnMowerSound.play() 
    
def moveLawnMover(zombiesList, runningMowerList, length):
    #function to move each lawn mower currently in runningMowerList across screen
    #loops through each lawn mover moving
    #[x, y, rowIndex]
    for movingMower in runningMowerList:
        movingMower[0] += 5 #increase its x coor by 5
        screen.blit(lawnMowerPic, (movingMower[0], movingMower[1])) #blits picture of mower
        for zombie in zombiesList:
            #loopes through each zombie
            if movingMower[2] == zombie[6]: #checks if mower and zombie are in same row
                if Rect(movingMower[0], movingMower[1], 90, 60).colliderect(zombie[1], zombie[2], 90, 100):
                    #checks if mower collides with zombie; if it does, remove zombie
                    zombiesList.remove([zombie[0], zombie[1], zombie[2], zombie[3], zombie[4], zombie[5], zombie[6], zombie[7], zombie[8]])
                    zombieDeathSound.play()
        if movingMower[0] > screenWidth:
            #if mower is at the end of the screen, remove the mower
            runningMowerList.remove([movingMower[0], movingMower[1], movingMower[2]])
            



    
#PLANT RELATED FUNCTIONS
def placePlant(plant, pic, sunAmount, plantsCostList, plantsNameGrid, plantsHealthGrid, plantsHealthList, plantSpriteGrid, plantsActionList, plantsRechargeList, selectedPlants, selectingPlant, x, y, width, length):
    #function to place plant on lawn if user is currently selecting a plant
    oneSpot = 0 #var used to check how many squares of the lawn the user is currently hovering over
                #(used so that user can only select one square at a time because user can sometimes
                # select 2 squares if they are hovering between them)

    #loops through each individual lawn square
    for row in range(len(plantsNameGrid)):
        for col in range(len(plantsNameGrid[row])):
            #gets rect of that lawn square
            square = Rect([x + col * width, y + row * length, width, length])

            #checks if mouse cursor is hovering over it and if only one square is selected
            if square.x < mx < (square.x + length) and square.y < my < (square.y + length) and oneSpot != 1:
                square = Rect([x + col * width, y + row * length, width, length]) #get rect of that square again since it is only selected square
                oneSpot = 1 #change oneSpot to 1 so that we know a square is already selected
                if plant != "" and plantsNameGrid[row][col] == "": #if current plant is not an empty string and the lawn square has no plant
                    pic = pic.copy()
                    pic = pic.convert()
                    pic.set_colorkey((0, 0, 0))
                    pic.set_alpha(128)
                    #get the pic of the plant sprite from the drawScene loop, convert it to alpha, and blit it on that lawn square
                    #(used to indicate where plant will be placed with user left clicks)
                    screen.blit(pic, (square.x, square.y))
                    if mb[0] == 1: #if user left clicks 
                        plantSound.play()
                        plantsNameGrid[row][col] = plant #change the plant name grid to the current plant (so we can identify it at that square)
                        plantsSpriteGrid[row][col] = 0 #change the plant sprite grid to 0 (we start at index 0 when we blit the plant sprites from the sprite list in plantAnimation)
                        healthIndex = inList(plant, plantsHealthList) #get index of the plant health from the plantsHealthList (only get health data from this list)
                        plantsHealthGrid[row][col] = plantsHealthList[healthIndex][1] #set the health of the plant in the plantsHealthGrid (used to check current health oof plant on screen)
                        selectingPlant = False #change selectingPlant to false so user stops selecting plant
                        sunAmount -= plantsCostList[sunIndex][1] #decrease the sun amountusing data in plantsCostList(since we "bought" a plant)
                        plantsRechargeList.append([plant, time.get_ticks()]) #append plant and current time to plantsRechargeList so that we can recharge the plant
                        if plant != "nut" or plant != "bomb": #check if the plant is not nut or bomb (they don't perfrom periodic actions)
                            plantsActionList.append([plant, row, col, time.get_ticks()]) #append the plant, row, col, and current time to plantsActionList, so that we can check whenever plant perfroms new action 
                    
            else:
                square = Rect([x + col * width, y + row * length, width, length])
                oneSpot = 0 #otherwise we change oneSpot back to 0 if user is not hovering over it

    if mb[2] == 1: #if user right clicks, change selectingPlant to false so user stops selecting plant
        selectingPlant = False
                        
    return [selectingPlant, plantsRechargeList, plantsActionList, sunAmount] #return any vars changed when selecting a plant

def plantAnimation(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, mineCheckList, plantsActionList, zombiesList, width, length):
    #function used to animate plants on lawn using sprites from their sprites list

    #loops through each lawn square
    for row in range(len(plantsNameGrid)):
        for col in range(len(plantsNameGrid[row])):
            if plantsNameGrid[row][col] != "" and plantsSpriteGrid[row][col] != "": #if lawnsquare doesn't contain a plant
                #if the plant is nut
                if plantsNameGrid[row][col] == "nut":
                    #since the nutList contains 3 seperate lists of sprites to use depending on the nut's health,
                    #we have to find the index of the one of the 3 lists depending on the nut's current health,
                    #so that we know which set of sprites to use
                    if plantsHealthGrid[row][col] > 2700:
                        indexValue = 1
                    elif plantsHealthGrid[row][col] > 1800:
                        indexValue = 2
                    else:
                        indexValue = 3
                    listName = "%sList" % (plantsNameGrid[row][col]) #gets the variable name of the spriteList for the respective plant

                    #find x and y coor of lawn square
                    x = 50 + col * width
                    y = 100 + row * length

                    #to animate sprites, we have to increase the index in plantSpriteGird by a small value (0.1) to cause delay
                    #in animation instead of animation occuring everytime game loops, and we use the integer value
                    #of that index to find which sprite in the spriteList we blit on screen.
                    #when we reach the end of the list (index + 1 equals the length of the list), we have to restart the index back to 0
                    #to restart animation again
                    if (int(plantsSpriteGrid[row][col]) + 1) == len((eval(listName))[indexValue]): 
                        plantsSpriteGrid[row][col] = 0
                        pic = (eval(listName))[indexValue][int(plantsSpriteGrid[row][col])]
                        screen.blit(pic, (x, y))
                    else:
                        plantsSpriteGrid[row][col] += 0.1
                        pic = (eval(listName))[indexValue][int(plantsSpriteGrid[row][col])]
                        screen.blit(pic, (x, y))
    
                        
                elif plantsNameGrid[row][col]  == "mine":
                    #if plant is mine
                    explode = False #boolean used to check if mine is ready to explode or is exploding 
                    for mine in mineCheckList: #check all the mines currently on the screen that are ready to explode or is exploding in the mineCheckList
                        if (mine[0], mine[1]) == (row, col): #if the row and col match the ones in the list
                            explode = True #we set the boolean to true
                            mineAction = mine[2] #we get the current action of that mine as well (either waiting to explode or is currently exploding)

                    #if mine is ready to explode or is exploding    
                    if explode == True:
                        #animation explained above with the nut
                        listName = "%sList" % (plantsNameGrid[row][col])
                        x = 50 + col * width
                        y = 100 + row * length
                        #if the mine is waiting to explode, we only blit up to the first 7 sprites since those sprites show the mine waiting to explode
                        if (int(plantsSpriteGrid[row][col]) + 1) > 7 and mineAction == "waiting": 
                            plantsSpriteGrid[row][col] = 0
                            pic = eval(listName)[int(plantsSpriteGrid[row][col])]
                            screen.blit(pic, (x, y))

                        #if the mine that is currently exploding is finished playing through all the sprites, we have to remove the mine from lawn  
                        elif (int(plantsSpriteGrid[row][col]) + 1) == 15 and mineAction == "exploding":
                            removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, row, col)

                        #otherwise if the mine is currently exploding, we blit up to the final last 8 sprites since those sprites show the mine exploding
                        else:
                            plantsSpriteGrid[row][col] += 0.2
                            pic = eval(listName)[int(plantsSpriteGrid[row][col])]
                            screen.blit(pic, (x, y))

                        #we have to check if the mine that is ready to explode is colliding with a zombie (so we can kill that zombie)
                        for zombie in zombiesList:
                            if row == zombie[6]: #if the mine and zombie are in same row
                                square = [x, y, width, length] #ger the rect of the current lawn square
                                if 0 < sqrt((square[0] - zombie[1]) ** 2 + (square[1] - zombie[2]) ** 2) < width // 2: #if the distance between the zombie and mine is less than half the width of the square
                                    zombiesList.remove([zombie[0], zombie[1], zombie[2], zombie[3], zombie[4], zombie[5], zombie[6], zombie[7], zombie[8]]) #we remove the zombie
                                    for mine in mineCheckList: #loop through mineCheckList
                                        if (mine[0], mine[1]) == (row, col):
                                            #we have to set the mine in that list to exploding so the sprite animation would be different
                                            mine[2] = "exploding"
                                            plantsSpriteGrid[row][col] = 8 #we start the sprite index at 8 since those sprites show the mine exploding
                                            mineSound.play()
                                    break #break the loop since we only kill one zombie
                                
                    elif explode == False:
                        #otherwise we just blit the respective sprites if the mine is NOT ready to explode or is NOT exploding
                        listName = "%sList" % (plantsNameGrid[row][col])
                        x = 50 + col * width
                        y = 100 + row * length
                        screen.blit(eval(listName)[0], (x, y))
                    
                elif plantsNameGrid[row][col]  == "bomb":
                    #if the plant is bomb 
                    x = 50 + col * width
                    y = 100 + row * length
                    #we just animate the plant as normally except when the sprite index reaches over 5, we have to kill zombies in the surrounding
                    #area since those sprites show the bomb exploding
                    if int(plantsSpriteGrid[row][col]) > 5: 
                        plantsSpriteGrid[row][col] += 0.2
                        pic = bombList[int(plantsSpriteGrid[row][col])]
                        screen.blit(pic, (x - width, y - length))
                        
                        for zombie in zombiesList: #we check all the zombies and if the collide with the area of the sprite, we remove the zombie
                            if Rect(zombie[1], zombie[2], 90, 100).colliderect([x - width, y - length, pic.get_width(), pic.get_height()]):
                                zombiesList.remove([zombie[0], zombie[1], zombie[2], zombie[3], zombie[4], zombie[5], zombie[6], zombie[7], zombie[8]])
                                
                        if (int(plantsSpriteGrid[row][col]) + 1) == len(bombList):
                            #if the sprite index reaches the end of the bomb sprite lise, we remove the bomb because it is done exploding
                            removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, row, col)
                            
                    else:
                        #if the sprite index is below 5.5 (so it doesn't round to 6), we just animate it normally, and if it is over 5.5, we change the
                        #sprite index to 6 so that it can start exploding
                        if plantsSpriteGrid[row][col] < 5.5:
                            plantsSpriteGrid[row][col] += 0.2
                            pic = bombList[int(plantsSpriteGrid[row][col])]
                            screen.blit(pic, (x, y))
                        else:
                            plantsSpriteGrid[row][col] = 6
                            bombSound.play()
                    
                else:
                    #if the plant is not nut, mine, or bomb, we animate them normally (explained above in nut animation)
                    listName = "%sList" % (plantsNameGrid[row][col])
                    x = 50 + col * width
                    y = 100 + row * length
                    if (int(plantsSpriteGrid[row][col]) + 1) == len(eval(listName)): 
                        plantsSpriteGrid[row][col] = 0
                        pic = eval(listName)[int(plantsSpriteGrid[row][col])]
                        screen.blit(pic, (x, y))
                    else:
                        plantsSpriteGrid[row][col] += 0.1
                        pic = eval(listName)[int(plantsSpriteGrid[row][col])]
                        screen.blit(pic, (x, y))

def removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, row, col):
    #this function removes a plant that was placed on the lawn already

    #if the plant to be removed is mine, we need to check the mineCheckList, and remove the mine at that row and col from it
    #[row, col, stateofmine]
    if plantsNameGrid[row][col] == "mine":
        if len(mineCheckList) > 0:
            for mine in mineCheckList:
                if (row, col) == (mine[0], mine[1]): #check if row and col of mine to be removed is equal the row and col in list
                                                     #and we remove it if it is   
                    if mine[2] == "exploding":
                        mineCheckList.remove([row, col, "exploding"])
                    else:
                        mineCheckList.remove([row, col])

    #change the values of the square plant is on back to empty string so another plant can be placed on it                            
    plantsNameGrid[row][col] = ""
    plantsSpriteGrid[row][col] = ""
    plantsHealthGrid[row][col] = ""

    #loop through plantsActionList and check if the action list has a row and col value equal to the row and col of the plant being removed,
    #and we remove it if it does
    for action in plantsActionList:
        if action[1] == row and action[2] == col:
            plantsActionList.remove([action[0], action[1], action[2], action[3]])
    
def plantRecharge(plantsRechargeList, plantsRechargeTimesList, selectedPlants):
    #function recharges plant seed packets so user has to wait before placing new plant

    #we loop through all the seed packets currently recharging in plantsRechargeList
    for rechargeList in plantsRechargeList:
        if rechargeList[0] in selectedPlants: #check if plant recharging is in selectedPlants 
            timeIndex = inList(rechargeList[0], plantsRechargeTimesList) #we get the index of the list containing the data value
                                                                         #of how much milliseconds it takes to recharge a plant in the plantsRechargeTimesList
            if time.get_ticks() - rechargeList[1] >= plantsRechargeTimesList[timeIndex][1]: #check if the current time subtract the recharge time
                                                                                            #is greater or equal to the data time
                ind = plantsRechargeList.index(rechargeList) 
                del plantsRechargeList[ind] #we remove it from the recharge list if it is
                
    return plantsRechargeList #return plantsRechargeList so we can update the plants recharging
                  
def plantAction(plantsNameGrid, sunEnergyList, mineCheckList, plantsActionList, plantsActionTimesList, bulletsList, width, length):
    #function checks timing of plants and performs a plant action if the timer reaches the time in the data list 
    for action in plantsActionList: #loops through all actions [plantname, row, col, time]
        timeIndex = inList(action[0], plantsActionTimesList) #gets data of time of how long it takes for each plant to perform action
        if action[0] == plantsActionTimesList[timeIndex][0]: #if the action name is equal to the name in the data list
            if time.get_ticks() - action[3] >= plantsActionTimesList[timeIndex][1]: #we use have to subtract current time from time
                                                                                    #in action list and check if it is greater than
                                                                                    #the time in the data list to perform the action 
                action[3] = time.get_ticks() #if it is we have to reset the action timer to the current time so that the timer starts from 0 again
                if action[0] == "pea":
                    bulletsList.append(["pea", 50 + width * action[2], 100 + length * action[1] + 10, action[1]])
                    #we have to append a bullet to the bulletsList if the plant is pea because it shoots a bullet
                elif action[0] == "snowpea":
                    bulletsList.append(["snowpea", 50 + width * action[2], 100 + length * action[1] + 10, action[1]])
                    #we have to append a bullet to the bulletsList if the plant is snowPea because it shoots a bullet
                elif action[0] == "sun":
                    addSun(plantsNameGrid, width, length, sunEnergyList, "plant", action[1], action[2])
                    #we have to add sun to the screen if the plant is a sunflower
                elif action[0] == "mine":
                    mineCheckList.append([action[1], action[2], "waiting"])
                    #we have to append the mine to the mineCheckList so that it is active
                    
    return [plantsActionList, bulletsList]                    

def checkBullets(bulletsList, zombiesList):
    #this function moves all the bullets in the bulletsList across the screen and checks if it hits a zombie
    for bullet in bulletsList: #loops through all bullets [name, x, y, row]
        bullet[1] = bullet[1] + 10 #increase x coor of bullet
        if bullet[1] >= screenWidth: #if the bullet reaches the end of the screen, we have to remove it
            ind = bulletsList.index(bullet)
            del bulletsList[ind]
        screen.blit(eval(bullet[0] + "Bullet"), (bullet[1], bullet[2] + 40)) #blit the picture of the bullet on the screen
        for zombie in zombiesList: #we loop through all the zombies in zombiesList
            if int(bullet[3]) == int(zombie[6]): #if the bullet is on the same row as the zombie, we check if it collides with the zombie
                if Rect(bullet[1], bullet[2], 20, 20).colliderect(Rect(zombie[1], zombie[2], 90, 100)):
                    if zombie[0] == "bucket":
                        hitSound2.play()
                    else:
                        hitSound1.play()
                    zombie[4] -= 1 #we decrease the zombie's health by 1 if the bullet hits them
                    if bullet[0] == "snowpea":
                        zombie[8] = "freeze" #we have to make the zombie frozen so we know how to animate it in zombiesAnimation function

                    #then we have to remobe the bullet from the screen and remove the zombie if its health falls belows 0
                    if [bullet[0], bullet[1], bullet[2], bullet[3]] in bulletsList:
                        bulletsList.remove([bullet[0], bullet[1], bullet[2], bullet[3]])
                    if zombie[4] <= 0:
                        zombiesList.remove([zombie[0], zombie[1], zombie[2], zombie[3], zombie[4], zombie[5], zombie[6], zombie[7], zombie[8]])
                        zombieDeathSound.play()
    return [bulletsList, zombiesList]





#SUNRELATED FUNCTIONS
def addSun(plantsNameGrid, width, length, sunEnergyList, source, row, col):
    #function adds sun on the screen
    #[spriteIndex, x, y, stateofsun, row, col]
    if source == "sky": #if the sun came from the sky
        row = randint(0, len(plantsNameGrid) - 1)
        col = randint(0, len(plantsNameGrid) - 1)
        #we have to get a random row and col, find its x coor, make its y coor from the top of the screen, and add it to the sunEnergyList
        x = 50 + col * width
        y = 100
        sunEnergyList.append([0, x, y, "falling", row, col])
    elif source == "plant": #if the sun came from a sunflower, then we just add the sun at that row, col where the plant is 
        row = row
        col = col
        x = 50 + col * width
        y = 100 + row * length
        sunEnergyList.append([0, x, y, "idle", row, col])
        
def sunAnimation(sunEnergyList, sunSpriteList, length):
    #function animate and move sun sprites
    for sunEnergy in sunEnergyList: #loops through all the sun in sunEnergyList [spriteIndex, x, y, stateofsun, row, col]
        if sunEnergy[3] == "falling": #if the sun came from the sky and is still falling, we have to increase its y coor so it keeps falling until
                                      #it reaches the row it is supposed to land on
            if sunEnergy[2] < (100 + sunEnergy[4] * length): 
                sunEnergy[2] += 1

        #to animate the sun sprite, we add a decimal num to the spriteIndex of the sunEnergy and blit the sprite in the list using theint of its current
        #spriteIndex as a index to find the sprite; if the spriteIndex reaches the end of the list, we have to reset it back to 0
        if (int(sunEnergy[0]) + 1) >= len(sunSpriteList): 
            sunEnergy[0] = 0
            screen.blit(sunSpriteList[int(sunEnergy[0])], (sunEnergy[1], sunEnergy[2]))
        else:
            sunEnergy[0] += 0.05
            screen.blit(sunSpriteList[int(sunEnergy[0])], (sunEnergy[1], sunEnergy[2]))
            
def checkSun(sunEnergyList, returningSunList):
    #this function checks if the user clicks on the sun
    for sunEnergy in sunEnergyList: #loops through each sunEnergy
        if Rect(sunEnergy[1], sunEnergy[2], (sunSpriteList[int(sunEnergy[0])].get_width()), (sunSpriteList[int(sunEnergy[0])].get_height())).collidepoint(mx, my):
            #checks if user collides with and clicks on the sun
            if mb[0] == 1: 
                ind = sunEnergyList.index(sunEnergy) #if they do, we have to append the sun to the returningSunList and remove it from the sunEnergyList
                                                     #as the user already selected it
                returningSunList.append(sunEnergyList[ind])
                del sunEnergyList[ind]

def returnSun(sunAmount, returningSunList, sunSpriteList):
    #this function animates the sun the user already collected by moving in a straight line to the ui select bar and increases the sunAmount if it does
    for sunEnergy in returningSunList: #loops through all the sunEnergy in the returningSunList [spriteIndex, x, y, stateofsun, row, col]
        if sqrt((sunEnergy[1] - 120) ** 2 + (sunEnergy[2] - 15) ** 2) < 100: #if the distance of the sun energy to the ui bar (coor of ui bar is (120, 15))
                                                                             #is less than 100 pixels, we have to increase the sunAmount and delete the sun from
                                                                             #the returningSunList
            sunAmount += 25
            pointsSound.play()
            ind = returningSunList.index(sunEnergy)
            del returningSunList[ind]
        else:
            #otherwise we have to move the sun to the ui bar by gerring the angle of the right triangle formed from the hypotenuse of the
            #straight line from the sunEnergy to the ui bar, and we have to decrease the x, y of the sunEnergy by the cos, sin of the angle
            #scaled up by 100
            angle = radians(tan((sunEnergy[1] - 120) / (sunEnergy[2] - 15)))
            angle = atan2((sunEnergy[2] - 0), (sunEnergy[1] - 120))
            sunEnergy[1] -= 100 * cos(angle)
            sunEnergy[2] -= 100 * sin(angle)
            screen.blit(sunSpriteList[0], (sunEnergy[1], sunEnergy[2])) #blits the sunSprite on the screen
    return sunAmount





#ZOMBIE RELATED FUNCTIONS
def addZombies(zombiesList, waveCount, screenWidth, y, width, length):
    #this function adds zombies on the screen whenever there is a new wave
    zombieNum = randint(1, waveCount) #we have to get a random number of the num of zombies to add to the screen (from 1 to the current wave num)
    soundNum = randint(1, 5) #plays a random sound out of 5 sounds whenever we add new zombies
    soundName = eval("zombieSound" + str(soundNum))
    soundName.play()
    for i in range(zombieNum): #for each of the random zombies we are adding to the screen
        zombieType = randint(1, 6) #gets a random num to determine the zombie type
        zombieX = screenWidth #zombie x coor starts at right mose side of screen
            
        randRow = randint(0, 4) #gets a random num to determine row zombie is in (starts at index 0)
        zombieY = y + (randRow * length) #gets zombie y coor using row

        #depending on the zombie type determined, we set the speed, health, spriteIndex, and row depending on the zombie type
        #and we add the zombie to the zombiesList
        if zombieType == 1:
            speed = width / (40 * 4.7)
            health = 10
            spriteIndex = 0
            zombiesList.append(["normal", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])
        elif zombieType == 2:
            speed = width / (40 * 4.7)
            health = 20
            spriteIndex = 0
            zombiesList.append(["cone", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])
        elif zombieType == 3:
            speed = width / (40 * 4.7)
            health = 30
            spriteIndex = 0
            zombiesList.append(["bucket", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])
        elif zombieType == 4:
            speed = 2 * (width / (40 * 4.7))
            health = 5
            spriteIndex = 0
            zombiesList.append(["football", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])
        elif zombieType == 5:
            speed = 0.5 * (width / (40 * 4.7))
            health = 40
            spriteIndex = 0
            zombiesList.append(["trash", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])
        elif zombieType == 6:
            speed = 0.5 * (width / (40 * 4.7))
            health = 30
            spriteIndex = 0
            zombiesList.append(["door", zombieX, zombieY, speed, health, spriteIndex, randRow, "walking", "normal"])

def zombieAnimation(currentScreen, zombiesList, normalZombieList, normalZombieEat, zombieObjectList, plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, x, y, width, length):
    #this function animates the zombies using sprites, moves the zombies, and checks if the zombies are eating a plant, as well as check if zombie
    #reach end of screen (lose)
    #zombie [zombietype, x, y, speed, health, spriteIndex, rowIndex, currentactionofzombie, ifzombieisfrozen]
    for zombie in zombiesList: #we loop through all the zombies
        for row in range(len(plantsNameGrid)): #we loop through all the squares of the lawn
            for col in range(len(plantsNameGrid[row])):
                square = [x + col * width, y + row * length, width, length] #get the rect of the square of the lawn 
                if plantsNameGrid[row][col] != "" and 0 < sqrt((square[0] - zombie[1]) ** 2 + (square[1] - zombie[2]) ** 2) < width // 2:
                    #if the square does contain a plant and the distance between the zombie and the plant is less than half of the square width
                    zombie[7] = [row, col] #we set the currentactionofzombie to the row and col of where the plant is at so that the
                                           #zombie can eat the plant instead of walking
    for zombie in zombiesList: #we loop through all the zombies again 
        if zombie[1] < 0:
            #if the zombie x coor reaches the end of the screen (player loses)
            loseZombie = zombie 
            del zombiesList[:] #we remove all of the other zombies in the list, set the x coor of the zombie that reached the end of the screen to 50
                               #and append it to zombiesList (so that we only animate that zombie when it walks up to the house)
            loseZombie[1] = 50
            zombiesList.append(loseZombie)
            currentScreen = "lose" #we set the currentScreen to "lose" so that the game ends and we only show the zombie walking up to the house
            
        if zombie[7] == "walking": #checks if the zombie is walking 

            freezePic = "" #variable used to determine if zombie is frozen
            
            if currentScreen != "lose": #if the player did not lose
                #we decrease the x coor of the zombie by their speed to move it across screen; if the zombie is frozen, it only moves at half their speed and the
                #we set the freezePic variable to the freezeAlpha picture we are going to load
                if zombie[8] == "normal":
                    zombie[1] -= zombie[3]

                elif zombie[8] == "freeze":
                    zombie[1] -= zombie[3] / 2
                    freezePic = image.load("freezeAlpha.png").convert_alpha()
                     
            elif currentScreen == "lose": #however if the player is losing
                #same logic as above except we don't change the zombie x coor since the screen is side scrolling to the house
                #while the playing is losing. we only increase or decrease (depending on if zombie is above or below middle of screen)
                #the zombie y coor if the distance of it to the middle of the screen is less than 5 so that it can go towards the middle of
                #the screen where the house is
                if zombie[8] == "normal":
                    if sqrt((0 - zombie[1]) ** 2 + (400 - zombie[2]) ** 2) > 5:
                        if zombie[2] > 400:
                            zombie[2] -= 1
                        else:
                            zombie[2] += 1
                            

                elif zombie[8] == "freeze":
                    if 0 < sqrt((400 - zombie[1]) ** 2 + (0 - zombie[2]) ** 2) < 5:
                        if zombie[2] > 400:
                            zombie[2] -= 1
                        else:
                            zombie[2] += 1
                            
                    freezePic = image.load("freezeAlpha.png").convert_alpha()

            #we animate the zombie by blitting the respective sprite from the normalZombieList depending on the int of its spriteIndex;
            #we increase the sprite index by 0.2 to cause delay between the sprites and if the spriteIndex reaches the end of the list,
            #we have to reset it back to 0
            if (int(zombie[5]) + 1) == len(normalZombieList): 
                zombie[5] = 0
                pic = normalZombieList[int(zombie[5])]
            else:
                zombie[5] += 0.2
                pic = normalZombieList[int(zombie[5])]

            #if the zombie is frozen, we have to blit a blue alpha filter over it to show that it's frozen
            if freezePic != "":
                #we have to generate a new surface 
                freezeSurface = Surface((90, 100), SRCALPHA).convert()
                
                freezeSurface.blit(pic, (0, 0)) #blit the sprite on the surface

                blit_alpha(freezeSurface, freezePic, (0, 0), 125) #use the blit_alpha function to blit the filter over
                                                                  #the surface so that it doesn't "erase" the sprite underneath 

                freezeCol = freezeSurface.get_at((0, 0)) #get the colour of that filter
                freezeSurface.set_colorkey(freezeCol) #use colourkey to remove the filter where it is not overtop the zombie
                                                      #so that a blue rectangle wont't surround zombie
                   
                screen.blit(freezeSurface, (zombie[1], zombie[2]))
                
            else:
                #otherwise if the zombie is not frozen, we blit the sprite normally
                screen.blit(pic, (zombie[1], zombie[2]))
                            
        else: #otherwise if the zombie is eating a plant
            #we do the same sprite animation above as if the zombie is walking above, except that we have to use sprites
            #from the normalZombieEat list to show that the zombie is eating the plant
            if (int(zombie[5]) + 1) == len(normalZombieEat): 
                zombie[5] = 0
                pic = normalZombieEat[int(zombie[5])]
                #we also have to decrease the health of the plant the zombie is eating by 1 in the plantsHealthGrid
                if plantsHealthGrid[zombie[7][0]][zombie[7][1]] != "" and plantsHealthGrid[zombie[7][0]][zombie[7][1]] > 0:
                    plantsHealthGrid[zombie[7][0]][zombie[7][1]] -= 1
                    if eatChannel.get_busy() == 0: #we use a special sound channel to play the eating sound and we have to check
                                                   #if it is not already playing to avoid stressing out the sound channel 
                        eatChannel.play(zombieEatSound)
                elif plantsHealthGrid[zombie[7][0]][zombie[7][1]] != "": #if the plant's health reaches zero, we have to remove the plant
                                                                         #and change the action of the zombie back to "walking"
                                                    
                    removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, zombie[7][0], zombie[7][1])
                    gulpSound.play()
                    zombie[7] = "walking"

                if len(zombie[7]) == 2 and plantsHealthGrid[zombie[7][0]][zombie[7][1]] == "": #if the zombie is still eating and there is no plant
                                                                                               #on the lawn anymore, we have to change its action back to eating
                                                                                               #(used when two or more plants eat the same plant at the same time,
                                                                                               #the one who doesn't kill it will be stuck eating forever unless we do this)
                    zombie[7] = "walking"
                    
                screen.blit(pic, (zombie[1], zombie[2])) 
            else:
                #this is the same as above except this is only if the spriteIndex of the zombies is not at the end of the list
                zombie[5] += 0.2
                if (int(zombie[5]) + 1) >= len(normalZombieEat):
                    zombie[5] = 0
                    pic = normalZombieEat[int(zombie[5])]
                else:
                    pic = normalZombieEat[int(zombie[5])]

                if plantsHealthGrid[zombie[7][0]][zombie[7][1]] != "" and plantsHealthGrid[zombie[7][0]][zombie[7][1]] > 0:
                    plantsHealthGrid[zombie[7][0]][zombie[7][1]] -= 1
                    if eatChannel.get_busy() == 0:
                        eatChannel.play(zombieEatSound)
                elif plantsHealthGrid[zombie[7][0]][zombie[7][1]] != "":
                    removePlant(plantsNameGrid, plantsSpriteGrid, plantsHealthGrid, plantsActionList, mineCheckList, zombie[7][0], zombie[7][1])
                    gulpSound.play()
                    zombie[7] = "walking"

                if len(zombie[7]) == 2 and plantsHealthGrid[zombie[7][0]][zombie[7][1]] == "":
                    zombie[7] = "walking"

                #blits freeze filter overtop zombie if it's frozen
                if zombie[8] == "freeze":
                    freezePic = image.load("freezeAlpha.png").convert_alpha()
                    freezeSurface = Surface((90, 100), SRCALPHA).convert()
                    
                    freezeSurface.blit(pic, (0, 0))

                    blit_alpha(freezeSurface, freezePic, (0, 0), 125)

                    freezeCol = freezeSurface.get_at((0, 0))
                    freezeSurface.set_colorkey(freezeCol)
                    screen.blit(freezeSurface, (zombie[1], zombie[2]))
                else:
                    screen.blit(pic, (zombie[1], zombie[2]))

        #lastly, if the zombie type is not "normal", then we have to blit a special object on top
        #of the zombie to show that is a different type; we have to get the picture in the zombieObjectList
        #by using the zombie type name to fnd the index of the 2-d list that contains the sprite
        objectIndex = inList(zombie[0], zombieObjectList)
        if zombie[0] == "cone":
            screen.blit(zombieObjectList[objectIndex][1], (zombie[1] + 25, zombie[2] - 30))
        elif zombie[0] == "bucket":
            screen.blit(zombieObjectList[objectIndex][1], (zombie[1] + 12, zombie[2] - 27))
        elif zombie[0] == "football":
            screen.blit(zombieObjectList[objectIndex][1], (zombie[1] + 12, zombie[2] - 27))
        elif zombie[0] == "trash":
            screen.blit(zombieObjectList[objectIndex][1], (zombie[1] - 30, zombie[2] + 25))
        elif zombie[0] == "door":
            screen.blit(zombieObjectList[objectIndex][1], (zombie[1] - 10, zombie[2]))
            
    return [zombiesList, currentScreen]
       
#INITIALIZING PYGAME
init() 
font.init()
size = (screenWidth, screenHeight) = (1200, 800)
screen = display.set_mode(size)

display.set_caption("Plants vs Zombies - Phillip Pham")

mx, my = mouse.get_pos() 

#ASSETS

#MENU IMAGES
menuBackground = image.load("menu/menu.jpg")
logoPic = image.load("menu/logo.png")
helpBackground = image.load("menu/help.png")
startButton = image.load("menu/startbutton.png")
instructionsBackground = image.load("menu/instructions.png")
nextButton1 = image.load("menu/nextbutton1.png")
nextButton2 = image.load("menu/nextbutton2.png")
backButton = image.load("menu/backbutton.png")
backButton.set_colorkey((255, 255, 255))

#MENU BUTTON RECTS 
playRect = Rect(600, 90, 500, 175)
helpRect = Rect(950, 640, 100, 100)
quitRect = Rect(1065, 640, 100, 100)
helpMenuRect = Rect(480, 695, 235, 55)
nextRect = Rect(1050, 340, 148, 148)
backRect = Rect(1000, 620, 127, 125)

#MUSIC AND SOUNDS
mixer.init()
mixer.set_num_channels(10) #sets maximum of 10 sound channels

hitSound1 = mixer.Sound("sounds/splat2.wav")
hitSound2 = mixer.Sound("sounds/shieldhit.wav")

mineSound = mixer.Sound("sounds/potato_mine.wav")
bombSound = mixer.Sound("sounds/cherrybomb.wav")
lawnMowerSound = mixer.Sound("sounds/lawnmower.wav")
pointsSound = mixer.Sound("sounds/points.wav")
plantSound = mixer.Sound("sounds/plant.wav")
packetSound = mixer.Sound("sounds/seedlift.wav")
shovelPlantSound = mixer.Sound("sounds/plant2.wav")
shovelSound = mixer.Sound("sounds/Shovel.ogx")

zombieSound1 = mixer.Sound("sounds/awooga.wav")
zombieSound2 = mixer.Sound("sounds/groan5.wav")
zombieSound3 = mixer.Sound("sounds/hugewave.wav")
zombieSound4 = mixer.Sound("sounds/siren.wav")
zombieSound5 = mixer.Sound("sounds/sukhbir6.wav")

zombieDeathSound = mixer.Sound("sounds/groan2.wav")

screamSound = mixer.Sound("sounds/scream.wav")

gulpSound = mixer.Sound("sounds/gulp.wav")

loseSound = mixer.Sound("sounds/losemusic.wav")
zombieEatSound = mixer.Sound("sounds/ZombieBite.ogx")
zombieEatSound.set_volume(1.0)


eatChannel = mixer.Channel(5) #special channel to play zombe eating sound (to avoid sound bug when too much sounds are playing)

#BACKGROUND IMAGES
back1 = image.load("backgrounds/stage1.jpg").convert_alpha()
backSubsurface = back1.subsurface([290, 0, 1200, 800]) 

back = backSubsurface 

#LOSE GAME VARIABLES
loseX = 0 #counter variable used to indicate which x coor to start taking subsurface of background
          #so that we can side scroll background image to show house when player loses
loseBack = image.load("menu/loseBack.jpg").convert_alpha() #background for when you lose game

#UI
selectBar = image.load("backgrounds/bar.png").convert_alpha() #plant select ui bar

#PLANT SPRITES (list that contains sprites of an individual plant)
peaList = addSprites("sprites", "plants", "pea", "pea", 1, 8)
sunList = addSprites("sprites", "plants", "sun", "sun", 1, 8)
snowpeaList = addSprites("sprites", "plants", "snowpea", "snowpea", 1, 8)
mineList = addSprites("sprites", "plants", "mine", "mine", 1, 16)
nutList = [image.load("sprites/plants/nut/nut1-1.png"), addSprites("sprites", "plants", "nut", "nut", 1, 4), addSprites("sprites", "plants", "nut", "nut", 2, 4), addSprites("sprites", "plants", "nut", "nut", 3, 4)]
bombList = addSprites("sprites", "plants", "bomb", "bomb", 1, 14)

#PLANT SEED PACKETS (to blit on select plant ui bar to inidicate what plant to select)
peaPacket = image.load("sprites/plants/pea/PeashooterSeedPacket.png").convert_alpha()
sunPacket = image.load("sprites/plants/sun/SunflowerSeedPacket.png").convert_alpha()
nutPacket = image.load("sprites/plants/nut/WallnutSeedPacket.png").convert_alpha()
snowpeaPacket = image.load("sprites/plants/snowpea/SnowpeaSeedPacket.png").convert_alpha()
bombPacket = image.load("sprites/plants/bomb/CherrybombSeedPacket.png").convert_alpha()
minePacket = image.load("sprites/plants/mine/PotatomineSeedPacket.png").convert_alpha()

#BULLETS (sprites for bullets produced from peashooter and snowpea)
peaBullet = image.load("sprites/plants/pea/b1.png").convert_alpha()
snowpeaBullet = image.load("sprites/plants/snowpea/snowb1.png").convert_alpha()
bulletsList = [] #list to hold all bullets on screen (holds lists of [plantname, x, y, row])

#SELECTED PLANTS AND BOOLEAN FOR SELECTING PLANTS
selectedPlants = ["pea", "sun", "nut", "snowpea", "bomb", "mine"] #list to contain plants that you can select to plant on screen
selectingPlant = False #boolean used to check whether user is selecting a plant

#SHOVEL TOOL
shovelCursor = image.load("sprites/extra/ShovelCursor.png").convert_alpha() #cursor used when user is shovelling plants
shovelPic = image.load("sprites/extra/Shovel.jpg").convert_alpha() #picture used as shovel button 
shovelRect = Rect(660, 0, 100, 100) #rect to check if user click on shovel button
shovellingPlant = False #boolean used to check whether user is shovelling a plant

#CURRENT PLANT
plant = "" #variable to hold current plant user is planting on screen (empty string at start)


#PLANT DATA LISTS; GETS DATA ABOUT CERTAIN ATTRIBUTES ABOUT PLANTS
plantsRechargeList = [] #list holds all the plants currently rechanging (holds lists of [plant, currentrechargetime]) 
plantsRechargeTimesList = [] #list to hold data of recharge times of different plants (holds lists of [plantname, plantrechargetime])
plantsRechargeTimesList.append(["pea", 7500])
plantsRechargeTimesList.append(["sun", 7500])
plantsRechargeTimesList.append(["nut", 30000])
plantsRechargeTimesList.append(["snowpea", 7500])
plantsRechargeTimesList.append(["bomb", 50000])
plantsRechargeTimesList.append(["mine", 30000])

plantsActionList = [] #list to hold all plants that can perfrom an action (holds lists of [plant, row, col, currentactiontime])
plantsActionTimesList = [] #list to hold data of action times of different plants (holds lists of [plantname, plantactiontime])
plantsActionTimesList.append(["pea", 1430])
plantsActionTimesList.append(["sun", 24000])
plantsActionTimesList.append(["snowpea", 1430])
plantsActionTimesList.append(["mine", 15000])

plantsCostList = [] #list to hold data about sun cost to place a plant on the lawn (holds lists of [plantname, plantcost])
plantsCostList.append(["pea", 100])
plantsCostList.append(["sun", 50])
plantsCostList.append(["nut", 50])
plantsCostList.append(["snowpea", 175])
plantsCostList.append(["bomb", 150])
plantsCostList.append(["mine", 25])

plantsHealthList = [] #list to hold data about normal health value of each plant (holds lists of [plantname, planthealth])
plantsHealthList.append(["pea", 300])
plantsHealthList.append(["sun", 300])
plantsHealthList.append(["nut", 3600])
plantsHealthList.append(["snowpea", 300])
plantsHealthList.append(["bomb", 9999])
plantsHealthList.append(["mine", 300])

#MINE CHECK LIST
mineCheckList = [] #list to hold lists of active mines (holds lists of [row, col, stateofmine])

#GRID RELATED VARIABLES
plantsNameGrid = createGrid(9, 5) #grid to hold names of each plant on each square of the lawn
plantsSpriteGrid = createGrid(9, 5) #grid to hold sprite indexes of each plant on each square of the lawn
plantsHealthGrid = createGrid(9, 5) #grid to hold health values of each plant on each square of the lawn

width = 120 #width of one square of the lawn
length = 130 #length of one square of the lawn
x = 50 #x coor of where the first top left square of the lawn starts
y = 100 #y coor of where the first top left square of the lawn starts

#ZOMBIE RELATED VARIRABLES
zombiesList = [] #list of all zombie instances on the screen (holds lists of [zombietype, x, y, speed, health, spriteIndex, rowIndex, currentactionofzombie, ifzombieisfrozen])
normalZombieList = addSprites("sprites", "zombies", "normal", "normal", 1, 8) #zombie sprite list for walking zombie 
normalZombieEat = addSprites("sprites", "zombies", "normaleat", "normaleat", 1, 7) #zombie sprite list for eating zombie 

#zombie object images
conePic = image.load("sprites/zombies/cone/cone.png")
bucketPic = image.load("sprites/zombies/bucket/bucket.png")
footballPic = image.load("sprites/zombies/football/football.png")
trashPic = image.load("sprites/zombies/trash/trash.png")
doorPic = image.load("sprites/zombies/door/door.png")
zombieObjectList = [["cone", conePic], ["bucket", bucketPic], ["football", footballPic], ["trash", trashPic], ["door", doorPic]]
#list to hold images of all zombie objects so that we can easily find it given the zombie type


#LAWNMOWER VARIABLES
lawnMowerPic = image.load("sprites/lawnmower.png") #lawnmower image
lawnMowerList = [] #list to hold all lawnmower instances on screen (holds lists of [x, y, rowIndex])
for i in range(5):
    #use a for loop to place a lawnmower on each row of the lawn (use i as row num and use the row num to find y coor)
    lawnMowerList.append([5, 110 + i * 140, i])
    
runningMowerList = [] #list to hold all the lawnmowers that are currently moving across the screen to kill zombies (holds lists of [x, y, rowIndex])

#SUN ENERGY VARIABLES
sunSpriteList = addSprites("sprites", "extra", "sunenergy", "sunenergy", 1, 4) #sprite list to hold sprites of sun energy
sunEnergyList = [] #holds all sun energy instances currently on the lawn (holds lists of [spriteIndex, x, y, stateofsun, row, col])
returningSunList = [] #holds all sun energy user has clicked on that is returning to ui bar (holds lists of [spriteIndex, x, y, stateofsun, row, col])
sunAmount = 50 #variable to hold current amount of sun energy user has to buy plants
sunAmountFont = font.SysFont("SeriesOrbit", 20) #font used to display current sun amount on screen

#WAVE COUNT VARIABLES
waveCount = 0 #variable to hold how much waves of zombies has passed already


#TIMERS
fpsClock = time.Clock() #clock to control fps

SUNEVENT = USEREVENT + 0 #timer event used to add sun falling from sky

ZOMBIEEVENT = USEREVENT + 1 #timer event used to add another wave of zombies on screen

currentScreen = "menu"  #variable to hold name of current screen user is currently on (start with "menu")

#play bg music for menu
mixer.music.load("sounds/maintheme.mp3")
mixer.music.play(-1, 0.0)

#MAIN WHILE LOOP

while currentScreen != "exit": #while the currentScreen is not "exit"
    #if the currentScreen is "menu"
    if currentScreen == "menu":
        #we have running while loop to display menu screen
        running = True
        while running:
            for evt in event.get():
                #if user exits, we have to set running = False to break out of this inner while running loop and
                #set currentScreen = "exit" to break out of main loop
                if evt.type == QUIT:
                    running = False
                    currentScreen = "exit"
                    
            mx, my = mouse.get_pos() #gets current mouse pos
            mb = mouse.get_pressed() #checks if user clicks
            
            screen.blit(menuBackground, (0, 0)) #blits background of menu
            screen.blit(logoPic, (0, 50)) #blits logo on screen

            #blits my name on screen
            displayNameAmount = sunAmountFont.render("By: Phillip Pham", True, (0, 0, 0))
            screen.blit(displayNameAmount, (200, 400))

            #checks if user collides with play button and clicks on it;
            #if they do, we have to start game by setting running = False to break out of this loop,
            #set currentScreen = "game", play different bg music, and set the sun and zombie timers
            if playRect.collidepoint(mx, my):
                screen.blit(startButton, (playRect[0], playRect[1]))
                if mb[0] == 1:
                    running = False
                    currentScreen = "game"
                    mixer.music.load("sounds/day.mp3")
                    mixer.music.play(-1, 0.0)
                    sunTimer = time.set_timer(SUNEVENT, 5000)
                    zombieSpawnTimer = time.set_timer(ZOMBIEEVENT, 20000)

            #if user clicks on help button; we set currentScreen = "help"   
            if helpRect.collidepoint(mx, my) and mb[0] == 1:
                running = False
                currentScreen = "help"

            #if user clicks on help button; we set currentScreen = "exit" to exit game   
            if quitRect.collidepoint(mx, my) and mb[0] == 1:
                running = False
                currentScreen = "exit"
                
            display.flip() #updates screen

    #if user is on help screen     
    if currentScreen == "help":
        #we have while running loop to display help screen
        running = True
        while running:
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
                    currentScreen = "exit"
                    
            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()

            screen.blit(helpBackground, (0, 0)) #blit help background image

            screen.blit(nextButton1, (nextRect[0], nextRect[1])) #blit next button
            
            #if user clicks menu button, we return to the menu
            if helpMenuRect.collidepoint(mx, my) and mb[0] == 1:
                running = False
                currentScreen = "menu"

            if nextRect.collidepoint(mx, my): #if user clicks on next button, set currentScreen = "instructions"
                screen.blit(nextButton2, (nextRect[0], nextRect[1]))
                if mb[0] == 1:
                    running = False
                    currentScreen = "instructions"
                    
            display.flip()

    #if user is on instructions screen
        if currentScreen == "instructions":
            #we have while running loop to display instructions screen
            running = True
            while running:
                for evt in event.get():
                    if evt.type == QUIT:
                        running = False
                        currentScreen = "exit"
                        
                mx, my = mouse.get_pos()
                mb = mouse.get_pressed()

                screen.blit(instructionsBackground, (0, 0)) #blit instructions background

                screen.blit(backButton, (backRect[0], backRect[1])) #blit back button

                if backRect.collidepoint(mx, my) and mb[0] == 1: #if user clicks on back button, set currentScreen = "help"
                    running = False
                    currentScreen = "help"

                display.flip()
                
    #if user lost the game
    if currentScreen == "lost":
        running = True
        while running:
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
                    currentScreen = "exit"

            screen.fill((0, 0, 0))
            screen.blit(loseBack, (0, 0)) #blit lose background 

            displayLostAmount = sunAmountFont.render("Waves Survived: " + str(waveCount), True, (255, 255, 255))

            screen.blit(displayLostAmount, (500, 700)) #displayed rendered high score on screen
            display.flip()
    
    #if user is currently playing or is losing the game
    if currentScreen == "game" or currentScreen == "lose":
        #while running loop to run main game
        running = True
        while running:
            for evt in event.get():
                if evt.type == QUIT:
                    running = False
                    currentScreen = "exit"

                #if sun timer ticked, we add sun energy to the screen
                if evt.type == SUNEVENT:
                    addSun(plantsNameGrid, width, length, sunEnergyList, "sky", 0, 0)

                #if zombie timer ticked, we increase waveCount and call addZombies function
                if evt.type == ZOMBIEEVENT:
                    waveCount += 1
                    addZombies(zombiesList, waveCount, screenWidth, y, width, length)

                #checks if user is pressing mouse button down 
                if evt.type == MOUSEBUTTONDOWN:
                    #if user left clicks shovel button and selectingPlant and shovellingPlant are False
                    if evt.button == 1 and selectingPlant == False and shovellingPlant == False and shovelRect.collidepoint(mx, my):
                        shovellingPlant = True #we set shovellingPlant = True so user can shovel a plant
                        shovelSound.play()

                    #if user left clicks and selectingPlant and shovellingPlant are False, and plant is an empty string  
                    if evt.button == 1 and selectingPlant == False and plant == "" and shovellingPlant == False:
                        for ind in range(len(selectedPlants)):
                            #we check if user collided with a seed packet (we find rect of seed packet though plant's position in selectedPlants list)
                            if Rect(200 + 75 * ind, 10, 65, 90).collidepoint(mx, my):
                                selectingPlant = True #we change selectingPlant to true so user can select a plant
                                plant = selectedPlants[ind] #we get the plant name through selectedPlants list
                                nameIndex = inList(plant, plantsRechargeList) #we check if the plant is already in the plantsRechargeList 
                                sunIndex = inList(plant, plantsCostList) #we also have to check the cost of the plant
                                if (sunAmount - plantsCostList[sunIndex][1]) < 0: #if the user can't afford the plant with current sun currency
                                                                                  #we have to set plant back to an empty string and change selectingPlant to False
                                    plant = ""
                                    selectingPlant = False
                                elif nameIndex != -1:#also if plant is still recharging 
                                                    #we have to set plant back to an empty string and change selectingPlant to False
                                    plant = ""
                                    selectingPlant = False
                                else:
                                    packetSound.play()

            mx, my = mouse.get_pos() #gets current mouse pos
            mb = mouse.get_pressed() #checks if user click on screen

            checkSun(sunEnergyList, returningSunList) #check if user clicked on sun

            #run drawScene function and return respective variables
            returnList = drawScene(zombiesList, plantsActionList, bulletsList, plantsRechargeList, shovellingPlant, selectingPlant, sunAmount, plant, currentScreen, loseX)

            zombiesList = returnList[0]
            plantsActionList = returnList[1]
            bulletsList = returnList[2]
            plantsRechargeList = returnList[3]
            shovellingPlant = returnList[4]
            selectingPlant = returnList[5]
            sunAmount = returnList[6]
            plant = returnList[7]
            currentScreen = returnList[8]
            loseX = returnList[9]

            #if the user lost the game (figured out through returning currentScreen from drawScene()), we have to break this game loop
            #so that we go directly to lose screen
            if currentScreen == "lost":
                break
            
            sunAmount = returnSun(sunAmount, returningSunList, sunSpriteList) #we update the sunAmount value through the returnSun function
   
            display.flip() #updates the screen

            fpsClock.tick(30) #controls fps
            
quit() #close window

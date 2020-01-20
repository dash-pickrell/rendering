import pygame
import math
pygame.init()

# Coordinates for lines are stored as [x1, y1, x2, y2]
screen_x = 1000
screen_y = 1000

border_top = [0, 0, screen_x, 0]
border_right = [screen_x, 0, screen_x, screen_y]
border_bottom = [screen_x, screen_y, 0, screen_y]
border_left = [0, screen_y, 0, 0]

player_x = 500
player_y = 500
player_t = 0 # Angle of players view, going clockwise

wall_height = 10

map_x = 100
amp_y = 100

window = pygame.display.set_mode([screen_x, screen_y])

FOV = 90

clock = pygame.time.Clock()

running = True
while running:

    pygame.draw.polygon(window, (70, 140, 100), [(0, screen_y / 2), (screen_x, screen_y / 2), (screen_x, screen_y), (0, screen_y)]) # Draw floor

    # Check for quit
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_w]:
        move_t = player_t % 360
        player_x +=0.13* math.sin(math.radians(move_t))
        player_y -=0.13* math.cos(math.radians(move_t))
                
    if pressed[pygame.K_s]:
        move_t = (player_t + 180) % 360
        player_x +=0.13* math.sin(math.radians(move_t))
        player_y -=0.13* math.cos(math.radians(move_t))
                
    if pressed[pygame.K_a]:
        move_t = (player_t + 270) % 360
        player_x +=0.13* math.sin(math.radians(move_t))
        player_y -=0.13* math.cos(math.radians(move_t))
                
    if pressed[pygame.K_d]:
        move_t = (player_t + 90) % 360
        player_x +=0.13* math.sin(math.radians(move_t))
        player_y -=0.13* math.cos(math.radians(move_t))

    

    if player_x > map_x - 50:
        player_x = map_x - 50
        
    if player_x < 50:
        player_x = 50
        
    if player_y > map_y - 50:
        player_y = map_y - 50
        
    if player_y < 50:
        player_y = 50

        
    if pressed[pygame.K_LEFT]:
        player_t -= 1
                
    if pressed[pygame.K_RIGHT]:
        player_t += 1

    # print(str(player_x) + "     " + str(player_y))
            
    if player_t < 0:
        player_t += 360
    if player_t >= 360:
        player_t %= 360

    current_t = player_t - int(FOV / 2)
    if current_t < 0:
        current_t += 360
        
    # Find the angle to all the corners, (n)orth (e)ast (s)outh (w)est

    nw_t = 270 + math.degrees(math.atan(player_y / player_x))
    sw_t = 180 + math.degrees(math.atan(player_x / (screen_y - player_y)))
    se_t = 90 + math.degrees(math.atan((screen_y - player_y) / (screen_x - player_x)))
    ne_t = math.degrees(math.atan((screen_x - player_x) / player_y))

    # print(str(nw_t) + " " + str(sw_t) + " " + str(se_t) + " " + str(ne_t)  )
    # ray_count = 0
    # while ray_count < FOV:
    # ray_count += 1
    for ray_count in range(0, FOV):
        
        current_t += 1
        current_t %= 360

        angle = 90-current_t

        red = 190
        green = 190
        blue = 190

        # Find if the ray is perpendicular to the wall
        # print(str(nw_t) + " " + str(current_t))
        if current_t == 0 or current_t == 90 or current_t == 180 or current_t == 270:
  
            if current_t == 0:
                box_point_x = player_x
                box_point_y = 0
                red = 230
                green = 160
                blue = 160
                
            elif current_t == 90:
                box_point_x = screen_x
                box_point_y = player_y
                red = 230
                green = 230
                blue = 140
                
            elif current_t == 180:
                box_point_x = player_x
                box_point_y = screen_y
                red = 220
                green = 160
                blue = 160
                
            elif current_t == 270:
                box_point_x = 0
                box_point_y = player_y
                red = 160
                green = 160
                blue = 200

            else:
                print("Error plotting perpendicular endpoint on border")
                box_point_x = -1
                box_point_y = -1

        # Find if the ray goes to a corner

        elif current_t == nw_t or current_t == sw_t or current_t == se_t or current_t == ne_t:
            # print("hello")
            if current_t == nw_t:
                box_point_x = 0
                box_point_y = 0
                
            elif current_t == sw_t:
                box_point_x = 0
                box_point_y = screen_y
                
            elif current_t == se_t:
                box_point_x = screen_x
                box_point_y = screen_y
                
            elif current_t == ne_t:
                box_point_x = screen_x
                box_point_y = screen_y

            else:
                print("Error plotting corner endpoint on border")
                box_point_x = -1
                box_point_y = -1

        # Find what triangle the ray would go into

        elif (current_t > 0 and current_t < ne_t) or (current_t > ne_t and current_t < 90) or (current_t > 90 and current_t < se_t) or (current_t > se_t and current_t < 180) or (current_t > 180 and current_t < sw_t) or (current_t > sw_t and current_t < 270) or (current_t > 270 and current_t < nw_t) or (current_t > nw_t and current_t < 360):
            if current_t > 0 and current_t < ne_t:
                box_point_x = player_x + player_y * math.tan(math.radians(current_t))
                box_point_y = 0
                red = 230
                green = 160
                blue = 160
                # print(" 1st octant degrees is " + str(current_t) + "  x=" + str(box_point_x))
                
            elif current_t > ne_t and current_t < 90:
                box_point_x = screen_x
                box_point_y = player_y - math.tan(math.radians(angle)) * (screen_x - player_x)
                red = 230
                green = 230
                blue = 140
                
            elif current_t > 90 and current_t < se_t:
                box_point_x = screen_x
                box_point_y = player_y + math.tan(math.radians(angle)) * (screen_x - player_x)
                red = 230
                green = 230
                blue = 140
                
            elif current_t > se_t and current_t < 180:
                box_point_x = player_x + math.tan(math.radians(current_t)) * (screen_y - player_y)
                box_point_y = screen_y
                red = 220
                green = 160
                blue = 160
                
            elif current_t > 180 and current_t < sw_t:
                box_point_x = player_x - math.tan(math.radians(current_t)) * (screen_y - player_y)
                box_point_y = screen_y
                red = 220
                green = 160
                blue = 160
                
            elif current_t > sw_t and current_t < 270:
                box_point_x = 0
                box_point_y = player_y + math.tan(math.radians(angle)) * player_x
                red = 160
                green = 160
                blue = 200
            # print(str(angle) + " " + str(box_point_y) + " " + str(math.radians(angle))   + " " + str(math.tan(math.radians(angle)))     + " " + str(math.tan(math.radians(angle)) * player_x))
                
            elif current_t > 270 and current_t < nw_t:
                box_point_x = 0
                box_point_y = player_y + math.tan(math.radians(angle)) * player_x
                red = 160
                green = 160
                blue = 200
                
            elif current_t > nw_t and current_t < 360:
                box_point_x = player_x - player_y * math.tan(math.radians(current_t))
                box_point_y = 0
                red = 230
                green = 160
                blue = 160
                
            else:
                # print("Error finding border point along triangle")
                box_point_x = -1
                box_point_y = -1

        else:
            # print("Error finding point on border")
            box_point_x = -1
            box_point_y = -1

        if box_point_x != -1 and box_point_y != -1:
            box_point_distance = math.sqrt(((box_point_x - player_x) ** 2) + ((box_point_y - player_y) ** 2))
        else:
            box_point_distance = -1

        if box_point_distance != -1:
            line_height = 5 * math.degrees(math.atan(wall_height / box_point_distance))
        else:
            line_height = -1

        if current_t % 5 == 0:
            pass

            # print("current t, ht is " + str(current_t) + " " + str(box_point_distance) + ", " + str(line_height) + ", " + str(wall_height) + ", " + str(box_point_distance) + ", " + str(math.degrees(math.atan(wall_height / box_point_distance))))
        if line_height != -1:
            final_line = pygame.Rect((screen_x / FOV) * ray_count, (screen_y / 2) - int(line_height), screen_x / FOV + 1, (int(line_height) * 2))
            # print("current t is " + str(current_t))

            red = min(int((red / 1.5) + (line_height / 3)), 255)
            green = min(int((green / 1.5) + (line_height / 3)), 255)
            blue = min(int((blue / 1.5) + (line_height / 3)), 255)
            
            pygame.draw.rect(window, (red, green, blue), final_line)
            # pygame.draw.rect(window, (0, 0, int(line_height)), final_line)

            
            
    pygame.draw.circle(window, (0, 0, 0), (int(screen_x / 2), int(screen_y / 2)), 3, 1)
    
    pygame.display.flip()
    clock.tick(60)
    window.fill((255, 255, 255))
        




























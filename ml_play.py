class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass
        self.command=[0,0,0,0,0]
        
    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 45: # left bound  本來為65
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 585: # right bound  本來為565
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                   
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            speed_ahead = car["velocity"]
                            if y < 180:
                                
                                grid.add(5) 
                            if y<110:
                                grid.add(11)
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            #0左 1右
           
            if len(scene_info[self.player]) != 0:
                self.car_pos = scene_info[self.player]

            for car in scene_info["cars_info"]:
                if car["id"]==self.player_no:
                    self.car_vel = car["velocity"]
            self.car_lane = self.car_pos[0] // 70
            if self.player_no == 0:
                 print(self.car_pos[0])
                 print(grid)
            if len(grid) == 0:
                return ["SPEED"]
            
                
            else:
                if (11 in grid ) and (1 not in grid) and (4 not in grid) :
                        if self.car_vel < speed_ahead:
                            print("11speed","moveleft")
                            self.command.append(0)
                            return ["SPEED","MOVE_LEFT"]
                        else:
                            print("11brake","moveleft")
                            self.command.append(0)
                            return ["BRAKE","MOVE_LEFT"]
                elif (11 in grid ) and (3 not in grid) and (6 not in grid) :
                        if self.car_vel < speed_ahead:
                            if self.command[-2]!=1 and self.command[-3]!=1:
                                print("11speed","moveright")
                                self.command.append(1)
                                return ["SPEED","MOVE_RIGHT"]
                        else:
                            print("11brake","moveright")
                            self.command.append(1)
                            return ["BRAKE","MOVE_RIGHT"]
                elif (11 in grid) :
                        if self.car_vel > speed_ahead:    
                            print("11brake")
                            return ["BRAKE"]
              
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        if self.command[-2]!=1 and self.command[-3]!=1:
                           print("speed","moveleft2222")
                           self.command.append(0)
                           return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0] < self.lanes[self.car_lane]:
                        print("speed","moveright2222")
                        self.command.append(1)
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        print("speed222")
                        return ["SPEED"]
                else:
                    if (2 in grid) and  (3 in grid) and  (5 in grid) and  (6 in grid) and  (9 in grid) and (4 not in grid) and(1 not in grid) and self.lanes[self.car_lane]==595 :
                        print("moveleft 595","speed")
                        self.command.append(0)
                        return ["SPEED", "MOVE_LEFT"]
                    elif (2 in grid) and  (3 in grid) and  (5 in grid) and  (6 in grid) and  (9 in grid) and (4 not in grid) and self.lanes[self.car_lane]==595 :
                        print("moveleft 595")
                        self.command.append(0)
                        return [ "MOVE_LEFT"]
                    if (5 in grid): # NEED to BRAKE
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            if self.car_vel < speed_ahead:
                                if self.command[-2]!=1 and self.command[-3]!=1:
                                    self.command.append(0)         
                                    print("in 5 not 1 not 4 not 7","speed","moveleft")
                                    return ["SPEED", "MOVE_LEFT"]
                            else:
                                if self.command[-2]!=1 and self.command[-3]!=1:
                                    if self.car_vel < speed_ahead:
                                        self.command.append(0)
                                        print("moveleft")
                                        return ["MOVE_LEFT"]#保命
                                    else:
                                        self.command.append(0)
                                        print("moveleft")
                                        return ["MOVE_LEFT"]#保命
                        elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            if self.car_vel < speed_ahead:
                                self.command.append(1)         
                                print("in 5 not 3 not 6 not 9","speed","moveright")
                                return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("moveright")
                                return ["MOVE_RIGHT"]#保命
                        elif (1 not in grid) and (4 not in grid):
                             if self.car_vel < speed_ahead:
                                 if self.command[-2]!=1 and self.command[-3]!=1:
                                     self.command.append(0)         
                                     print("in 5 not 4","speed","moveleft")
                                     return ["SPEED", "MOVE_LEFT"]
                             else:
                                if self.command[-2]!=1 and self.command[-3]!=1:
                                    self.command.append(0)
                                    print("moveleft")
                                    return ["MOVE_LEFT"]#保命
                        elif (3 not in grid) and (6 not in grid):
                            if self.car_vel < speed_ahead:
                               self.command.append(1)         
                               print("in 5 not 6","speed","moveright")
                               return ["SPEED", "MOVE_RIGHT"]
                            else:
                                print("moveright")
                                return ["MOVE_RIGHT"]#保命
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                print("speed")
                                return ["SPEED"]
                            else:
                                print("brake")
                                return ["BRAKE"]
                    if (self.car_pos[0] < 35 ):
                        print("<35  speed  moveright")
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        if self.command[-2]!=1 and self.command[-3]!=1:
                            self.command.append(0)     
                            print("not 1 not4 not 7 speed","moveleft1111111000000")
                            return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        self.command.append(1)         
                        print("not 3 not6 not 9 speed","moveright1111")   
                        return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        if self.command[-2]!=1 and self.command[-3]!=1:
                            self.command.append(0)     
                            print("not 1 not4 speed","moveleft1111133")
                            return ["SPEED", "MOVE_LEFT"]
                    if (3 not in grid) and (6 not in grid): # turn right
                        self.command.append(1)     
                        print("not 3  not 6 speed","moveright111122")     
                        return ["SPEED", "MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid): # turn left 
                        if self.command[-2]!=1 and self.command[-3]!=1:
                            self.command.append(0)     
                            print("not 4 not 7 moveleft111144")
                            return ["MOVE_LEFT"]    
                    if (6 not in grid) and (9 not in grid): # turn right
                        self.command.append(1)     
                        print("not 6 not 9 moveright111155")   
                        return ["MOVE_RIGHT"]
                                
     

        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
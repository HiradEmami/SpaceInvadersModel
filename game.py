# Required Imports
import turtle
import os
import random as rd
import math
import time
import tkinter as tk
from tkinter import messagebox



__author__ = 'Hirad Emami Alagha - s3218139'
# http://nob.cs.ucdavis.edu/classes/ecs010-2014-02/handouts/turtle.html

#TODO: Loading Blocks
#TODO: Leaderboard

class game:
    def __init__(self, argTrial=False):
        # Primary vars
        self.main_frame = None
        self.player = None
        self.enemies = []
        self.bullets = []
        self.enemy_dic = None
        # Initial colors
        self.player_color = 'red'
        self.background_color = 'black'
        self.boarder_color = 'Red'
        # Player - Enemy Speed
        self.player_speed = 15 # Relatively fast
        self.minion_speed_x = 2 # Relatively slow
        self.minion_speed_y = 2
        self.bullet_speed = 50
        self.minion_shape_size_x = 1
        self.minion_shape_size_y = 1
        # difficulty
        self.num_enemies = 2000
        self.num_batch = 3
        # Spawn timer is based on seconds
        self.frame_rate = 0.05
        self.spawn_timer = 5
        self.spawn_timer *= 1/self.frame_rate
        # player info
        self.num_bullets = 5
        self.player_hp = 5
        self.health_turtules = []
        self.hit_threshold = 35
        self.auto_shoot = False
        self.upgrade_point_required = 500
        self.upgade_cycle_point = self.upgrade_point_required
        self.upgrade_allowed = True
        # Player Score
        self.score = 0
        # state-machines
        #   Bullet_states are either ready (meaning ready to fire)  or fire (meaning is already used)
        self.bullet_state = "ready"
        #   Game_state is either "running" , "finished" , "initialized"
        self.game_state = "initialized"
        self.pause = False
        self.pause_duration_second = 5
        # Varriables for response time
        self.after_pause_time = None
        self.first_action_time = None
        self.listen_for_action = False
        self.response_recordings = []

        # Gun configuration
        self.gun_modes = ["xs","s","m","l","xl"]
        self.current_gun_mode = 0
        # Register the icons
        turtle.register_shape("spaceShip/ship_l.gif")
        turtle.register_shape("spaceShip/ship_xl.gif")
        turtle.register_shape("spaceShip/ship_m.gif")
        turtle.register_shape("spaceShip/ship_xs.gif")
        turtle.register_shape("spaceShip/ship_s.gif")
        turtle.register_shape("spaceShip/heart_damaged.gif")
        turtle.register_shape("spaceShip/heart_full.gif")
        # create the health
        self.spawn_health_turtules()
        # set the difficulty and the settings
        if argTrial:
            self.trial_difficulty = "Easy"
            self.set_tial_difficulty()
        else:
            # todo: this should change to improt blocks
            self.trial_difficulty = "Hard"
            self.set_tial_difficulty()
            self.game_current_stage = 0

    def set_pause_duration(self,duration_seconds):
        self.pause_duration_second = duration_seconds

    def set_stage_difficulty_level(self):
        print("to be implemented")

    def set_tial_difficulty(self):
        # add the most basic enemy type to the dictionary
        self.enemy_dic = [{"color": "blue", "shape": "circle", "moveset": 1}]
        if self.trial_difficulty == "Easy":
            self.minion_shape_size_x = 2
            self.minion_shape_size_y = 2
        elif self.trial_difficulty == "Medium":
            self.enemy_dic.append({"color": "yellow", "shape": "square", "moveset": 2})
            self.minion_speed_x += 5
            self.minion_speed_y += 5
            self.minion_shape_size_x = 1.5
            self.minion_shape_size_y = 1.5
            self.num_batch += 3
        elif self.trial_difficulty == "Hard":
            self.enemy_dic.append({"color": "yellow", "shape": "square", "moveset": 2})
            self.enemy_dic.append({"color": "red", "shape": "triangle", "moveset": 3})
            self.minion_speed_x += 12
            self.minion_speed_y += 12
            self.minion_shape_size_x = 1
            self.minion_shape_size_y = 1
            self.num_batch += 3




    def quit_game(self):
        result = messagebox.askquestion("Quit", "You are about to quit the game! Are You Sure?", icon='warning')
        if result == 'yes':
            print
            self.game_state = "finished"
            print("The game has ended")
        else:
            print("I'm Not Done Yet")


    def euclidean_distance(self,x1,x2,y1,y2):
        deltaX = math.pow((x2-x1),2)
        deltaY = math.pow((y2-y1),2)
        distance = math.sqrt(deltaX+deltaY)
        return distance

    @staticmethod
    def draw_boarders():
        border_pen = turtle.Turtle()
        border_pen.speed(0)
        border_pen.color('black')
        border_pen.penup()
        border_pen.setposition(-300, 300)
        border_pen.pendown()
        border_pen.pensize(4)
        for edge in range(4):
            border_pen.fd(600)
            border_pen.right(90)

        border_pen.hideturtle()

    def draw_base_line(self):
        border_pen = turtle.Turtle()
        border_pen.speed(0)
        border_pen.color('black')
        border_pen.penup()
        border_pen.setposition(-290, -285)
        border_pen.pendown()
        border_pen.pensize(4)
        border_pen.fd(580)
        border_pen.penup()
        border_pen.setposition(-290, -215)
        border_pen.pendown()
        border_pen.pensize(4)
        border_pen.fd(580)
        border_pen.hideturtle()

    def draw_score(self):
        # Draw the score
        self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color("black")
        self.score_pen.penup()
        self.score_pen.setposition(-280, 270)
        self.scorestring = "Score: %s" % self.score
        self.score_pen.write(self.scorestring, False, align="left", font=("Arial", 14, "normal"))
        self.score_pen.hideturtle()


    def draw_game_progression(self):
        # Draw the score
        self.game_state_pen = turtle.Turtle()
        self.game_state_pen.speed(0)
        self.game_state_pen.color("red")
        self.game_state_pen.penup()
        self.game_state_pen.setposition(+310, 280)
        self.update_status_view()
        self.game_state_pen.hideturtle()

    def update_status_view(self):
        self.game_state_pen.clear()
        if self.pause:
            self.status_report = "Paused!"
            self.game_state_pen.write(self.status_report, False, align="left", font=("Arial", 14, "normal"))
        else:
            self.status_report = "Stage: %s" % (self.game_current_stage + 1)
            self.game_state_pen.write(self.status_report, False, align="left", font=("Arial", 14, "normal"))

    def update_score_view(self):
        scorestring = "Score: %s" % self.score
        self.score_pen.clear()
        self.score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

    def spwan_player(self):
        self.player = turtle.Turtle()
        self.player.color(self.player_color)
        self.set_player_ship()
        self.player.penup()
        self.player.speed(0)
        self.player.setposition(0,-250)
        self.player.setheading(90)

    def upgrade_player(self):
        if not self.current_gun_mode >= 4:
            self.current_gun_mode +=1
            self.set_player_ship()
            self.upgrade_gun()

        if len(self.bullets) == 5:
            self.upgrade_allowed = False

    def upgrade_gun(self):
        self.bullet_speed += 1
        self.hit_threshold += 25
        new_bullet = self.create_bullet()
        self.bullets.append(new_bullet)
        self.arrange_bullets()

    def fire_bullet(self):
        if self.bullet_state == "ready":
            self.bullet_state  = "fire"
            # reset the bullets
            self.arrange_bullets()
            self.bullet_exit = False

            if self.listen_for_action:
                self.record_response()


    def arrange_bullets(self):
        x = self.player.xcor()
        y = self.player.ycor() + 15

        if len(self.bullets) ==1:
            self.bullets[0].setposition(x, y)
        elif len(self.bullets) == 2:
            self.bullets[0].setposition(x-20, y)
            self.bullets[1].setposition(x+20, y)
        elif len(self.bullets) == 3:
            self.bullets[0].setposition(x-20, y)
            self.bullets[1].setposition(x+20, y)
            self.bullets[2].setposition(x , y)
        elif len(self.bullets) == 4:
            self.bullets[0].setposition(x-20, y)
            self.bullets[1].setposition(x+20, y)
            self.bullets[2].setposition(x + 30, y)
            self.bullets[3].setposition(x - 30, y)
        elif len(self.bullets) == 5:
            self.bullets[0].setposition(x-20, y)
            self.bullets[1].setposition(x+20, y)
            self.bullets[2].setposition(x + 30, y)
            self.bullets[3].setposition(x - 30, y)
            self.bullets[4].setposition(x , y)

        for i in self.bullets:
            i.showturtle()

    def hit_target(self,argBullet, argEnemy):
        distance = self.euclidean_distance(self.player.xcor(),argEnemy.xcor(),
                                           argBullet.ycor(),argEnemy.ycor())
        if distance < self.hit_threshold:
            return True
        else:
            return False

    def set_player_ship(self):
        shape = "spaceShip/ship_"+self.gun_modes[self.current_gun_mode]+".gif"
        self.player.shape(shape)
        self.player.shapesize(0.5,0.5)

    def move_left_player(self):
        x = self.player.xcor()
        x -= self.player_speed
        if x < -290:
            x = -290
        self.player.setx(x)

        if self.listen_for_action:
            self.record_response()

    def move_right_player(self):
        x = self.player.xcor()
        x += self.player_speed
        if x > 290:
            x = 290
        self.player.setx(x)

        if self.listen_for_action:
            self.record_response()

    def move_right_minion(self,argMinion):
        x = argMinion.xcor()
        x += self.minion_speed_x
        if x > 280:
            self.move_left_minion(argMinion)
        else:
            argMinion.setx(x)

    def move_left_minion(self,argMinion):
        x = argMinion.xcor()
        x -= self.minion_speed_x
        if x < -280:
            self.move_right_minion(argMinion)
        else:
            argMinion.setx(x)

    def move_up_minion(self,argMinion):
        y = argMinion.ycor()
        y += self.minion_speed_y
        if y > 280:
            y = 280
        argMinion.sety(y)

    def move_down_minion(self,argMinion):
        y = argMinion.ycor()
        y -= self.minion_speed_y
        if y < -280:
            y = -280
        argMinion.sety(y)

    def record_response(self):
        self.first_action_time = time.time()
        duration = self.first_action_time - self.after_pause_time
        self.response_recordings.append(duration)
        print("\nResponse Time:     \t{:.1f}".format(duration) + " s")
        self.listen_for_action = False


    def move_down_left(self,argMinion):
        self.move_left_minion(argMinion)
        self.move_down_minion(argMinion)

    def move_down_right(self,argMinion):
        self.move_right_minion(argMinion)
        self.move_down_minion(argMinion)

    def move_up_left(self, argMinion):
        self.move_left_minion(argMinion)
        self.move_up_minion(argMinion)

    def move_up_right(self, argMinion):
        self.move_right_minion(argMinion)
        self.move_up_minion(argMinion)

    def cheat_upgrade(self):
        self.upgrade_player()

    def move_set_one(self,minion,direction):
        x = minion.xcor()
        x -= (direction*self.minion_speed_x)
        minion.setx(x)

        if x > 280 or x < -280:
            direction *= -1
            y = minion.ycor()
            y -= 40
            minion.sety(y)

        return direction

    def move_set_two(self,minion,direction):
        x = minion.xcor()
        x += (direction * self.minion_speed_x)
        minion.setx(x)

        if x > 280 or x < -280:
            direction *= -1
            y = minion.ycor()
            y -= 50
            minion.sety(y)

        return direction

    def move_set_three(self,minion,direction):
        x = minion.xcor()
        lef_right_proc =rd.uniform(0,1)
        x = minion.xcor()
        x += (direction * self.minion_speed_x)
        if lef_right_proc>0.9:
            x += rd.randint(-50,50)


        if x > 280 or x < -280:
            direction *= -1
            y = minion.ycor()
            y -= 50
            minion.sety(y)

        if x > 280:
            x = 280
        elif x < -280:
            x = -280

        minion.setx(x)

        return direction

    def create_bullet(self):
        # Create the player's bullet
        bullet = turtle.Turtle()
        bullet.color("yellow")
        bullet.shape("triangle")
        bullet.penup()
        bullet.speed(0)
        bullet.setheading(90)
        bullet.shapesize(0.5, 0.5)
        bullet.hideturtle()
        return bullet

    def create_health_turtule(self):
        # Create the player's bullet
        health = turtle.Turtle()
        shape_full = "spaceShip/heart_full.gif"
        health.shape(shape_full)
        health.penup()
        health.speed(0)
        return health

    def spawn_health_turtules(self):
        x_counter = -280
        for i in range(self.player_hp):
            health = self.create_health_turtule()
            health.setposition(x_counter, -330)
            x_counter += 30
            self.health_turtules.append(health)

    def update_player_health(self):
        for i in range(self.player_hp):
            self.health_turtules[i].shape("spaceShip/heart_full.gif")
        if not self.player_hp ==5:
            for j in range(self.player_hp - 1, len(self.health_turtules)):
                self.health_turtules[j].shape("spaceShip/heart_damaged.gif")



    def minion_perform_action(self,minion):
        if minion[0].isvisible():
            if minion[1]==1:
                minion[2]=self.move_set_one(minion[0],direction=minion[2])
            elif minion[1]==2:
                minion[2]=self.move_set_two(minion[0],direction=minion[2])
            elif minion[1]==3:
                minion[2] = self.move_set_three(minion[0], direction=minion[2])

    def generate_minion(self):
        selection = rd.randint(0,len(self.enemy_dic)-1)
        color = self.enemy_dic[selection].get("color")
        shape = self.enemy_dic[selection].get("shape")
        move_pattern = self.enemy_dic[selection].get("moveset")
        minion = turtle.Turtle()
        minion.color(color)
        minion.shape(shape)
        minion.shapesize(self.minion_shape_size_x ,self.minion_shape_size_y)
        minion.penup()
        minion.speed(0)
        x = rd.randint(-280,280)
        y = 280
        minion.setposition(x,y)
        direction = 1
        return  [minion,move_pattern,direction]

    def spawn_new_enemy_row(self):
        for i in range(self.num_batch):
            minion = self.generate_minion()
            self.enemies.append(minion)
        self.num_enemies -= self.num_batch

    def toggle_auto_shoot(self):
        if self.auto_shoot:
            self.auto_shoot = False
        else:
            self.auto_shoot = True
        
    def toggle_pause(self):
        if self.pause:
            self.pause = False
        else:
            self.pause = True
            self.update_status_view()
            print("Game Paused")

    def run(self):
        #   First create the Window
        self.main_frame = turtle.Screen()
        self.main_frame.bgcolor(self.background_color)
        self.main_frame.bgpic("spaceShip/new_backGround.gif")
        self.main_frame.title('Evil Geometry Invaders')
        self.main_frame.setup(width=1.0, height=1.0, startx=None, starty=None)
        self.main_frame.tracer(0,delay=0)
        #   Draw the Boarders
        self.draw_boarders()
        self.draw_base_line()
        self.draw_score()
        self.draw_game_progression()
        #   Spawn the Player
        self.spwan_player()
        #   Generate enemies
        self.spawn_new_enemy_row()
        #   Create the starting bullet
        bullet = self.create_bullet()
        self.bullets.append(bullet)
        self.arrange_bullets()
        #   Setting the Controls
        turtle.onkeypress(self.move_left_player,"a")
        turtle.onkeypress(self.move_right_player, "d")
        turtle.onkey(self.move_left_player, "Left")
        turtle.onkey(self.move_right_player, "Right")
        turtle.onkey(self.fire_bullet, "space")
        turtle.onkey(self.quit_game, "q")
        # dev mode keys
        turtle.onkey(self.cheat_upgrade, "u")
        turtle.onkey(self.toggle_auto_shoot,"i")
        turtle.onkey(self.toggle_pause, "p")

        turtle.listen()
        spawn_counter = 0
        self.game_state = "running"
        self.main_frame.update()
        while self.game_state=="running":
            if not self.pause:
                spawn_counter += 1
                spawn_counter = self.performe_one_move_cycle(spawn_counter)
                time.sleep(self.frame_rate)
                self.main_frame.update()
            else:
                time.sleep(self.pause_duration_second)
                print("Resumed")
                self.after_pause_time = time.time()
                self.listen_for_action = True
                self.pause = False
                self.update_status_view()

           #self.main_frame.delay(15)
           #self.main_frame.update()

        #turtle.mainloop()

    def performe_one_move_cycle(self,counter):
        if counter >= self.spawn_timer:
            counter = 0
            self.spawn_new_enemy_row()
        if not self.player_hp > 0 or self.num_enemies <= 0:
            self.game_state = "finished"
            print("the Game Ended")
        temp = -1
        for i in self.enemies:
            temp += 1
            if i[0].isvisible() and self.bullets[0].isvisible:
                self.minion_perform_action(i)
                minion_y = i[0].ycor()
                if self.hit_target(argEnemy=i[0], argBullet=self.bullets[0]):
                    i[0].hideturtle()
                    # Update the score
                    self.score += (i[1] * 10)
                    self.update_score_view()
                    if self.score  >= self.upgrade_point_required and self.upgrade_allowed:
                        self.upgrade_point_required += self.upgade_cycle_point
                        self.upgrade_player()
                elif minion_y <= -215:
                    i[0].hideturtle()
                    self.player_hp -= 1
                    self.update_player_health()
                    print("player lost health... down to "+str(self.player_hp))

        if self.bullet_state == "fire":
            for i in self.bullets:
                new_y = i.ycor()
                new_y += self.bullet_speed
                i.sety(new_y)

        if self.bullets[0].ycor() > 290:

            self.arrange_bullets()
            if not self.auto_shoot:
                self.bullet_state = "ready"
            else:
                self.bullet_state = "fire"

        return counter

if __name__ == '__main__':
    game = game()
    game.run()
from kandinsky import *
from ion import *
from kandinsky import *
from math import *

def circle(x0, y0, r, c, t):
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        set_pixel(x0 + x, y0 + y, c)
        set_pixel(x0 - x, y0 + y, c)
        set_pixel(x0 + x, y0 - y, c)
        set_pixel(x0 - x, y0 - y, c)
        set_pixel(x0 + y, y0 + x, c)
        set_pixel(x0 - y, y0 + x, c)
        set_pixel(x0 + y, y0 - x, c)
        set_pixel(x0 - y, y0 - x, c)

        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
    if t > 1:
        for i in range(t):
            x = 0
            y = r + i
            d = i
            while x <= y:
                set_pixel(x0 + x, y0 + y, c)
                set_pixel(x0 - x, y0 + y, c)
                set_pixel(x0 + x, y0 - y, c)
                set_pixel(x0 - x, y0 - y, c)
                set_pixel(x0 + y, y0 + x, c)
                set_pixel(x0 - y, y0 + x, c)
                set_pixel(x0 + y, y0 - x, c)
                set_pixel(x0 - y, y0 - x, c)

                x += 1
                if d < 0:
                    d += 2 * x + 1
                else:
                    y -= 1
                    d += 2 * (x - y) + 1

class ShopItem:
    def __init__(self, name, count, price, cps):
        self.name = name
        self.count = count
        self.price = price
        self.cps = cps
        
finger = ShopItem("finger", 0, 5, 1)
granny = ShopItem("granny", 0, 50, 5)
farm = ShopItem("farm", 0, 100, 15)

score = 0
keylock_click = False
keylock_down = False
keylock_up = False
keylock_buy = False
shop_selected = 1
refresh_score = True
ticks_since_last_cps = 0


draw_string(str(score),75,55)
circle(80,130,40,color("black"),4)

def show_score():
   score_string_length = len(str(score))
   score_positionX = 80 - (score_string_length * 5)
   fill_rect(0,55,149,15,color("white"))
   draw_string(str(score),score_positionX,55)

def show_shop_item(name, count, price, cps, rank):
    cps_string = str(cps) + "c/ps"
    price_string = "$" + str(price)
    if shop_selected == rank:
        for i in range(150):
            set_pixel(i+150,rank*50-25,color("red"))
            set_pixel(i+150,rank*50+25,color("red"))
        for i in range(50):
            set_pixel(150,i+rank*50-25,color("red"))
            set_pixel(300,i+rank*50-25,color("red"))
        draw_string(name,155,rank*50-20,color("red"))
        draw_string(str(count),155,rank*50+1,color("red"))
        draw_string(price_string,295-len(price_string)*10,rank*50-20,color("red"))
        draw_string(cps_string,295-len(cps_string)*10,rank*50+1,color("red"))
    else:
        for i in range(150):
            set_pixel(i+150,rank*50-25,color("black"))
            set_pixel(i+150,rank*50+25,color("black"))
        for i in range(50):
            set_pixel(150,i+rank*50-25,color("black"))
            set_pixel(300,i+rank*50-25,color("black"))
        draw_string(name,155,rank*50-20)
        draw_string(str(count),155,rank*50+1)
        draw_string(price_string,295-len(price_string)*10,rank*50-20)
        draw_string(cps_string,295-len(cps_string)*10,rank*50+1)

def refresh_shop():
    show_shop_item(farm.name, farm.count, farm.price, farm.cps, 3)
    show_shop_item(granny.name, granny.count, granny.price, granny.cps, 2)
    show_shop_item(finger.name, finger.count, finger.price, finger.cps, 1)
    
def refresh_shop_element(item_rank):
    if item_rank == 1:
        show_shop_item(finger.name, finger.count, finger.price, finger.cps, 1)
    elif item_rank == 2:
        show_shop_item(granny.name, granny.count, granny.price, granny.cps, 2)
    elif item_rank == 3:
        show_shop_item(farm.name, farm.count, farm.price, farm.cps, 3)

refresh_shop()

def add_items_score():
    global score, refresh_score
    score += finger.count * finger.cps + granny.count * granny.cps + farm.count * farm.cps
    refresh_score = True
    
    
while True:
    ticks_since_last_cps = ticks_since_last_cps + 1
    if keydown(KEY_OK) and not keylock_click:
        score = score + 1
        keylock_click = True
        refresh_score = True
        circle(80,130,40,color("white"),4)
        circle(80,130,30,color("black"),3)
    if not keydown(KEY_OK) and keylock_click:
        keylock_click = False
        circle(80,130,30,color("white"),3)
        circle(80,130,40,color("black"),4)
    if keydown(KEY_DOWN) and not keylock_down and shop_selected < 3:
       shop_selected = shop_selected + 1
       refresh_shop_element(shop_selected - 1)
       refresh_shop_element(shop_selected)
       keylock_down = True
    if not keydown(KEY_DOWN) and keylock_down:
         keylock_down = False
    if keydown(KEY_UP) and not keylock_up and shop_selected > 1:
       shop_selected = shop_selected - 1
       refresh_shop_element(shop_selected + 1)
       refresh_shop_element(shop_selected)
       keylock_up = True
    if not keydown(KEY_UP) and keylock_up:
         keylock_up = False 
    if keydown(KEY_EXE) and not keylock_buy:
        if shop_selected == 1 and score >= finger.price:
            score = score - finger.price
            finger.count = finger.count + 1
            finger.price = ceil(finger.price * 1.15)
            refresh_shop_element(1)
            refresh_score = True
        elif shop_selected == 2 and score >= granny.price:
            score = score - granny.price
            granny.count = granny.count + 1
            granny.price = ceil(granny.price * 1.15)
            refresh_shop_element(2)
            refresh_score = True
        elif shop_selected == 3 and score >= farm.price:
            score = score - farm.price
            farm.count = farm.count + 1
            farm.price = ceil(farm.price * 1.15)
            refresh_shop_element(3)
            refresh_score = True
        keylock_buy = True
    if not keydown(KEY_EXE) and keylock_buy:
        keylock_buy = False
    if ticks_since_last_cps >= 100:
        # Need to decrease this if running in an emulator
        add_items_score()
        ticks_since_last_cps = 0
    if refresh_score:
        show_score()
        refresh_score = False
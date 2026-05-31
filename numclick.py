import kandinsky as k
import ion as i
import math as m

def circle(x0, y0, r, c, t):
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        k.set_pixel(x0 + x, y0 + y, c)
        k.set_pixel(x0 - x, y0 + y, c)
        k.set_pixel(x0 + x, y0 - y, c)
        k.set_pixel(x0 - x, y0 - y, c)
        k.set_pixel(x0 + y, y0 + x, c)
        k.set_pixel(x0 - y, y0 + x, c)
        k.set_pixel(x0 + y, y0 - x, c)
        k.set_pixel(x0 - y, y0 - x, c)

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
                k.set_pixel(x0 + x, y0 + y, c)
                k.set_pixel(x0 - x, y0 + y, c)
                k.set_pixel(x0 + x, y0 - y, c)
                k.set_pixel(x0 - x, y0 - y, c)
                k.set_pixel(x0 + y, y0 + x, c)
                k.set_pixel(x0 - y, y0 + x, c)
                k.set_pixel(x0 + y, y0 - x, c)
                k.set_pixel(x0 - y, y0 - x, c)

                x += 1
                if d < 0:
                    d += 2 * x + 1
                else:
                    y -= 1
                    d += 2 * (x - y) + 1

class ShopItem:
    def __init__(self, name, count, price, cps, mult):
        self.name = name
        self.count = count
        self.price = price
        self.cps = cps
        self.mult = mult

finger = ShopItem("finger", 0, 5, 1, 1.15)
granny = ShopItem("granny", 0, 50, 5, 1.15)
farm = ShopItem("farm", 0, 100, 15, 1.15)

score = 0
keylock_click = False
keylock_down = False
keylock_up = False
keylock_buy = False
shop_selected = 1
refresh_score = True
last_cps_tick = 0
ticks = 0


k.draw_string(str(score),75,55)
circle(80,130,40,k.color("black"),4)

def show_score():
   score_string_length = len(str(score))
   score_positionX = 80 - (score_string_length * 5)
   k.fill_rect(0,55,149,15,k.color("white"))
   k.draw_string(str(score),score_positionX,55)

def show_shop_item(name, count, price, cps, rank):
    cps_string = str(cps) + "c/ps"
    price_string = "$" + str(price)
    if shop_selected == rank:
        for i in range(150):
            k.set_pixel(i+150,rank*50-25,k.color("red"))
            k.set_pixel(i+150,rank*50+25,k.color("red"))
        for i in range(50):
            k.set_pixel(150,i+rank*50-25,k.color("red"))
            k.set_pixel(300,i+rank*50-25,k.color("red"))
        k.draw_string(name,155,rank*50-20,k.color("red"))
        k.draw_string(str(count),155,rank*50+1,k.color("red"))
        k.draw_string(price_string,295-len(price_string)*10,rank*50-20,k.color("red"))
        k.draw_string(cps_string,295-len(cps_string)*10,rank*50+1,k.color("red"))
    else:
        for i in range(150):
            k.set_pixel(i+150,rank*50-25,k.color("black"))
            k.set_pixel(i+150,rank*50+25,k.color("black"))
        for i in range(50):
            k.set_pixel(150,i+rank*50-25,k.color("black"))
            k.set_pixel(300,i+rank*50-25,k.color("black"))
        k.draw_string(name,155,rank*50-20)
        k.draw_string(str(count),155,rank*50+1)
        k.draw_string(price_string,295-len(price_string)*10,rank*50-20)
        k.draw_string(cps_string,295-len(cps_string)*10,rank*50+1)

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
    ticks = ticks+1
    if i.keydown(i.KEY_OK) and not keylock_click:
        score = score + 1
        keylock_click = True
        refresh_score = True
        circle(80,130,40,k.color("white"),4)
        circle(80,130,30,k.color("black"),3)
    if not i.keydown(i.KEY_OK) and keylock_click:
        keylock_click = False
        circle(80,130,30,k.color("white"),3)
        circle(80,130,40,k.color("black"),4)
    if i.keydown(i.KEY_DOWN) and not keylock_down and shop_selected < 3:
       shop_selected = shop_selected + 1
       refresh_shop_element(shop_selected - 1)
       refresh_shop_element(shop_selected)
       keylock_down = True
    if not i.keydown(i.KEY_DOWN) and keylock_down:
         keylock_down = False
    if i.keydown(i.KEY_UP) and not keylock_up and shop_selected > 1:
       shop_selected = shop_selected - 1
       refresh_shop_element(shop_selected + 1)
       refresh_shop_element(shop_selected)
       keylock_up = True
    if not i.keydown(i.KEY_UP) and keylock_up:
         keylock_up = False 
    if i.keydown(i.KEY_EXE) and not keylock_buy:
        if shop_selected == 1 and score >= finger.price:
            score = score - finger.price
            finger.count = finger.count + 1
            finger.price = m.ceil(finger.price * finger.mult)
            refresh_shop_element(1)
            refresh_score = True
            if finger.mult > 1.2:
                finger.mult = finger.mult - 0.05
        elif shop_selected == 2 and score >= granny.price:
            score = score - granny.price
            granny.count = granny.count + 1
            granny.price = m.ceil(granny.price * granny.mult)
            refresh_shop_element(2)
            refresh_score = True
            if granny.mult > 1.2:
                granny.mult = granny.mult - 0.05
        elif shop_selected == 3 and score >= farm.price:
            score = score - farm.price
            farm.count = farm.count + 1
            farm.price = m.ceil(farm.price * farm.mult)
            refresh_shop_element(3)
            refresh_score = True
            if farm.mult > 1.2:
                farm.mult = farm.mult - 0.05
        keylock_buy = True
    if not i.keydown(i.KEY_EXE) and keylock_buy:
        keylock_buy = False
    if ticks - last_cps_tick >= 100:
        # Need to decrease this if running in an emulator
        add_items_score()
        last_cps_tick = ticks
    if refresh_score:
        show_score()
        refresh_score = False
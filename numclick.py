import kandinsky as k
import ion as i
import math as m
import random as r

class ShopItem:
    # Class to represent an item in the shop
    def __init__(self, name, count, price, cps, mult):
        self.name = name
        self.count = count
        self.price = price
        self.cps = cps
        self.mult = mult

finger = ShopItem("finger", 0, 5, 1, 1.15)
granny = ShopItem("granny", 0, 50, 5, 1.15)
farm = ShopItem("farm", 0, 100, 15, 1.15)


# Variables related to the score
score = 0
refresh_score = True

# Variables related to the "keylock"
# Keylock is a system to prevent multiple actions from a single key press
keylock_click = False
keylock_down = False
keylock_up = False
keylock_buy = False

# Variables related to the shop
shop_selected = 1

# Variables related to ticks
# Ticks is a system to keep track of time in the game, by counting the number of iterations of the main loop
last_cps_tick = 0
ticks = 0

# Variables related to the golden touch
# The golden touch is a random event that gives the player a random multiplier to their score if they press the correct button in time
golden_touch_active = False
golden_touch_timer = r.randint(500, 1000)
golden_touch_buttons = [i.KEY_ZERO, i.KEY_ONE, i.KEY_TWO, i.KEY_THREE, i.KEY_FOUR, i.KEY_FIVE, i.KEY_SIX, i.KEY_SEVEN, i.KEY_EIGHT, i.KEY_NINE]
last_golden_touch = 0

# Used to show the score at the correct position and to clear the previous score
def show_score():
   score_string_length = len(str(score))
   score_positionX = 80 - (score_string_length * 5)
   k.fill_rect(0,55,149,15,k.color("white"))
   k.draw_string(str(score),score_positionX,55)

# Midpoint circle algorithm
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

# Used to show every shop items, calculating the position of everything based on the "rank" (the position of the item in the shop, from top to bottom)
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

# Used to refresh the whole shop
# You probably don't want to use that, it's better to use refresh_shop_element because this one can create some bugs
def refresh_shop():
    show_shop_item(farm.name, farm.count, farm.price, farm.cps, 3)
    show_shop_item(granny.name, granny.count, granny.price, granny.cps, 2)
    show_shop_item(finger.name, finger.count, finger.price, finger.cps, 1)

# Used to refresh only one element of the shop, based on the "rank"
def refresh_shop_element(item_rank):
    if item_rank == 1:
        show_shop_item(finger.name, finger.count, finger.price, finger.cps, 1)
    elif item_rank == 2:
        show_shop_item(granny.name, granny.count, granny.price, granny.cps, 2)
    elif item_rank == 3:
        show_shop_item(farm.name, farm.count, farm.price, farm.cps, 3)

# Used to add the score generated by the items
def add_items_score():
    global score, refresh_score
    score += finger.count * finger.cps + granny.count * granny.cps + farm.count * farm.cps
    refresh_score = True

# Used to generate a golden touch event, which gives the player a random multiplier to their score if they press the correct button in time
def golden_touch():
    global golden_button, golden_touch_active, last_golden_touch
    button_names = {
    i.KEY_ZERO: "0",
    i.KEY_ONE: "1",
    i.KEY_TWO: "2",
    i.KEY_THREE: "3",
    i.KEY_FOUR: "4",
    i.KEY_FIVE: "5",
    i.KEY_SIX: "6",
    i.KEY_SEVEN: "7",
    i.KEY_EIGHT: "8",
    i.KEY_NINE: "9"
    }
    golden_button = r.choice(golden_touch_buttons)
    k.draw_string("Press " + button_names[golden_button] + "!", 50, 200, k.color("red"))
    golden_touch_active = True
    last_golden_touch = ticks

show_score()
circle(80,130,40,k.color("black"),4)
refresh_shop()

# Main loop
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
    if ticks - last_golden_touch >= golden_touch_timer and not golden_touch_active:
        golden_touch()
    if golden_touch_active and i.keydown(golden_button):
        score = score * r.randint(2,5)
        k.fill_rect(0,200,145,15,k.color("white"))
        refresh_score = True
        golden_touch_active = False
        golden_touch_timer = r.randint(500, 1000)
        last_golden_touch = ticks
    if golden_touch_active and ticks - last_golden_touch >= 500:
        golden_touch_active = False
        k.fill_rect(0,200,145,15,k.color("white"))
        last_golden_touch = ticks
        golden_touch_timer = r.randint(500, 1000)
    if refresh_score:
        show_score()
        refresh_score = False
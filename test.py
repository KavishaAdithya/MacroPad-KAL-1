import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus

import adafruit_displayio_ssd1306


displayio.release_displays()

i2c = busio.I2C(scl=board.GP13,sda=board.GP12)

display_bus = I2CDisplayBus(i2c,device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus,width = 128,height = 64)



        
        
def key_bindings(box):
    
    splash = displayio.Group()
    display.root_group = splash


    color_bitmap = displayio.Bitmap(128,64,1)
    color_palette = displayio.Palette(1)

    color_palette[0] = 0xFFFFFF

    bg_sprite = displayio.TileGrid(color_bitmap,pixel_shader=color_palette,x=0,y=0)
    splash.append(bg_sprite)



    for i in range(3):
        for j in range(3):
            box_1_bitmap= displayio.Bitmap(40,20,1)
            box_1_color = displayio.Palette(1)

            box_1_color[0] = 0x000000

            box_1 = displayio.TileGrid(box_1_bitmap,pixel_shader=box_1_color,x=44*i,y=24*j)
            splash.append(box_1)
    
    
    
    k=0
    
    for j in range(3):
        for i in range(3):
            text_area = label.Label(terminalio.FONT,text=box[k],color=0xFFFFFF,x=44*i+5,y=24*j+8)
            k = k+1
            splash.append(text_area)
        
    
    
    





 
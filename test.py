import busio
import adafruit_displayio_ssd1306
import board
import displayio
import adafruit_imageload
from adafruit_display_text import label
import terminalio



displayio.release_displays()

i2c = busio.I2C(scl=board.GP1,sda=board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(display_bus,width =128,height=64)

def display_Header(pc,mic,speaker_mute,speaker_unmute,text1):
    bitmap1,palette1 = adafruit_imageload.load("/monitor.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
    bitmap2,palette2 = adafruit_imageload.load("/Link.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
    bitmap3,palette3 = adafruit_imageload.load("/unmute.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
    bitmap4,palette4 = adafruit_imageload.load("/mute.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
    bitmap5,palette5 = adafruit_imageload.load("/mic.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)

    tile_grid1 = displayio.TileGrid(bitmap1,pixel_shader = palette1,x=0,y=1)
    tile_grid2 = displayio.TileGrid(bitmap2,pixel_shader = palette2,x=20,y=1)
    tile_grid3 = displayio.TileGrid(bitmap3,pixel_shader = palette2,x=39,y=1)
    tile_grid4 = displayio.TileGrid(bitmap4,pixel_shader = palette2,x=39,y=1)
    tile_grid5 = displayio.TileGrid(bitmap5,pixel_shader = palette2,x=60,y=1)

    text = "KAL.v1"
    

    text_area = label.Label(terminalio.FONT,text=text,color=0xFFFFFF,x=91,y=5)
    text_area1 = label.Label(terminalio.FONT,text=text1,color=0xFFFFFF,x=20,y=50)

    group = displayio.Group()
    
    if mic:
        group.append(tile_grid5)
     
    if speaker_mute:
        group.append(tile_grid4)
        
    if speaker_unmute:
        group.append(tile_grid3)
        
    if pc:
        group.append(tile_grid2)
        
    group.append(text_area)
    group.append(text_area1)
    group.append(tile_grid1)
    


    display.root_group = group
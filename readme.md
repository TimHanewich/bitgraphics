# bitgraphics
[`bitgraphics.py`](./src/bitgraphics.py) is a MicroPython module for displaying images, text, and other graphics on an [SSD-1306](https://www.adafruit.com/product/326) OLED display.

The `bitgraphics` module allows for you to easily encode images that can easily be moved to a microcontroller like a Raspberry Pi Pico and display on an OLED display.

## What does this do?
On a simple OLED display like an SSD-1306, each pixel can be represented as either a **0** or a **1**. `0` would indicate that the pixel is in an *off* position (black) and `1` would indicate that the pixel is in an *on* position (white). For example, consider the following example:

![smiley](https://i.imgur.com/bjSnnNr.png)

The standard `FrameBuffer` class that comes with MicroPython as part of the build-in `framebuf` module allows for us to manipulate individual pixels across the display, specifying the value (on/off) of any pixel at any coordinate across the display.

However, when it comes to displaying pictures, that can be a bit challenging. Firstly, you can load a bytearray buffer into a `FrameBuffer` object. This is demonstrated in this repo [here](https://github.com/TimHanewich/MicroPython-SSD1306), with this repo also providing some foundational tools to make that a bit easier. However, encoding *all* images of *any* dimension is not easy using this method, for various reasons.

The `bitgraphics` module developed here provides the same functionality as the method described in the repo referenced above, but also supports the following scenarios:
- Encode any image of any dimension
- Combine ("flatten") multiple graphics together into a single graphic
- Tools for positioning these graphics in the display
- Chain alphanumeric graphics together to form text using the `Typewriter` class

## Getting Started
In this short guide below I'll provide examples in how to use the `bitgraphics` module. The `bitgraphics` module is designed to run on both the "full" Python experience (on a device like a Windows, Linux, or Mac machine), and MicroPython experience (on a microcontroller like the Raspberry Pi Pico). When importing the `bitgraphics` module, different resources will be available depending on what machine you are loading it on.

### Encoding an image
`bitgraphics` uses [Pillow](https://pypi.org/project/pillow/) for image manipulation, so any images that you want to show on your SSD-1306 display must be encoded on the desktop first, with the encoded state (a `.json` file) being transfered to the microcontroller.

I have a simple 64x64 image of a dog's paw print that I want to encode and display on my SSD-1306 display:

![paw print](https://i.imgur.com/TXDemJw.png)

To encode this for use by the microcontroller, I will use the `image_to_BitGraphic` function (only available on desktop) of the `bitgraphics` module to encode it as a `BitGraphic` object. That can easily be done from REPL:

```
>>> import bitgraphics
>>> bg = bitgraphics.image_to_BitGraphic(r"C:\Users\timh\Downloads\pawprint.png")
>>> bg.to_json()
'{"bits": "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111110000000000000000000000000000000000000000000000000000001111111111100000000000000000000000000000000000000000000000000001111111111111100000000000000000000000000000000000000000000000001111111111111111000000000000000000000000000000000000000000000000111111111111111100000000000000000000000000000000000000000000000111111111111111111000000011111111000000000000000000000000000000011111111111111111100000111111111110000000000000000000000000000001111111111111111110000111111111111100000000000000000000000000001111111111111111111100111111111111111000000000000000000000000000111111111111111111110011111111111111110000000000000000000000000011111111111111111111011111111111111111000000000000000000000000001111111111111111111101111111111111111100000000000000011111100000111111111111111111111111111111111111110000000000000011111111110011111111111111111110111111111111111111100000000000011111111111100111111111111111111011111111111111111100000000000011111111111111011111111111111111101111111111111111110000000000011111111111111100111111111111111100111111111111111111000000000001111111111111111011111111111111110011111111111111111100000000000111111111111111100111111111111110000111111111111111110000000000011111111111111110001111111111110000011111111111111110000000000001111111111111111100011111111110000001111111111111111000000000000111111111111111110000001111000000000011111111111111001111110000011111111111111111000000000011111000000111111111111011111111111001111111111111111100000011111111111110001111111110011111111111100111111111111111110000111111111111111110001111100011111111111111001111111111111110000111111111111111111100000000011111111111111110111111111111111000111111111111111111111100000001111111111111111001111111111111000111111111111111111111111000001111111111111111100011111111111100111111111111111111111111100000111111111111111110000111111111000111111111111111111111111111000011111111111111111000000111110000111111111111111111111111111110001111111111111111100000000000000011111111111111111111111111111100111111111111111110000000000000011111111111111111111111111111110011111111111111111000000000000001111111111111111111111111111111101111111111111111000000000000001111111111111111111111111111111111111111111111111100000000000001111111111111111111111111111111111101111111111111100000000000000111111111111111111111111111111111111111111111111100000000000000111111111111111111111111111111111111101111111111100000000000000111111111111111111111111111111111111111001111111100000000000000011111111111111111111111111111111111111110000000000000000000000011111111111111111111111111111111111111111000000000000000000000001111111111111111111111111111111111111111110000000000000000000001111111111111111111111111111111111111111111000000000000000000000111111111111111111111111111111111111111111110000000000000000000011111111111111111111111111111111111111111111000000000000000000001111111111111111111111111111111111111111111100000000000000000000111111111111111111111111111111111111111111110000000000000000000011111111111111111111111111111111111111111111000000000000000000001111111111111111111111111111111111111111111000000000000000000000111111111111111111111111111111111111111111100000000000000000000011111111111111111111111111111111111111111110000000000000000000000111111111111111111111111111111111111111110000000000000000000000001111111111111111111111111111111111111111000000000000000000000000011111111111111111111111111111111111111000000000000000000000000000111111111111110000000011111111111111000000000000000000000000000000111111110000000000000001111111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", "width": 64, "height": 64}'
```

As you can see in the example above, the image was converted to a binary representation of 0's and 1's, each character representing the state of a pixel within the 64x64 graphic. Save this JSON string output to a file on your microcontroller! This is what will be opened, parsed, and used to display on your SSD-1306 display.

Please note that you can also resize an image before conversion using the optional `resize` parameter:

```
>>> import bitgraphics
>>> bg = bitgraphics.image_to_BitGraphic(r"C:\Users\timh\Downloads\pawprint.png", resize=(12,12))
>>> bg.to_json()
'{"bits": "000111000000001111111100011111111110111111111110111111111111111111111111111111111111001111111111011111111110011111111100011111111100001110111000", "width": 12, "height": 12}'
```

As you can see in the example above, by using `resize=(12,12)`, the image has been shrunk from a 64x64 graphic to a 12x12 graphic.

Finally, also note that you can batch convert a directory full of graphics using the `images_to_BitGraphics` function.

### Displaying the `BitGraphic`
Before running, ensure you are placing the [`ssd1306.py` module]() and [`bitgraphics.py` module]() on your microcontroller at the root level. These are two dependencies of the following code:

The following opens the `paw.json` file we converted and saved earlier and displays it on the display at position (0, 0) (top left).
```
import machine
import bitgraphics

# create I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) # I have my display hooked up to pins 14 and 15 (for I2C)
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# load the BitGraphic (paw.json)
bg = bitgraphics.BitGraphic(path="paw.json")

# display it
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create new BitGraphicDisplay with width 128, height 64
bgd.display(bg, 0, 0) # display the paw.json BitGraphic in the top left of the screen
bgd.show() # show what is displayed (turn on)
```

Result:

![paw](https://i.imgur.com/D62btXC.jpeg)

In the example above, I am opening the `BitGraphic` from a file. Note that you can also directly pass in the object as a JSON-encoded string or a `dict`:

```
import machine
import bitgraphics

# create I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) # I have my display hooked up to pins 14 and 15 (for I2C)
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# load the BitGraphic (paw.json)
bg = bitgraphics.BitGraphic(jsond={"bits": "0000000000000000000000000000000000000000000111000000000000000000000000000111111100000000000000000000000011111111100000000000000000000000111111111000111110000000000000011111111111011111110000000000000111111111111111111110000000010001111111111111111111100000011111011111111111111111111000001111111111111111111111111110000011111111111111111111111111100000111111111111111101111111111000001111111110111110001111111111110011111111100011111101111111111111111111111011111111111111111111111111111101111111111110011111111101111110111111111111110111111111000111011111111111111111111111110000001111111111111111111111111100000011111111111111111111111111000001111111111111111111111111100000111111111111111111111111110000001111111111111111111111000000000111111111111111111111110000000001111111111111111111111100000000011111111111111111111111000000000111111111111111111111110000000000111111111111111111111100000000000111111111111111111110000000000000111111111111111111000000000000000011000000000011000000000000000000000000000000000000000000", "width": 32, "height": 32})

# display it
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create new BitGraphicDisplay with width 128, height 64
bgd.display(bg, center=(0.5, 0.5)) # display the paw.json BitGraphic in the top left of the screen
bgd.show() # show what is displayed (turn on)
```

In the above example, a 32x32 version of the paw graphic is loaded as a `BitGraphic` directly from a `dict`. Also, note that the graphic is displayed using the `BitGraphicDisplay`'s optional `center` parameter, positioning the graphic to be perfectly centered at 50% of the width of the screen (`0.5`) and 50% of the height of the display (the other `0.5`):

![32x32 centered](https://i.imgur.com/LcWhhcT.jpeg)

## Combining multiple graphics into one with `BitGraphicGroup`
The `BitGraphicGroup` class can also be used to combine multiple `BitGraphic` objects into a single, combined `BitGraphic` object. For example:

```
import machine
import bitgraphics

# create I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) # I have my display hooked up to pins 14 and 15 (for I2C)
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# load graphics
rocket = bitgraphics.BitGraphic(jsond={"bits": "0000000000111111000000001111000100000001110000010000001110000011000111111111001101111110110100111110110011110110110110000111111010111000000111001111110000111000000111100111000000000111111100001111011110110000110100110110000011110010111000001111001111000000", "width": 16, "height": 16})
bolt = bitgraphics.BitGraphic(jsond={"bits": "0000011111110000000011000111000000001100011000000001100001100000000110001100000000011000111111000011000000001100001100000000110001100000000111000011111110011000000000011011000000000001111100000000001101100000000000111100000000000111110000000000011110000000", "width": 16, "height": 16})
plane = bitgraphics.BitGraphic(jsond={"bits": "0000111110000000000001101100000000000110110000000000001001100000111100110111000011110011001100001101111100111111011000000000001101100000000000111101111100111111111100110011000011110011011100000000001001100000000001101100000000000110110000000000111110000000", "width": 16, "height": 16})

# combine into one
bgg = bitgraphics.BitGraphicGroup()
bgg.add(rocket, 12, 0) # position (x:12, y:0) 
bgg.add(bolt, 0, 24) # position (0, 24) 
bgg.add(plane, 24, 24) # position (24, 24)
all_in_1 = bgg.flatten() # combine into a single BitGraphic

# display it
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create new BitGraphicDisplay with width 128, height 64
bgd.display(all_in_1, center=(0.5, 0.5)) # display the paw.json BitGraphic in the top left of the screen
bgd.show() # show what is displayed (turn on)
```

In the example above, three 16x16 graphics are loaded as `BitGraphic` objects. The three are then added to a `BitGraphicGroup`, positioned relative to one another. They are then flattened into a single `BitGraphic`, called *all_in_1*, and then shown on the display, centered in the middle of the display. 

Keep in mind that once you have flattened multiple graphics into one, you can also use the `to_json` function of that `BitGraphic` to save into a file for later!

## Typing with `Typewriter`
The `Typewriter` class within the `bitgraphics` module makes it easier to form words and sentences by "chaining together" graphics of alphanumeric characters. You can use the `Typewriter` class like this:

```
import machine
import bitgraphics

# create I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) # I have my display hooked up to pins 14 and 15 (for I2C)
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# create the Typewriter
tr = bitgraphics.Typewriter()
txt = tr.write("hi tim", 16, 16) # type of "hi tim" in 16x16 letters

# display it
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create new BitGraphicDisplay with width 128, height 64
bgd.display(txt, center=(0.5, 0.5)) # display the paw.json BitGraphic in the top left of the screen
bgd.show() # show what is displayed (turn on)
```

The above example types out "hi tim" and displays it:

![hi tim](https://i.imgur.com/MZuhRka.jpeg)

This is possible because the `Typewriter` class comes pre-loaded with 16x16 characters of every number (0-9) and every letter in uppercase (A-Z), as well as the space character. If you'd like to expand the characters and sizes that your `Typewriter` has at its disposal, you can use the `add_character` function to add additional graphics of various sizes:

```
import machine
import bitgraphics

# create I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15)) # I have my display hooked up to pins 14 and 15 (for I2C)
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# create the Typewriter and add required 24x24 letters
tr = bitgraphics.Typewriter()
tr.add_character("t", bitgraphics.BitGraphic(jsond={"bits": "001111111111111111111100001111111111111111111100001111111111111111111100001111111111111111111100000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000", "width": 24, "height": 24}))
tr.add_character("i", bitgraphics.BitGraphic(jsond={"bits": "000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000000000000011110000000000", "width": 24, "height": 24}))
tr.add_character("m", bitgraphics.BitGraphic(jsond={"bits": "111110000000000000011111111111000000000000111111111111000000000000111111111111000000000000111111111111100000000001111111111111100000000001111111111111100000000001111111111111110000000011111111111111110000000011111111111111111000000111111111111111111000000111111111111111111000000111111111111101111100001111101111111101111100001111101111111101111100001111101111111100111110011111001111111100111110011111001111111100111111111111001111111100011111111110001111111100011111111110001111111100001111111100001111111100001111111100001111111100001111111100001111111100000111111000001111", "width": 24, "height": 24}))

# type out "tim" in 24x24 letters. 
# because the size is being specified, the other pre-loaded 16x16 characters will not be selected
txt = tr.write("tim", 24, 24)

# display it
bgd = bitgraphics.BitGraphicDisplay(i2c, 128, 64) # create new BitGraphicDisplay with width 128, height 64
bgd.display(txt, center=(0.5, 0.5)) # display the paw.json BitGraphic in the top left of the screen
bgd.show() # show what is displayed (turn on)
```

![tim 24x24](https://i.imgur.com/kqyXlln.jpeg)

In the example above, the 24x24 letters "T", "I", and "M" are added and then used to type out "tim" in 24x24 size. You can add any characters of any size in this way. 

Note that, at the time of this writing, `Typewriter` is not case sensitive. Any letter, uppercase or lowercase, will be displayed as uppercase.

## Graphics Repository
I have collected some useful graphics in the graphics folder [here](./graphics/). Go there to read more!
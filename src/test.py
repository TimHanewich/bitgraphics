import bitgraphics as bit
import machine

# set up display
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
print(i2c.scan())
bgd = bit.BitGraphicDisplay(i2c, 128, 64)



def go():

    # open bitanimation
    print("opening bit animation...")
    ba = bit.BitAnimation("/test", "r")

    # play
    try:
        bgd.play(ba, 30)
    except Exception as e:
        print("Error while playing: " + str(e))
    finally:
        ba.close()
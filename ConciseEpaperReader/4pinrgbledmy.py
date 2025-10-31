
import machine as m


if __name__ == "__main__":
    r = m.Pin(1,m.Pin.OUT)
    g = m.Pin(2,m.Pin.OUT)
    b = m.Pin(3,m.Pin.OUT) 
    r.value(1)
    pass
import usys
import ustruct as struct
import utime
from machine import Pin, SPI, ADC
from nrf24l01 import NRF24L01
from micropython import const

# Slave pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)
# Slave pauses an additional _SLAVE_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) master time to get into receive mode. The
# master may be a slow device.
_SLAVE_SEND_DELAY = const(10)

#initialize SPI interface for pi pico
if usys.platform == "rp2":  # PI PICO
    cfg = {"spi": 0, "miso": 4, "mosi": 7, "sck": 6, "csn": 14, "ce": 17}
else:
    raise ValueError("Unsupported platform {}".format(usys.platform))

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

#use GPIO26 for reading analog value of potentiometer
pot = ADC(Pin(26))
#use GPIO27 to capture the value of the motion sensor
motion_sensor = Pin(27, Pin.IN, Pin.PULL_DOWN)

def master():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    if cfg["spi"] == 0:
        spi = SPI(0, sck=Pin(cfg["sck"]), mosi=Pin(cfg["mosi"]), miso=Pin(cfg["miso"]))
        nrf = NRF24L01(spi, csn, ce, payload_size=32)
    else:
        nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=32)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()
    print("NRF24L01 master mode, detecting thieves ...")
    
    while True:
        #make nrf module ready for sending
        nrf.stop_listening()
        #read motion sensor
        alarm_state = motion_sensor.value()
        #read potentiometer and remap value to the number of sounds in your soundboard
        pot_value = pot.read_u16()
        
        #warn the other side when movement is detected
        if alarm_state == 1:
            print("sending:", alarm_state, pot_value)
            try:
                nrf.send(struct.pack("ii", alarm_state, pot_value))
            except OSError:
                pass

            # start listening again
            nrf.start_listening()

            # wait for response, with 500ms timeout
            start_time = utime.ticks_ms()
            timeout = False
            while not nrf.any() and not timeout:
                if utime.ticks_diff(utime.ticks_ms(), start_time) > 500:
                    timeout = True

            if timeout:
                print("failed, response timed out")

            else:
                #receive packet
                (acknowledge,) = struct.unpack("i", nrf.recv())
                print("got response:", acknowledge)
                #break the sending loop when we're sure the other side received our warning
                #note: this will force the pico to be manually reset!
                break
                
                    
            #delay then loop
            utime.sleep_ms(250)

# alarm-system
Hi and welcome to Bonsa's alarm system! Ever had an annoying sibling enter your room while you're away?\
Or would you just like to experiment with a few common data protocols to test your electronics knowledge?\
Look no further! 
## BOM
| component | amount | type |
| --- | --- | --- |
| Pi Pico | 2  | W |
| motionsensor | 1 | PIR |
| oled  | 1 | SSD1306 |
| nrf24L01  | 2  | + |
| potentiometer  | 1  | 50k Ohms |
| buzzer | 1 | |
| push button | 1 | |
| resistor | 1 | 10k Ohms
| Dupont cables | 20 | |

Most of these components are ubiquitous and should already be in your electronics kit!\
Maybe the PIR sensor is new to you, but it's actually pretty simple and easy to use. It requires a little bit of finetuning depending on the light in your environment.\
The one used in this project can be found [here](https://www.gotron.be/pir-bewegingssensor-voor-arduinor.html)

## build guide
### 1. connect nrf modules
To keep things easy, both modules use the same pins for their connection to the nrf modules.\
wiring table:

| Pico	| NRF24L01+ |
| --- | --- |
| Pin 36 / 3V3 Out | 	VCC |
| Pin 38 / GND (or any other GND Pin)	| GND |
| Pin 22 / GP17	| CE |
| Pin 19 / GP14	| CS |
| Pin 9 / GP6	| SCK |
| Pin 10 / GP7	| MOSI |
| Pin 6 / GP4	| MISO |

note that the IQR pin on both nrf modules is left unconnected. They are not necessary for this project.

### 2. connect PIR sensor
Choose which Pico you want to use to capture motion. Connect the sensor as follows:

| Pico	| PIR sensor |
| --- | --- |
| Pin 36 / 3V3 Out | 	VCC |
| Pin 38 / GND (or any other GND Pin)	| GND |
| Pin 32 / GP27	| digital in |

### 3. connect the potentiometer
On the same Pico that you connected the PIR sensor to, connect the potentiometer.\
Follow this wiring diagram:

| Pico	| potentiometer |
| --- | --- |
| Pin 36 / 3V3 Out | 	VCC |
| Pin 38 / GND (or any other GND Pin)	| GND |
| Pin 31 / GP26	| analog in |

You are now done with the master of this project. We're halfway there, congrats!

### 3. connect the oled display
Take the other Pi Pico and connect your oled display as follows:

| Pico	| oled |
| --- | --- |
| Pin 36 / 3V3 Out | 	VCC |
| Pin 38 / GND (or any other GND Pin)	| GND |
| Pin 1 / GP0	| SDA |
| Pin 2 / GP1	| SCL |

### 4. connect the reset button
On Pin 14 (GP10) connect a pushbutton with the 10k Ohms resistor to GND like this:\
![image](https://user-images.githubusercontent.com/68948638/231729023-5c4e8c00-e941-4072-bc76-0cf64cc6c3c8.png)

### 5. connect the buzzer
On Pin 21 (GP16) connect 1 leg of the buzzer. Connect the other leg to a GND pin, like Pin 38.\
You are now finished with all the wiring. Congratulations!

## code
All that's left to do is upload the correct folder to every Pico. The one with the oled screen connected should get the folder called slave.\
The other one the folder called master.

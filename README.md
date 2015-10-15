# RPiSmartThermostat
RaspberryPi-based Smart Thermostat

## Steps:
1. Assemble hardware
  - Wall unit: Raspberry pi with LCD hat and DHT22 sensor
	-- https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi
  - Control unit: ESP8266 controlling a JBTek Relay board
    -- https://www.adafruit.com/product/2471
3. Program wall unit with control logic 
4. Wire HVAC interface relay control board
5. Adapt control logic to learn trends
  - preferences 
  - weather 
  - season
6. Go nuts. Add more sensors, controllers
  - Humidifier
  - Furnace fan
  - Patio melter
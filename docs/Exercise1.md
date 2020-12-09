# First exercise: blinking a LED

Long pin is positive, short pin is ground
Always use a current limiting resistor 

## Open the micropython repl
```bash
rshell -p COM7 repl 
```

## Enter some python

```python
from machine import Pin
led = Pin(17, Pin.OUT)
led.on()
```

## Blink the led

Hint:
```python
from time import sleep_ms
```
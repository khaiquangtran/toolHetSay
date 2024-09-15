from pynput.mouse import Controller

mouse = Controller()
position = mouse.position
print(f"Current mouse position is {position}")

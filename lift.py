from boxlift_api import Command, BoxLift
from pprint import pprint

box_lift = BoxLift('Lolevator', 'training_1', 'aywang31@gmail.com', '13247', event_name='pycon2015', sandbox_mode=False)

state = box_lift.send_commands()
pprint(state)

floors = state['floors']

trip = 0
direction = 1
while trip < 10: # Total trips through building
    floor = 0
    while floor < floors:
        command = Command(0, direction, 1)
        state = box_lift.send_commands([command])
        pprint(state)

        if floor == floors-1:
            direction = -direction

        command = Command(0, direction, 0)
        state = box_lift.send_commands([command])
        pprint(state)
        floor += 1
    trip += 1


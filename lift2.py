from boxlift_api import Command, BoxLift
from pprint import pprint

box_lift = BoxLift('Lolevator', 'training_1', 'aywang31@gmail.com', '13247', event_name='pycon2015', sandbox_mode=True)

pprint(box_lift.send_commands())

elevator_states = {}
for elevator in state['elevators']:
    elevator_states[elevator['id']] = {'speed': 0}

def get_state_for_elevator(elevator_id, state):
    for elevator in state['elevators']:
        if elevator['id'] == elevator_id:
            return elevator
    raise "Unknown elevator %s" % elevator_id

def direction(elevator):
    if elevator['direction'] == 1:
        if max(elevator['buttons_pressed']) > elevator['floor']:
            return 1
        else:
            return -1
    elif elevator['direction'] == -1:
        if min(elevator['buttons_pressed']) < elevator['floor']:
            return -1
        else:
            return 1
    else:
        return 'Error - unknown elevator direction'

def stop_elevator_on_floor(elevator_id, floor, state):
    elevator = get_state_for_elevator(elevator_id)
    if floor == elevator['floor'] and elevator['speed'] == 1:
        return Command(elevator_id, direction(elevator), 0)
    elif floor == elevator['floor'] and elevator['speed'] == 0:
        raise 'Error - elevator has not dropped off passengers'
    elif direction(elevator) in [1, -1]:
        return Command(elevator_id, direction(elevator), 1)
    else:
        return Command(elevator_id, 1, 0)

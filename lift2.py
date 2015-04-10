from boxlift_api import Command, BoxLift
from pprint import pprint

box_lift = BoxLift('Lolevator', 'training_1', 'aywang31@gmail.com', '13247', event_name='pycon2015', sandbox_mode=True)

state = box_lift.send_commands()
pprint(state)

elevator_states = {}
for elevator in state['elevators']:
    elevator_states[elevator['id']] = {'speed': 0, 'direction': 1}


def get_state_for_elevator(elevator_id, state):
    for elevator in state['elevators']:
        if elevator['id'] == elevator_id:
            elevator['speed'] = elevator_states[elevator['id']]['speed']
            elevator['direction'] = elevator_states[elevator['id']]['direction']
            return elevator
    raise "Unknown elevator %s" % elevator_id

def floor_requests(elevator, state):
    return set(elevator['buttons_pressed'] + [request['floor'] for request in state['requests']])

def direction(elevator, state):
    requests = floor_requests(elevator, state)
    if len(requests) == 0:
        return 1
    if elevator['direction'] == 1:
        if max(requests) > elevator['floor']:
            return 1
        else:
            return -1
    elif elevator['direction'] == -1:
        if min(requests) < elevator['floor']:
            return -1
        else:
            return 1
    else:
        return 'Error - unknown elevator direction'

def stop_direction(floor, state):
    for request in state['requests']:
        if request['floor'] == floor:
            return request['direction']
    return 1

def stop_floor(elevator, state):
    if elevator['floor'] in [request['floor'] for request in state['requests']]:
        return True
    if elevator['floor'] in elevator['buttons_pressed']:
        return True
    return False

def iterate_elevator(elevator_id, state):
    elevator = get_state_for_elevator(elevator_id, state)
    if stop_floor(elevator, state):
        return Command(elevator_id, stop_direction(elevator['floor'], state), 0)
    elif direction(elevator, state) in [1, -1]:
        return Command(elevator_id, direction(elevator, state), 1)
    else:
        return Command(elevator_id, 1, 0)

while state['status'] != 'finished':
    command = iterate_elevator(0, state)
    state = box_lift.send_commands([command])
    pprint(state)


import random
from .settings import *

class Generator:
    def __init__(self, req_size = 15, time_limit = 30, max_simultaneous_req = 15):
        self.elevator_info = [{'id': i, 'speed':0.4, 'capacity': 6, 'maintained': False} for i in range(1,7)]
        self.elevator_size = 6
        self.running_elevator = 6
        self.req_id = 0
        self.req_size = req_size
        self.time_limit = time_limit
        self.max_sim = max_simultaneous_req


    def gen(self):
        self.req_list = []
        self.req_info = []
        self.maintain_info = []
        time = 1.0
        maintain_set = []

        while time < self.time_limit and len(self.req_list) < self.req_size:
            self.time += random.random() * self.time_limit / (float(self.req_size) / self.max_sim)
            n = random.randint(1, self.max_sim + 1)

            if (random.random() < 0.3 and self.elevator_size < ELEVATOR_MAX_ALLOCATED):
                n -= 1
                if (random.random < 0.5 or self.running_elevator <= 2):
                    self.elevator_size += 1
                    self.running_elevator += 1
                    speed = random.choice(ELEVATOR_SPEED_LIST)
                    capacity = random.choice(ELEVATOR_CAPACITY_LIST)
                    starting_floor = 1
                    self.elevator_info.append({'id': self.elevator_size, 'speed': speed, 'capacity': capacity, 'maintained': False})
                    self.req_list.append("[{:.1f}]ADD-Elevator-{}-{}-{}-{:.1f}".format(time, self.elevator_size, starting_floor, capacity, speed))
                    self.maintain_info.append({'id': self.elevator_size, 'time': time, 'action': 'ADD'})
                else:
                    self.running_elevator -= 1
                    mid = random.randint(ELEVATOR_MIN_SIZE + 1, self.elevator_size)
                    while mid in maintain_set:
                        mid = random.randint(ELEVATOR_MIN_SIZE + 1, self.elevator_size)
                    maintain_set.append(mid)
                    self.req_list.append("[{:.1f}]MAINTAIN-Elevator-{}".format(time, mid))
                    self.maintain_info.append({'id': mid, 'time': time, 'action': 'MAINTAIN'})

            for i in range(n):
                start = random.randint(MIN_FLOOR, MAX_FLOOR)
                end = random.randint(MIN_FLOOR, MAX_FLOOR)
                while start == end:
                    end = random.randint(MIN_FLOOR, MAX_FLOOR)
                self.req_id += 1
                self.req_info.append({'id': self.req_id, 'from': start, 'to': end, 'time': time, 'status': 'WAITING'})
                self.req_list.append("[{:.1f}]{}-FROM-{}-TO-{}".format(time, self.req_id, start, end))

        return ('\n'.join(self.req_list), self.req_info, self.elevator_info)

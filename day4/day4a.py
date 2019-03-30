import datetime
import re
from collections import defaultdict, namedtuple

def get_data(parser=str):
    with open('input.txt', 'r') as f:
        values = [parser(line) for line in f.readlines()]
    return values

#[1518-09-19 00:42] wakes up
#[1518-08-06 00:16] wakes up
#[1518-07-18 00:14] wakes up
#[1518-03-23 00:19] falls asleep
#[1518-10-12 23:58] Guard #421 begins shift
DATE_FMT = '%Y-%m-%d %H:%M'
LINE_REGEXP = re.compile(r'\[(?P<date>[^\]]*)\] (?P<message>.*)')

class EventType:
    START_SHIFT = 0
    SLEEP = 1
    WAKE = 2

def parse_line(line):
    m = LINE_REGEXP.match(line).groupdict()
    msg = m['message'].split()
    date = datetime.datetime.strptime(m['date'], DATE_FMT)
    if msg[0] == 'wakes':
        return (date, EventType.WAKE, None)
    elif msg[0] == 'falls':
        return (date, EventType.SLEEP, None)
    else:
        return (date, EventType.START_SHIFT, int(msg[1][1:]))

class GuardState:
    ASLEEP = 0
    AWAKE = 1

class GuardSchedule(object):

    def __init__(self):
        self.asleep_minutes = defaultdict(int)
        self.guard_state = GuardState.AWAKE
        self.current_minute = 0
        self.total_asleep_minutes = 0
    
    def start_shift(self):
        self.guard_state = GuardState.AWAKE
        self.current_minute = 0

    def set_awake(self, time):
        self._update_asleep_minutes(GuardState.AWAKE, time.minute)

    def set_asleep(self, time):
        self._update_asleep_minutes(GuardState.ASLEEP, time.minute)

    def end_shift(self):
        self._update_asleep_minutes(GuardState.AWAKE, 60)
    
    def _update_asleep_minutes(self, new_state, new_minute):
        if self.guard_state == GuardState.ASLEEP:
            if new_state == GuardState.AWAKE:
                for minute in range(self.current_minute, new_minute):
                    self.asleep_minutes[minute] += 1
                self.total_asleep_minutes += (new_minute - self.current_minute)
                self.current_minute = new_minute
        elif self.guard_state == GuardState.AWAKE:
            if new_state == GuardState.ASLEEP:
                self.current_minute = new_minute

        self.guard_state = new_state
    
    def minutes_asleep(self):
        return self.total_asleep_minutes
    
    def best_minute(self):
        if self.asleep_minutes:
            return sorted(self.asleep_minutes.items(), key=lambda entry: entry[1], reverse=True)[0]
        return None

def build_guard_entries(entries):
    guards = {}
    current_guard = None
    for (e_date, e_type, e_guard_id) in entries:
        if e_type == EventType.START_SHIFT:
            if current_guard is not None:
                current_guard.end_shift()
            if not e_guard_id in guards:
                guards[e_guard_id] = GuardSchedule()
            current_guard = guards[e_guard_id]
            current_guard.start_shift()
        elif e_type == EventType.WAKE:
            current_guard.set_awake(e_date)
        elif e_type == EventType.SLEEP:
            current_guard.set_asleep(e_date)
    current_guard.end_shift()
    return guards

values = sorted(get_data(parser=parse_line))
guards = build_guard_entries(values)
data = []
for guard, schedule in guards.items():
    data.append((schedule.minutes_asleep(), schedule.best_minute(), guard))

winner = sorted(data, reverse=True)[0]
minutes_asleep, (best_minute, number_sleeps), guard_id = winner
print(f'mins: {minutes_asleep} best: {best_minute} num_sleeps: {number_sleeps} guard_id: {guard_id}')
print(f'result A => {guard_id*best_minute}')

data = []
for guard, schedule in guards.items():
    best = schedule.best_minute()
    if best is not None:
        data.append((best[1], best[0], schedule.minutes_asleep(), guard))

winner = sorted(data, reverse=True)[0]
number_sleeps, best_minute, minutes_asleep, guard_id = winner
print(f'mins: {minutes_asleep} best: {best_minute} num_sleeps: {number_sleeps} guard_id: {guard_id}')
print(f'result B => {guard_id*best_minute}')

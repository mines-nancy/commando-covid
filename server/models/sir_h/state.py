from models.sir_h.box import Box
from models.history import History


class State:
    def __init__(self,
                 delays,
                 coefficients,
                 time,
                 population
                 ):

        self._delays = delays
        self._coefficients = coefficients

        self._boxes = {
            'SE': Box('SE', 0),
            'INCUB': Box('INCUB', delays.dm_imcub),
            'IR': Box('IR', delays.dm_r),
            'IH': Box('IH', delays.dm_h),
            'SM': Box('SM', delays.dm_sm),
            'SI': Box('SI', delays.dm_si),
            'SS': Box('SS', delays.dm_ss),
            'DC': Box('DC')
        }

        # src -> [targets]
        self._moves = {
            'INCUB': [('IR', coefficients.pc_ir)],
            'INCUB': [('IH', coefficients.pc_ih)],
            'IR': [('R', 1)],
            'IH': [('SM', coefficients.pc_sm), ('SI', coefficients.pc_si)],
            'SM': [('SI', coefficients.pc_sm_si),
                   ('SS', coefficients.pc_sm_out * coefficients.pc_h_ss),
                   ('R', coefficients.pc_sm_out * coefficients.pc_h_r)],
            'SI': [('DC', coefficients.pc_si_dc),
                   ('SS', coefficients.pc_si_out * coefficients.pc_h_ss),
                   ('R', coefficients.pc_si_out * coefficients.pc_h_r)],
        }

        self.time = time

        self.e0 = delays.kpe * population
        self.box('SE').add(self.e0-1)
        self.box('INCUB').add(1)

    def boxes(self):
        return self._boxes.values()

    def boxnames(self):
        return self._boxes.keys()

    def box(self, name):
        return self._boxes[name]

    def output(self, name):
        return self.box(name).output()

    def delay(self, name):
        return self._delays[name]

    def coefficient(self, name):
        return self._coefficients[name]

    def __str__(self):
        pop = sum([box.full_size() for box in self.boxes()])
        return f'{self.box("E")} {self.box("MG")} {self.box("MH")} {self.box("HG")} {self.box("HR")} {self.box("R")} {self.box("G")} {self.box("D")} POP={round(pop,2)}'

    def get_time0(self):
        return 0

    def move(self, src_name, dest_name, delta):
        self.box(src_name).remove(delta)
        self.box(dest_name).add(delta)

    def step(self, history):
        self.time += 1
        for box in self.boxes():
            box.step()

        self.step_exposed(history)
        self.generic_steps(self._moves)

    def generic_steps(self, moves):
        for src_name in moves.keys():
            for dest_name, coefficient in moves[src_name]:
                self.move(src_name, dest_name, coefficient *
                          self.output(src_name))

    def step_exposed(self, history):
        n = self.box('SE').size() + self.box('INCUB').size() + \
            self.box('IR').size() + self.box('IH').size() + \
            self.box('R').size()
        previous_state = history.get_last_state(self.time - 1)
        delta = self._coefficients.r * self._coefficients.beta * \
            self.box('SE').output() * \
            (previous_state.box('IR').size() + previous_state.box('IH').size()) / n
        self.move('SE', 'INCUB', delta)

    def extract_series(self, history):
        series = {'SE': ['SE'], 'R': ['R'], 'I': ['INCUB', 'IR', 'IH'],
                  'SM': ['SM'],  'SI': ['SI'], 'SS': ['SS'], 'DC': ['DC'], }
        # sum the sizes of boxes
        lists = {name: [] for name in series.keys()}
        for state in history.sorted_list():
            sizes = {name: state.box(name).full_size()
                     for name in self.boxnames()}
            for name in lists.keys():
                lists[name].append(sum([sizes[n] for n in series[name]]))
        return lists

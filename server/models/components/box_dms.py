import math
from models.components.box import Box


class BoxDms(Box):
    def __init__(self, name, duration=math.inf):
        Box.__init__(self, name)
        self._duration = duration
        self._removed = 0

    def __str__(self):
        input = round(self.input(), 2)
        size = round(self.size(), 2)
        removed = round(self._output, 2)
        return f'BoxDms {self._name} t={self._t} [{input}]\{size}/[{removed}]'

    def step(self):
        previous_input = self.input()
        previous_output = self.output()
        previous_size = self.size()

        super().step()

        self._removed = 0
        if self._duration == 0:
            self.set_output(previous_output + previous_input)
            return

        new_output = previous_size / self._duration
        # print(f'pop: {output}')
        self.set_size(previous_size + previous_input - new_output)
        self.set_output(previous_output + new_output)
        # print(f'output: {self._output}')

    def full_size(self):
        return self.size() + self.input()

    def removed(self):
        return self._removed

    def remove(self, size):
        super().remove(size)
        self._removed += size


class BoxDmsSource(BoxDms):
    def __init__(self, name):
        BoxDms.__init__(self, name, 0)

    def step(self):
        super().step()
        self._removed = 0
        self.set_output(self.output(1) + self.input(1))

    def size(self):
        return self.output()


class BoxDmsTarget(BoxDms):
    def __init__(self, name):
        BoxDms.__init__(self, name)

    def step(self):
        super().step()
        self._removed = 0
        self.set_size(self.size(1) + self.input(1))

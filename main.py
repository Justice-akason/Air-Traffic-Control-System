class Plane:
    def __init__(self, name, fuel, distance, emergency=False):
        self.name = name
        self.fuel = fuel
        self.distance = distance
        self.emergency = emergency

    @property
    def priority(self):
        emergency_rank = 0 if self.emergency else 1
        return (emergency_rank, self.fuel + self.distance, self.fuel)

    def __repr__(self):
        tag = " [EMERGENCY]" if self.emergency else ""
        return f"{self.name}(fuel={self.fuel}%, dist={self.distance}km){tag}"


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def enqueue(self, plane):
        self.heap.append(plane)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i].priority < self.heap[parent].priority:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def dequeue(self):
        if self.is_empty():
            return None
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._heapify_down(0)
        return top

    def _heapify_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self.heap[left].priority < self.heap[smallest].priority:
                smallest = left
            if right < n and self.heap[right].priority < self.heap[smallest].priority:
                smallest = right
            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def update(self, plane, fuel=None, distance=None, emergency=None):
        if fuel is not None:
            plane.fuel = fuel
        if distance is not None:
            plane.distance = distance
        if emergency is not None:
            plane.emergency = emergency
        self._rebuild()

    def _rebuild(self):
        planes = self.heap[:]
        self.heap = []
        for p in planes:
            self.enqueue(p)


class LandingLog:
    def __init__(self):
        self.stack = []

    def push(self, plane):
        self.stack.append(plane)

    def most_recent(self):
        if not self.stack:
            return None
        return self.stack[-1]

    def pop(self):
        if not self.stack:
            return None
        return self.stack.pop()


class ATCS:
    def __init__(self):
        self.queue = PriorityQueue()
        self.log = LandingLog()

    def request_landing(self, plane):
        self.queue.enqueue(plane)

    def land_next(self):
        plane = self.queue.dequeue()
        if plane is not None:
            self.log.push(plane)
        return plane

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def bfs(room_id, destination, room_grid):
    q = Queue()
    q.enqueue(room_id)
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            if v == destination:
                return path

            visited.add(v)
            for key, value in room_grid[f'{v}'].items():
                new_path = list(path)
                new_path.append(value)
                q.enqueue(new_path)

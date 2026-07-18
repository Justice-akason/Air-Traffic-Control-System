```
FUNCTION computePriority(plane):
    IF plane.emergency:
        emergencyRank = 0
    ELSE:
        emergencyRank = 1
    RETURN (emergencyRank, plane.fuel + plane.distance, plane.fuel)
```

The priority is a three-part key compared left to right:
1. emergencyRank puts every emergency ahead of every normal plane.
2. fuel + distance orders planes within the same group.
3. fuel is the final tie-breaker (lower fuel lands first).

```
FUNCTION enqueue(heap, plane):
    APPEND plane TO heap
    heapifyUp(heap, LAST index of heap)

FUNCTION heapifyUp(heap, i):
    WHILE i > 0:
        parent = (i - 1) / 2
        IF computePriority(heap[i]) < computePriority(heap[parent]):
            SWAP heap[i] AND heap[parent]
            i = parent
        ELSE:
            BREAK

FUNCTION dequeue(heap):
    IF heap is empty: RETURN null
    top = heap[0]
    last = REMOVE last element of heap
    IF heap not empty:
        heap[0] = last
        heapifyDown(heap, 0)
    RETURN top

FUNCTION heapifyDown(heap, i):
    n = SIZE of heap
    LOOP:
        smallest = i
        left = 2*i + 1
        right = 2*i + 2
        IF left < n AND computePriority(heap[left]) < computePriority(heap[smallest]):
            smallest = left
        IF right < n AND computePriority(heap[right]) < computePriority(heap[smallest]):
            smallest = right
        IF smallest != i:
            SWAP heap[i] AND heap[smallest]
            i = smallest
        ELSE:
            BREAK

FUNCTION peek(heap):
    IF heap is empty: RETURN null
    RETURN heap[0]

FUNCTION updatePriority(heap, plane, newFuel, newDistance, newEmergency):
    plane.fuel = newFuel
    plane.distance = newDistance
    plane.emergency = newEmergency
    REBUILD heap

FUNCTION landNextPlane(heap, landedLog):
    plane = dequeue(heap)
    IF plane != null:
        PUSH plane ONTO landedLog
    RETURN plane
```

The landedLog is a **stack (LIFO)**: the most recently landed plane sits on top, which serves as an audit trail once landing is complete.

---

## Q4 Dry Run

Starting planes (no emergencies yet), with computed keys:

| Plane | Fuel % | Distance km | Priority key      |
|-------|--------|-------------|-------------------|
| A     | 20     | 50          | (1, 70, 20)       |
| B     | 60     | 30          | (1, 90, 60)       |
| C     | 30     | 70          | (1, 100, 30)      |
| D     | 90     | 10          | (1, 100, 90)      |

**Building the heap** (array form after each enqueue):

```
enqueue A -> [A]
enqueue B -> [A, B]          B(90) not < A(70), no swap
enqueue C -> [A, B, C]       C(100) not < A(70), no swap
enqueue D -> [A, B, C, D]    D(100) not < B(90), no swap
```

Heap root is A, the most urgent. Array: `[A, B, C, D]`.

**Landing sequence:**

```
land -> A   remove root, move D up, sift down -> [B, D, C]   log: [A]
land -> B   remove root, move C up, sift down -> [C, D]      log: [A, B]
```

**Emergency injected:** Plane E arrives, fuel 80%, distance 90 km, emergency = TRUE.
Key = (0, 170, 80).

```
enqueue E -> heap [C, D, E] then heapifyUp:
    E(0,...) < C(1,...) because rank 0 < 1  -> swap
    heap -> [E, D, C]
```

Even though E has high fuel and is far out, the emergency rank puts it at the front.

```
land -> E   emergency lands first   -> [C, D]   log: [A, B, E]
land -> C                            -> [D]      log: [A, B, E, C]
land -> D                            -> []       log: [A, B, E, C, D]
```

**Final landing order:** A, B, E, C, D.
**Landing log top-to-bottom (LIFO):** D, C, E, B, A. Most recent landing = D.

This demonstrates: correct base ordering (A, B, C, D), an emergency jumping the queue, and the LIFO audit log.

---

## Q5 Optimization Strategies

1. **Indexed heap.** Keep a hash map from plane ID to its position in the heap. This turns a priority update from a full O(n log n) rebuild into an O(log n) decrease-key or increase-key operation, which matters when conditions change often.

2. **Aging to prevent starvation.** A steady stream of emergencies could leave low-priority planes waiting indefinitely. Give waiting planes a small priority boost over time so no flight is starved of a landing slot.

3. **Separate emergency lane.** Maintain two heaps: one for emergencies, one for normal traffic. Always drain the emergency heap first. This keeps emergencies from churning the main heap and simplifies reasoning.

4. **Cached priority.** Store the computed key on the plane and only recompute when fuel, distance, or emergency status actually changes, rather than on every comparison.

5. **Fibonacci heap.** For very high update volumes, a Fibonacci heap offers O(1) amortized insert and decrease-key, though a binary heap is simpler and usually sufficient for this scale.

6. **Batching and lazy deletion.** When many updates arrive together, mark stale entries and skip them on removal instead of rebuilding immediately, reducing per-update overhead.

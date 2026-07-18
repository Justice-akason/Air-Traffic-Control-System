# Air Traffic Control System Using a Priority Queue

This project demonstrates how a priority queue can be used to determine the landing order of aircraft in a simplified Air Traffic Control System.

Aircraft are prioritised according to:

* Remaining fuel level
* Distance from the runway
* Emergency status

The system uses a binary heap to ensure that the most urgent aircraft is selected first.

## Project Overview

A normal queue processes items in arrival order. This is unsuitable for air traffic control because an aircraft with critically low fuel may need to land before an aircraft that arrived earlier.

A priority queue solves this problem by ordering aircraft according to urgency rather than arrival time.

| Data Structure | Processing Method                           | Suitable for ATCS? |
| -------------- | ------------------------------------------- | ------------------ |
| FIFO Queue     | First aircraft to arrive is processed first | No                 |
| LIFO Stack     | Most recent aircraft is processed first     | No                 |
| Priority Queue | Most urgent aircraft is processed first     | Yes                |

## Priority Formula

Each aircraft receives a numerical priority score:

```text
Priority = (100 - Fuel) + (100 / Distance)
```

Where:

* `Fuel` is the aircraft’s remaining fuel percentage.
* `Distance` is the aircraft’s distance from the runway in kilometres.
* A higher score represents greater urgency.

The formula gives fuel level more influence than distance. Aircraft with lower fuel therefore move closer to the front of the queue.

## Pseudocode

```text
BEGIN

Create PriorityQueue PQ

FUNCTION CalculatePriority(Fuel, Distance)
    Priority = (100 - Fuel) + (100 / Distance)
    RETURN Priority
END FUNCTION

FUNCTION AddPlane(Name, Fuel, Distance)
    Priority = CalculatePriority(Fuel, Distance)
    Insert (Name, Priority) into PQ
END FUNCTION

FUNCTION LandNextPlane()
    Plane = ExtractHighestPriority(PQ)
    Display Plane.Name + " cleared to land"
END FUNCTION

END
```

## Example Aircraft Data

| Plane | Distance | Fuel |
| ----- | -------: | ---: |
| A     |    50 km |  20% |
| B     |    30 km |  60% |
| C     |    70 km |  30% |
| D     |    10 km |  90% |

The calculated priority scores are:

| Plane | Priority Score |
| ----- | -------------: |
| A     |           82.0 |
| B     |           43.3 |
| C     |           71.4 |
| D     |           20.0 |

The initial landing order is:

```text
Plane A → Plane C → Plane B → Plane D
```

Plane C is given a higher priority than Plane B because its lower fuel level outweighs Plane B’s shorter distance from the runway.

## Queue Update Example

After Plane A lands:

```text
Plane C → Plane B → Plane D
```

Plane E then arrives with:

```text
Fuel: 10%
Distance: 40 km
Priority: 92.5
```

The updated queue becomes:

```text
Plane E → Plane C → Plane B → Plane D
```

After Plane E lands:

```text
Plane C → Plane B → Plane D
```

The heap reorganises itself after each insertion or removal so that the highest-priority aircraft remains at the front.

## Time Complexity

A binary heap provides efficient priority queue operations:

| Operation                        | Time Complexity |
| -------------------------------- | --------------: |
| View highest-priority aircraft   |            O(1) |
| Insert an aircraft               |        O(log n) |
| Remove highest-priority aircraft |        O(log n) |
| Search for a specific aircraft   |            O(n) |

The structure is suitable because insertion and removal remain efficient as the number of aircraft increases.

## Possible Improvements

The system could be extended by adding:

1. Emergency overrides for aircraft experiencing critical incidents.
2. Automatic priority updates when fuel levels or distances change.
3. Separate priority queues for multiple runways.
4. Weighted priority scoring for fuel, distance and emergency status.
5. A hash table for locating and updating individual aircraft quickly.
6. Validation to prevent invalid fuel or distance values.
7. A graphical interface showing the current landing queue.

## Limitations

This is a simplified academic model. A real Air Traffic Control System would consider additional factors, including:

* Weather conditions
* Aircraft type and size
* Runway availability
* Mechanical emergencies
* Medical emergencies
* Air traffic separation rules
* Communication with pilots
* Decisions made by qualified air traffic controllers

The model is intended to demonstrate the use of priority queues and binary heaps rather than reproduce a complete aviation control system.

## References

Baka, B. (2017). *Python data structures and algorithms*. Packt Publishing.

Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C. (2009). *Introduction to algorithms* (3rd ed.). MIT Press.

Goodrich, M. T., Tamassia, R., and Goldwasser, M. H. (2013). *Data structures and algorithms in Python*. Wiley.

## Author

**Justice Akason**

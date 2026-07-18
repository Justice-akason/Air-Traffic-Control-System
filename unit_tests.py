import unittest
from atcs import Plane, PriorityQueue, LandingLog, ATCS


class TestPriorityOrdering(unittest.TestCase):
    def test_brief_example_orders_A_B_C_D(self):
        atcs = ATCS()
        atcs.request_landing(Plane("A", 20, 50))
        atcs.request_landing(Plane("B", 60, 30))
        atcs.request_landing(Plane("C", 30, 70))
        atcs.request_landing(Plane("D", 90, 10))
        order = [atcs.land_next().name for _ in range(4)]
        self.assertEqual(order, ["A", "B", "C", "D"])

    def test_low_fuel_outranks_close_but_full(self):
        pq = PriorityQueue()
        pq.enqueue(Plane("Full", 95, 5))
        pq.enqueue(Plane("Thirsty", 10, 60))
        self.assertEqual(pq.dequeue().name, "Thirsty")

    def test_tie_broken_by_lower_fuel(self):
        pq = PriorityQueue()
        pq.enqueue(Plane("C", 30, 70))
        pq.enqueue(Plane("D", 90, 10))
        self.assertEqual(pq.dequeue().name, "C")


class TestEmergencyHandling(unittest.TestCase):
    def test_emergency_jumps_to_front(self):
        atcs = ATCS()
        atcs.request_landing(Plane("A", 20, 50))
        atcs.request_landing(Plane("Mayday", 80, 90, emergency=True))
        self.assertEqual(atcs.land_next().name, "Mayday")

    def test_emergency_beats_lowest_fuel(self):
        pq = PriorityQueue()
        pq.enqueue(Plane("Empty", 2, 5))
        pq.enqueue(Plane("Fire", 100, 100, emergency=True))
        self.assertEqual(pq.peek().name, "Fire")

    def test_multiple_emergencies_ordered_among_themselves(self):
        pq = PriorityQueue()
        pq.enqueue(Plane("E1", 70, 40, emergency=True))
        pq.enqueue(Plane("E2", 10, 20, emergency=True))
        pq.enqueue(Plane("Normal", 5, 5))
        self.assertEqual(pq.dequeue().name, "E2")
        self.assertEqual(pq.dequeue().name, "E1")
        self.assertEqual(pq.dequeue().name, "Normal")

    def test_declaring_emergency_via_update_reorders(self):
        pq = PriorityQueue()
        far = Plane("Far", 60, 80)
        near = Plane("Near", 40, 10)
        pq.enqueue(far)
        pq.enqueue(near)
        self.assertEqual(pq.peek().name, "Near")
        pq.update(far, emergency=True)
        self.assertEqual(pq.peek().name, "Far")


class TestQueueOperations(unittest.TestCase):
    def test_peek_does_not_remove(self):
        pq = PriorityQueue()
        pq.enqueue(Plane("A", 20, 50))
        pq.peek()
        self.assertFalse(pq.is_empty())

    def test_empty_queue_returns_none(self):
        pq = PriorityQueue()
        self.assertIsNone(pq.dequeue())
        self.assertIsNone(pq.peek())

    def test_update_reorders_after_new_low_fuel_arrival(self):
        atcs = ATCS()
        a = Plane("A", 20, 50)
        atcs.request_landing(a)
        atcs.request_landing(Plane("B", 60, 30))
        self.assertEqual(atcs.land_next().name, "A")
        atcs.request_landing(Plane("New", 5, 40))
        self.assertEqual(atcs.queue.peek().name, "New")


class TestLandingLogIsLIFO(unittest.TestCase):
    def test_most_recent_landing_on_top(self):
        atcs = ATCS()
        atcs.request_landing(Plane("A", 20, 50))
        atcs.request_landing(Plane("B", 60, 30))
        atcs.land_next()
        atcs.land_next()
        self.assertEqual(atcs.log.most_recent().name, "B")

    def test_log_pops_in_reverse_order(self):
        log = LandingLog()
        log.push(Plane("A", 20, 50))
        log.push(Plane("B", 60, 30))
        self.assertEqual(log.pop().name, "B")
        self.assertEqual(log.pop().name, "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)

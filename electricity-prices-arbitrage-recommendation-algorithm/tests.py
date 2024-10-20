import unittest
from recommendation_algorithm import Battery

class TestRecommendationAlgorithm(unittest.TestCase):

    def test_up_and_down_trend(self):
        max_input_flow = 15
        max_output_flow = 15
        battery_level = 10

        battery = Battery(4, max_input_flow, max_output_flow)
        battery.set_objective([10,0,10,0])
        battery.add_storage_constraints(1, 0, 100, battery_level )
        battery.solve_model()
        charge_schedule, discharge_schedule = battery.collect_output()
        self.assertListEqual(charge_schedule.tolist(), [0, max_input_flow, 0, max_input_flow])
        self.assertListEqual(discharge_schedule.tolist(), [10, 0, max_output_flow, 0])
    
    def test_high_network_fees(self):
        battery = Battery(4, 15, 15)
        battery.set_objective([10,0,10,0],  network_fee=1000)
        battery.add_storage_constraints(1, 0, 100, 10,  )
        battery.solve_model()

        charge_schedule, discharge_schedule = battery.collect_output()
        self.assertListEqual(charge_schedule.tolist(), [0, 0, 0, 0])
        self.assertListEqual(discharge_schedule.tolist(), [0, 0, 0, 0])

    def test_huge_consumption(self):
        battery = Battery(4, 15, 15)
        battery.set_objective([0,10,15,0], network_fee=0.01)
        battery.add_storage_constraints(1, 0, 100, 10, consumption_profile=[15, 15, 15, 15] )
        battery.solve_model()

        charge_schedule, discharge_schedule = battery.collect_output()
        self.assertListEqual(charge_schedule.tolist(), [15, 15, 5, 15])
        self.assertListEqual(discharge_schedule.tolist(), [0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
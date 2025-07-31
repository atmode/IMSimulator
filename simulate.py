import simpy
import random
import csv
from collections import defaultdict
from datetime import datetime

# Simulation Parameters
SIM_DAYS = 507            
INITIAL_STOCK = 3         
MAX_CAPACITY = 110        
REORDER_LEVEL = 50        
ORDER_QUANTITY = 100      
RAND_RANGE = (1, 100)      

# (Table 19-2)
DEMAND_DIST = {
    'ranges': [
        (1, 10, 0),       # 10% chance of 0 units demand
        (11, 35, 1),      # 25% chance of 1 unit demand
        (36, 70, 2),      # 35% chance of 2 units demand
        (71, 91, 3),      # 11% chance of 3 units demand
        (92, 100, 4)      # 19% chance of 4 units demand
    ]
}

# (Table 20-2)
LEAD_TIME_DIST = {
    'ranges': [
        (1, 60, (1, 6)),  # 60% chance of 1-6 days lead time
        (61, 90, (7, 9)), # 30% chance of 7-9 days lead time
        (91, 100, 10)      # 10% chance of 10 days lead time
    ]
}

class InventorySystem:
    def __init__(self, env):
        self.env = env
        self.current_stock = INITIAL_STOCK
        self.on_order = False
        self.stats = defaultdict(list)
        self.shortage_days = 0
        self.orders = []
        
        # Initial order (1 unit after 2 days)
        self.env.process(self.receive_order(1, 2))

    def generate_value(self, distribution):
        
        rand_num = random.randint(*RAND_RANGE)
        for low, high, value in distribution['ranges']:
            if low <= rand_num <= high:
                return value if isinstance(value, int) else random.randint(*value)
        return 0

    def daily_demand(self):
        return self.generate_value(DEMAND_DIST)

    def generate_lead_time(self):
        return self.generate_value(LEAD_TIME_DIST)

    def receive_order(self, quantity, lead_time):
        yield self.env.timeout(lead_time)
        self.current_stock = min(self.current_stock + quantity, MAX_CAPACITY)
        self.on_order = False

    def daily_operation(self):
        while True:
            # Record beginning inventory
            self.stats['day'].append(self.env.now + 1)
            self.stats['beginning_stock'].append(self.current_stock)
            
            # Process demand
            demand = self.daily_demand()
            self.stats['demand'].append(demand)
            
            # Update inventory and shortages
            if self.current_stock >= demand:
                self.current_stock -= demand
                self.stats['shortage'].append(0)
                # No Demand 
            else:
                self.shortage_days += 1
                shortage = demand - self.current_stock
                self.stats['shortage'].append(shortage)
                self.current_stock = 0
            
            # Place new order if needed
            if not self.on_order and self.current_stock <= REORDER_LEVEL:
                lead_time = self.generate_lead_time()
                self.env.process(self.receive_order(ORDER_QUANTITY, lead_time))
                self.on_order = True
                self.orders.append((self.env.now + 1, ORDER_QUANTITY, lead_time))
            
            # Record ending inventory
            self.stats['ending_stock'].append(self.current_stock)
            
            yield self.env.timeout(1)

def run_simulation():
    env = simpy.Environment()
    system = InventorySystem(env)
    env.process(system.daily_operation())
    env.run(until=SIM_DAYS)
    
    avg_ending_stock = sum(system.stats['ending_stock']) / SIM_DAYS
    total_shortage = sum(system.stats['shortage'])
    total_ending_stock = sum(system.stats['ending_stock'])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"inventory_results_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Day', 'Beginning Stock', 'Demand', 'Shortage', 'Ending Stock']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for i in range(len(system.stats['day'])):
            writer.writerow({
                'Day': system.stats['day'][i],
                'Beginning Stock': system.stats['beginning_stock'][i],
                'Demand': system.stats['demand'][i],
                'Shortage': system.stats['shortage'][i],
                'Ending Stock': system.stats['ending_stock'][i]
            })
    

    print("\nSimulation Results:")
    print(f"Average Ending Stock: {avg_ending_stock:.2f} units")
    print(f"Total of Ending Stock: {total_ending_stock:.2f} units")
    print(f"Number of Shortage Days: {system.shortage_days} days")
    print(f"Number of Orders: {len(system.orders)}")
    print(f"Results saved to file: {filename}")

if __name__ == '__main__':
    run_simulation()

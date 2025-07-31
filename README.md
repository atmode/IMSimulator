# Inventory Management Simulation

## Overview

This Python script simulates an inventory management system using SimPy, a discrete-event simulation framework. The simulation models daily inventory operations including demand fluctuations, order placements, and lead time variations over a specified time period.

## Features

- **Discrete-event simulation** of inventory management processes
- **Probabilistic demand modeling** based on predefined distribution
- **Variable lead time** for order deliveries
- **Reorder point system** for inventory replenishment
- **Shortage tracking** to identify stockout situations
- **Comprehensive statistics** on inventory levels and performance
- **CSV export** of simulation results with timestamp

## Requirements

- Python 3.x
- SimPy
- Random (standard library)
- CSV (standard library)
- Collections (standard library)
- Datetime (standard library)

## Configuration Parameters

The simulation can be customized through several parameters:

```python
# Simulation Parameters
SIM_DAYS = 507            # Number of days to simulate
INITIAL_STOCK = 3         # Starting inventory level
MAX_CAPACITY = 110        # Maximum warehouse capacity
REORDER_LEVEL = 50        # Level at which new orders are placed
ORDER_QUANTITY = 100      # Fixed order quantity
RAND_RANGE = (1, 100)     # Range for random number generation
```

## Probability Distributions

### Demand Distribution

```
DEMAND_DIST = {
    'ranges': [
        (1, 10, 0),       # 10% chance of 0 units demand
        (11, 35, 1),      # 25% chance of 1 unit demand
        (36, 70, 2),      # 35% chance of 2 units demand
        (71, 91, 3),      # 11% chance of 3 units demand
        (92, 100, 4)      # 19% chance of 4 units demand
    ]
}
```

### Lead Time Distribution

```
LEAD_TIME_DIST = {
    'ranges': [
        (1, 60, (1, 6)),  # 60% chance of 1-6 days lead time
        (61, 90, (7, 9)), # 30% chance of 7-9 days lead time
        (91, 100, 10)     # 10% chance of 10 days lead time
    ]
}
```

## Usage

Simply run the script to execute the simulation:

```
python inventory_simulation.py
```

The simulation will run for the specified number of days and output:
- Average ending stock
- Total ending stock
- Number of shortage days
- Number of orders placed
- CSV file with detailed daily simulation data

## Output

The script generates a CSV file with the naming convention `inventory_results_YYYYMMDD_HHMMSS.csv` containing:
- Day number
- Beginning stock level
- Daily demand
- Shortage quantity (if any)
- Ending stock level

## How It Works

1. The simulation initializes with a starting inventory level
2. Each day:
   - Random demand is generated based on probability distribution
   - Inventory is reduced according to demand
   - Shortages are recorded if demand exceeds inventory
   - If inventory falls below reorder level, new order is placed
   - Order arrivals update inventory after lead time passes
3. Statistics are collected throughout the simulation
4. Results are printed and saved to CSV upon completion

## Example Use Cases

- Supply chain optimization
- Inventory policy analysis
- Risk assessment for stockout situations
- Cost-benefit analysis of different reorder points and quantities
- Analysis of demand pattern impacts on inventory levels
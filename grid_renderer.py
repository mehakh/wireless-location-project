import matplotlib
matplotlib.use('TkAgg') # Or 'Qt5Agg'

import numpy as np
import matplotlib.pyplot as plt
from database import DatabaseConnection

class GridRenderer:
    def __init__(self):
        self.db = DatabaseConnection()
        self.measurements = []
        self.grid_data = None
        self.x_values = []
        self.y_values = []
    
    def load_measurements(self):
        """Load measurement points from database"""
        self.db.connect()
        
        # Query all measurements from matavimai table
        query = "SELECT x, y FROM matavimai ORDER BY x, y"
        self.measurements = self.db.execute_query(query)
        
        self.db.disconnect()
        
        if self.measurements:
            print(f"✓ Loaded {len(self.measurements)} measurement points")
            return True
        else:
            print("✗ No measurements found")
            return False
    
    def create_grid(self):
        """Create grid representation of measurements"""
        if not self.measurements:
            print("✗ No measurements loaded. Call load_measurements() first.")
            return False
        
        # Extract x and y coordinates
        self.x_values = sorted(list(set([m['x'] for m in self.measurements])))
        self.y_values = sorted(list(set([m['y'] for m in self.measurements])))
        
        # Create 2D grid where 1 = measurement exists, 0 = no measurement
        grid = np.zeros((len(self.y_values), len(self.x_values)))
        
        # Mark cells with measurements
        for measurement in self.measurements:
            x_idx = self.x_values.index(measurement['x'])
            y_idx = self.y_values.index(measurement['y'])
            grid[y_idx, x_idx] = 1
        
        self.grid_data = grid
        print(f"✓ Grid created: {len(self.x_values)} columns × {len(self.y_values)} rows")
        return True
    
    def visualize_grid(self, user_location=None):
        """Display the grid and optionally highlight the user's location."""
        if self.grid_data is None:
            print("✗ Grid not created. Call create_grid() first.")
            return

        plt.figure(figsize=(12, 10))
        plt.imshow(self.grid_data, cmap='Blues', origin='lower', aspect='auto')
        plt.grid(True, alpha=0.3)
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Wireless Network Measurement Points Grid')
        cbar = plt.colorbar()
        cbar.set_label('Measurement Status (1=Measured, 0=Not Measured)')
        plt.xticks(range(len(self.x_values)), self.x_values, rotation=45)
        plt.yticks(range(len(self.y_values)), self.y_values)

        # --- NEW CODE TO HIGHLIGHT USER LOCATION ---
        if user_location:
            try:
                # Find the index of the user's x and y coordinates
                user_x, user_y = user_location
                x_idx = self.x_values.index(user_x)
                y_idx = self.y_values.index(user_y)

                # Plot a large red 'X' on the specified coordinates
                plt.scatter(x_idx, y_idx, s=200, c='red', marker='X', label=f'User Location ({user_x}, {user_y})')
                plt.legend()
                print(f"✓ Highlighting user location at coordinates ({user_x}, {user_y}) on the grid.")

            except (ValueError, IndexError):
                print(f"✗ Warning: Calculated location ({user_location}) is outside the known grid and cannot be shown.")
        # --- END OF NEW CODE ---

        plt.tight_layout()
        plt.show()

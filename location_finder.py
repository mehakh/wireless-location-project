import numpy as np
from database import DatabaseConnection

class LocationFinder:
    def __init__(self):
        self.db = DatabaseConnection()
        self.signal_map = {}  # Dictionary: (x, y) -> {sensor: strength}
        self.measurement_points = []
    
    def load_signal_strength_map(self):
        """Load all signal strength measurements from database"""
        self.db.connect()
        
        # Query all measurements with their signal strengths
        query = """
        SELECT m.x, m.y, s.sensorius, s.stiprumas
        FROM matavimai m
        JOIN stiprumai s ON m.matavimas = s.matavimas
        ORDER BY m.x, m.y, s.sensorius
        """
        
        results = self.db.execute_query(query)
        self.db.disconnect()
        
        if not results:
            print("✗ No signal strength data found")
            return False
        
        # Organize data into a map: (x, y) -> {sensor: strength}
        for row in results:
            point = (row['x'], row['y'])
            sensor = row['sensorius']
            strength = row['stiprumas']
            
            if point not in self.signal_map:
                self.signal_map[point] = {}
            
            self.signal_map[point][sensor] = strength
        
        self.measurement_points = list(self.signal_map.keys())
        print(f"✓ Loaded signal strength map with {len(self.measurement_points)} points")
        return True
    
    def calculate_distance(self, signal_vector1, signal_vector2):
        """
        Calculate Euclidean distance between two signal strength vectors
        
        Args:
            signal_vector1: Dict of sensor strengths {sensor: strength}
            signal_vector2: Dict of sensor strengths {sensor: strength}
        
        Returns:
            Float: Euclidean distance
        """
        # Get all common sensors
        common_sensors = set(signal_vector1.keys()) & set(signal_vector2.keys())
        
        if not common_sensors:
            return float('inf')
        
        # Calculate sum of squared differences
        sum_squared_diff = 0
        for sensor in common_sensors:
            diff = signal_vector1[sensor] - signal_vector2[sensor]
            sum_squared_diff += diff ** 2
        
        # Return square root (Euclidean distance)
        return np.sqrt(sum_squared_diff)
    
    def find_user_location(self, user_signals):
        """
        Find user location using nearest neighbor search
        
        Args:
            user_signals: Dict of signal strengths {sensor: strength}
        
        Returns:
            Tuple: (x, y) coordinates of nearest measurement point
        """
        if not self.measurement_points:
            print("✗ Signal map not loaded")
            return None
        
        min_distance = float('inf')
        nearest_point = None
        
        # Compare with all measurement points
        for point in self.measurement_points:
            distance = self.calculate_distance(
                user_signals,
                self.signal_map[point]
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
        
        print(f"✓ User located at: ({nearest_point[0]}, {nearest_point[1]})")
        print(f"  Distance score: {min_distance:.2f}")
        return nearest_point
    
    def get_user_signal_strength(self, mac_address):
        """
        Get signal strength readings for a specific MAC address
        
        Args:
            mac_address: String MAC address (format: XX:XX:XX:XX:XX:XX)
        
        Returns:
            Dict: {sensor: strength} or None if not found
        """
        self.db.connect()
        
        query = f"SELECT sensorius, stiprumas FROM vartotojai WHERE mac = '{mac_address}'"
        results = self.db.execute_query(query)
        
        self.db.disconnect()
        
        if not results:
            print(f"✗ No data found for MAC address: {mac_address}")
            return None
        
        # Convert to signal strength dictionary
        signals = {row['sensorius']: row['stiprumas'] for row in results}
        print(f"✓ Signal strengths for {mac_address}: {signals}")
        return signals


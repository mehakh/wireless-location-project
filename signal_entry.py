from location_finder import LocationFinder

class SignalEntry:
    def __init__(self):
        self.location_finder = LocationFinder()
        self.location_finder.load_signal_strength_map()
    
    def enter_signal_manually(self):
        """Interactive input for MAC address and signal strengths"""
        print("\n" + "="*50)
        print("MANUAL SIGNAL STRENGTH ENTRY")
        print("="*50)
        
        # Get MAC address
        mac_address = input("Enter MAC address (format: XX:XX:XX:XX:XX:XX): ")
        
        # Get signal strengths for each sensor
        signals = {}
        print("\nEnter signal strengths for each access point:")
        print("(Enter -100 to -30, where -30 is strongest, -100 is weakest)")
        
        # Get available sensors from database
        sensors = set()
        for point_signals in self.location_finder.signal_map.values():
            sensors.update(point_signals.keys())
        
        for sensor in sorted(sensors):
            while True:
                try:
                    strength = int(input(f"Signal strength for {sensor} (dBm): "))
                    if -100 <= strength <= -30:
                        signals[sensor] = strength
                        break
                    else:
                        print("✗ Please enter value between -100 and -30")
                except ValueError:
                    print("✗ Please enter a valid integer")
        
        return mac_address, signals
    
    def process_user_location(self):
        """Main function to get user location"""
        mac_address, signals = self.enter_signal_manually()
        
        print("\n" + "="*50)
        print("PROCESSING LOCATION...")
        print("="*50)
        
        location = self.location_finder.find_user_location(signals)
        
        if location:
            print(f"\n✓ USER LOCATION DETERMINED:")
            print(f"  MAC Address: {mac_address}")
            print(f"  Coordinates: X={location[0]}, Y={location[1]}")
        else:
            print("✗ Could not determine location")

# Usage
if __name__ == "__main__":
    entry = SignalEntry()
    entry.process_user_location()

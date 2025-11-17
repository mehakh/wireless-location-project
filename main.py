# main.py

from database import DatabaseConnection
from grid_renderer import GridRenderer
from location_finder import LocationFinder
from signal_entry import SignalEntry

def display_menu():
    """Prints the main menu and returns the user's choice."""
    print("\n" + "="*60)
    print("      WIRELESS NETWORK USER LOCATION STUDY - PART 1")
    print("="*60)
    print("  1. Test Database Connection")
    print("  2. View Full Measurement Grid")
    print("  3. Locate User from Database and Show on Grid")
    print("  4. Enter Manual Signals and Locate User on Grid")
    print("  5. Exit")
    print("="*60)
    choice = input("  Select an option (1-5): ")
    return choice

def option_1_test_connection():
    """Tests the connection to the database."""
    print("\n--- Testing Database Connection ---")
    db = DatabaseConnection()
    if db.connect():
        # A simple query to confirm the connection is active and tables are accessible
        query = "SELECT COUNT(*) as count FROM matavimai"
        result = db.execute_query(query)
        if result:
            print(f"✓ Success! Database contains {result[0]['count']} measurement points.")
        db.disconnect()
    else:
        print("✗ Connection failed. Check your internet and the details in config.py.")

def option_2_view_grid(user_location=None):
    """
    Loads and displays the grid of all measurement points.
    Optionally highlights a user's location if provided.
    """
    if user_location:
        print("\n--- Loading Grid and Highlighting User Location ---")
    else:
        print("\n--- Loading and Displaying Full Measurement Grid ---")
        
    renderer = GridRenderer()
    if renderer.load_measurements():
        if renderer.create_grid():
            # Pass the location (or None) to the visualizer
            renderer.visualize_grid(user_location)

def option_3_locate_user():
    """Fetches a user from the database, calculates their location, and shows it on the grid."""
    print("\n--- Locate User from Database ---")
    db = DatabaseConnection()
    db.connect()
    # Query for distinct MAC addresses to show the user some available options
    macs = db.execute_query("SELECT DISTINCT mac FROM vartotojai")
    db.disconnect()
    
    if macs:
        print("Available MAC addresses in the database (showing up to 5):")
        for i, entry in enumerate(macs[:5], 1):
            print(f"  {i}. {entry['mac']}")
        if len(macs) > 5:
            print("  ...")
        
        mac_to_find = input("Enter the full MAC address to locate: ")
        
        location_finder = LocationFinder()
        if location_finder.load_signal_strength_map():
            signals = location_finder.get_user_signal_strength(mac_to_find)
            
            if signals:
                location = location_finder.find_user_location(signals)
                if location:
                    # If a location is found, call the grid view function
                    # and pass the location to be highlighted.
                    option_2_view_grid(user_location=location)
    else:
        print("✗ No users found in the 'vartotojai' database table.")

def option_4_manual_entry():
    """Allows manual entry of signal strengths to find and show a location."""
    print("\n--- Manual Signal Entry and Location ---")
    entry_system = SignalEntry()

    # The enter_signal_manually method handles the user input process
    mac_address, signals = entry_system.enter_signal_manually()

    print("\n" + "="*50)
    print("      PROCESSING LOCATION...")
    print("="*50)
    
    # Use the signals to find the location
    location = entry_system.location_finder.find_user_location(signals)
    
    if location:
        print(f"\n✓ USER LOCATION DETERMINED:")
        print(f"  MAC Address: {mac_address}")
        print(f"  Coordinates: X={location[0]}, Y={location[1]}")
        
        # Show the determined location on the grid
        option_2_view_grid(user_location=location)
    else:
        print("✗ Could not determine location. The signal vector may not have matched any grid points.")

def main():
    """The main loop of the application."""
    while True:
        choice = display_menu()
        
        if choice == '1':
            option_1_test_connection()
        elif choice == '2':
            # Shows the grid without any specific user location highlighted
            option_2_view_grid()
        elif choice == '3':
            option_3_locate_user()
        elif choice == '4':
            option_4_manual_entry()
        elif choice == '5':
            print("\nExiting the application. Goodbye!")
            break
        else:
            print("\n✗ Invalid option. Please enter a number from 1 to 5.")

# This ensures the main() function is called only when the script is executed directly
if __name__ == "__main__":
    main()

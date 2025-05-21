import re
from collections import defaultdict

def analyze_hide_and_seek(log_text):
    # Initialize counters
    hider_positions = defaultdict(int)
    seeker_positions = defaultdict(int)
    
    # Regular expressions to extract positions
    hider_pattern = r'Hider position: \((\d+),(\d+)\)'
    seeker_pattern = r'Seeker position: \((\d+),(\d+)\)'
    
    # Process each line
    for line in log_text.split('\n'):
        # Check for hider position
        hider_match = re.search(hider_pattern, line)
        if hider_match:
            x, y = map(int, hider_match.groups())
            hider_positions[(x, y)] += 1
        
        # Check for seeker position
        seeker_match = re.search(seeker_pattern, line)
        if seeker_match:
            x, y = map(int, seeker_match.groups())
            seeker_positions[(x, y)] += 1
    
    # Convert to sorted lists for display
    hider_counts = sorted(hider_positions.items(), key=lambda item: (-item[1], item[0]))
    seeker_counts = sorted(seeker_positions.items(), key=lambda item: (-item[1], item[0]))
    
    return hider_counts, seeker_counts

# Example usage with your log data
log_data = """Hide and Seek Simulation - 100 rounds (Zero-Sum)
World Size: 16
Proximity Effects: OFF
Grid: 2D
Human Role: hider

=== Round-by-Round Results ===

Round 1:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 1.000
  Total points of Computer: -1.000

Round 2:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 2.000
  Total points of Computer: -2.000

Round 3:
  Hider position: (2,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 4.000
  Total points of Computer: -4.000

Round 4:
  Hider position: (4,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 5.000
  Total points of Computer: -5.000

Round 5:
  Hider position: (3,4) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 7.000
  Total points of Computer: -7.000

Round 6:
  Hider position: (3,4) (Easy)
  Seeker position: (3,4)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 6.000
  Total points of Computer: -6.000

Round 7:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 7.000
  Total points of Computer: -7.000

Round 8:
  Hider position: (4,1) (Hard)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 8.000
  Total points of Computer: -8.000

Round 9:
  Hider position: (2,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 10.000
  Total points of Computer: -10.000

Round 10:
  Hider position: (2,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 12.000
  Total points of Computer: -12.000

Round 11:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 13.000
  Total points of Computer: -13.000

Round 12:
  Hider position: (2,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 15.000
  Total points of Computer: -15.000

Round 13:
  Hider position: (3,4) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 17.000
  Total points of Computer: -17.000

Round 14:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 18.000
  Total points of Computer: -18.000

Round 15:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 19.000
  Total points of Computer: -19.000

Round 16:
  Hider position: (2,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 21.000
  Total points of Computer: -21.000

Round 17:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 20.000
  Total points of Computer: -20.000

Round 18:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 21.000
  Total points of Computer: -21.000

Round 19:
  Hider position: (3,4) (Easy)
  Seeker position: (3,4)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 20.000
  Total points of Computer: -20.000

Round 20:
  Hider position: (3,4) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 22.000
  Total points of Computer: -22.000

Round 21:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 21.000
  Total points of Computer: -21.000

Round 22:
  Hider position: (4,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 22.000
  Total points of Computer: -22.000

Round 23:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 23.000
  Total points of Computer: -23.000

Round 24:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 25.000
  Total points of Computer: -25.000

Round 25:
  Hider position: (2,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 24.000
  Total points of Computer: -24.000

Round 26:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 25.000
  Total points of Computer: -25.000

Round 27:
  Hider position: (1,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 26.000
  Total points of Computer: -26.000

Round 28:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 27.000
  Total points of Computer: -27.000

Round 29:
  Hider position: (3,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 29.000
  Total points of Computer: -29.000

Round 30:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 30.000
  Total points of Computer: -30.000

Round 31:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 31.000
  Total points of Computer: -31.000

Round 32:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 33.000
  Total points of Computer: -33.000

Round 33:
  Hider position: (3,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 35.000
  Total points of Computer: -35.000

Round 34:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 36.000
  Total points of Computer: -36.000

Round 35:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 35.000
  Total points of Computer: -35.000

Round 36:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 36.000
  Total points of Computer: -36.000

Round 37:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 38.000
  Total points of Computer: -38.000

Round 38:
  Hider position: (3,4) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 40.000
  Total points of Computer: -40.000

Round 39:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 41.000
  Total points of Computer: -41.000

Round 40:
  Hider position: (1,1) (Hard)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 42.000
  Total points of Computer: -42.000

Round 41:
  Hider position: (1,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 43.000
  Total points of Computer: -43.000

Round 42:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 44.000
  Total points of Computer: -44.000

Round 43:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 45.000
  Total points of Computer: -45.000

Round 44:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 46.000
  Total points of Computer: -46.000

Round 45:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 47.000
  Total points of Computer: -47.000

Round 46:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 48.000
  Total points of Computer: -48.000

Round 47:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 49.000
  Total points of Computer: -49.000

Round 48:
  Hider position: (3,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 51.000
  Total points of Computer: -51.000

Round 49:
  Hider position: (3,4) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 53.000
  Total points of Computer: -53.000

Round 50:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 54.000
  Total points of Computer: -54.000

Round 51:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 56.000
  Total points of Computer: -56.000

Round 52:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 57.000
  Total points of Computer: -57.000

Round 53:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 58.000
  Total points of Computer: -58.000

Round 54:
  Hider position: (1,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 59.000
  Total points of Computer: -59.000

Round 55:
  Hider position: (2,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 58.000
  Total points of Computer: -58.000

Round 56:
  Hider position: (2,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 60.000
  Total points of Computer: -60.000

Round 57:
  Hider position: (3,4) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 62.000
  Total points of Computer: -62.000

Round 58:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 63.000
  Total points of Computer: -63.000

Round 59:
  Hider position: (2,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 62.000
  Total points of Computer: -62.000

Round 60:
  Hider position: (2,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 64.000
  Total points of Computer: -64.000

Round 61:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 66.000
  Total points of Computer: -66.000

Round 62:
  Hider position: (2,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 65.000
  Total points of Computer: -65.000

Round 63:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 66.000
  Total points of Computer: -66.000

Round 64:
  Hider position: (3,4) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 68.000
  Total points of Computer: -68.000

Round 65:
  Hider position: (3,4) (Easy)
  Seeker position: (3,4)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 67.000
  Total points of Computer: -67.000

Round 66:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 68.000
  Total points of Computer: -68.000

Round 67:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 69.000
  Total points of Computer: -69.000

Round 68:
  Hider position: (3,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 71.000
  Total points of Computer: -71.000

Round 69:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 72.000
  Total points of Computer: -72.000

Round 70:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 73.000
  Total points of Computer: -73.000

Round 71:
  Hider position: (1,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 74.000
  Total points of Computer: -74.000

Round 72:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 75.000
  Total points of Computer: -75.000

Round 73:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 76.000
  Total points of Computer: -76.000

Round 74:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 77.000
  Total points of Computer: -77.000

Round 75:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 78.000
  Total points of Computer: -78.000

Round 76:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 79.000
  Total points of Computer: -79.000

Round 77:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 80.000
  Total points of Computer: -80.000

Round 78:
  Hider position: (1,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 81.000
  Total points of Computer: -81.000

Round 79:
  Hider position: (3,2) (Easy)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 83.000
  Total points of Computer: -83.000

Round 80:
  Hider position: (4,1) (Hard)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 84.000
  Total points of Computer: -84.000

Round 81:
  Hider position: (4,1) (Hard)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 85.000
  Total points of Computer: -85.000

Round 82:
  Hider position: (2,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 87.000
  Total points of Computer: -87.000

Round 83:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 88.000
  Total points of Computer: -88.000

Round 84:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 87.000
  Total points of Computer: -87.000

Round 85:
  Hider position: (1,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 88.000
  Total points of Computer: -88.000

Round 86:
  Hider position: (3,4) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 90.000
  Total points of Computer: -90.000

Round 87:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 91.000
  Total points of Computer: -91.000

Round 88:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 90.000
  Total points of Computer: -90.000

Round 89:
  Hider position: (3,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 89.000
  Total points of Computer: -89.000

Round 90:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 90.000
  Total points of Computer: -90.000

Round 91:
  Hider position: (4,1) (Hard)
  Seeker position: (3,4)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 91.000
  Total points of Computer: -91.000

Round 92:
  Hider position: (2,3) (Neutral)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 92.000
  Total points of Computer: -92.000

Round 93:
  Hider position: (2,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 94.000
  Total points of Computer: -94.000

Round 94:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 95.000
  Total points of Computer: -95.000

Round 95:
  Hider position: (4,1) (Hard)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 96.000
  Total points of Computer: -96.000

Round 96:
  Hider position: (3,4) (Easy)
  Seeker position: (3,4)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 95.000
  Total points of Computer: -95.000

Round 97:
  Hider position: (2,2) (Easy)
  Seeker position: (3,2)
  RESULT: Hider not found
  Human points: 2.0
  Computer points: -2.0
  Winner: Human
  Total points of Human: 97.000
  Total points of Computer: -97.000

Round 98:
  Hider position: (2,3) (Neutral)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 98.000
  Total points of Computer: -98.000

Round 99:
  Hider position: (2,2) (Easy)
  Seeker position: (2,2)
  RESULT: Hider found!
  Human points: -1.0
  Computer points: 1.0
  Winner: Computer
  Total points of Human: 97.000
  Total points of Computer: -97.000

Round 100:
  Hider position: (1,1) (Hard)
  Seeker position: (2,2)
  RESULT: Hider not found
  Human points: 1.0
  Computer points: -1.0
  Winner: Human
  Total points of Human: 98.000
  Total points of Computer: -98.000

=== Simulation Summary ===
Total Rounds: 100
Human Score: 98.000
Computer Score: -98.000
Human Wins: 85 (85.000%)
Computer Wins: 15 (15.000%)
Net Score (Human - Computer): 196.000

"""

hider_counts, seeker_counts = analyze_hide_and_seek(log_data)

print("Hider Position Counts:")
for pos, count in hider_counts:
    print(f"  {pos}: {count} times")

print("\nSeeker Position Counts:")
for pos, count in seeker_counts:
    print(f"  {pos}: {count} times")

# Verification
total_hider = sum(count for _, count in hider_counts)
total_seeker = sum(count for _, count in seeker_counts)
print(f"\nVerification: Hider total = {total_hider}, Seeker total = {total_seeker}")
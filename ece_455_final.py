import sys
import math

def gcd(a, b):
    """Compute the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the least common multiple of a and b."""
    if a == 0 or b == 0:
        return 0
    return abs(a*b) // gcd(a, b) if a and b else 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python ece_455_final.py <input_filename>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    tasks = []
    try:
        with open(input_filename, 'r') as f:
            for i, line in enumerate(f):
                try:
                    execution_time_str, period_str, relative_deadline_str = line.strip().split(',')
                    execution_time = int(float(execution_time_str) * 1000)
                    period = int(float(period_str) * 1000)
                    relative_deadline = int(float(relative_deadline_str) * 1000)
                    tasks.append({
                        'id': f'T_{i}',
                        'execution_time': execution_time,
                        'period': period,
                        'relative_deadline': relative_deadline
                    })
                except ValueError:
                    print(f"Warning: Skipping malformed line {i+1} in {input_filename}")
        print(f"Successfully parsed {len(tasks)} tasks.")

        hyperperiod_limit = 1
        if tasks:
            hyperperiod_limit = tasks[0]['period']
            for i in range(1, len(tasks)):
                hyperperiod_limit = lcm(hyperperiod_limit, tasks[i]['period'])
        
        print(f"Calculated hyperperiod limit: {hyperperiod_limit}")

    except FileNotFoundError:
        print(f"Error: File not found at {input_filename}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

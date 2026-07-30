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
                        'relative_deadline': relative_deadline,
                        'remaining_execution_time': execution_time,
                        'next_release_time': 0,
                        'absolute_deadline': relative_deadline,
                        'preemption_count': 0
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

        current_time = 0
        last_running_task_id = None

        while current_time < hyperperiod_limit:
            for task in tasks:
                # Check for missed deadlines
                if current_time > task['absolute_deadline'] and task['remaining_execution_time'] > 0:
                    print(f"Error: Task {task['id']} missed its deadline at time {current_time}")
                    sys.exit(1)

                # Update absolute deadline if a new job is released
                if current_time >= task['next_release_time'] and task['remaining_execution_time'] == task['execution_time']:
                    task['absolute_deadline'] = current_time + task['relative_deadline']
            
            ready_tasks = []
            for task in tasks:
                if current_time >= task['next_release_time'] and task['remaining_execution_time'] > 0:
                    ready_tasks.append(task)
            
            if ready_tasks:
                ready_tasks.sort(key=lambda t: t['period'])
                highest_priority_task = ready_tasks[0]

                if last_running_task_id is not None and highest_priority_task['id'] != last_running_task_id:
                    # Find the task that was just preempted and increment its counter
                    for task in tasks:
                        if task['id'] == last_running_task_id and task['remaining_execution_time'] > 0:
                            task['preemption_count'] += 1
                            break
                
                highest_priority_task['remaining_execution_time'] -= 1
                last_running_task_id = highest_priority_task['id']

                if highest_priority_task['remaining_execution_time'] == 0:
                    highest_priority_task['next_release_time'] += highest_priority_task['period']
                    highest_priority_task['remaining_execution_time'] = highest_priority_task['execution_time']
                    highest_priority_task['absolute_deadline'] = highest_priority_task['next_release_time'] + highest_priority_task['relative_deadline']

            else:
                last_running_task_id = None # No task running

            current_time += 1

        print("Simulation complete.")
        for task in tasks:
            print(f"Task {task['id']}: Preemptions = {task['preemption_count']}")

    except FileNotFoundError:
        print(f"Error: File not found at {input_filename}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

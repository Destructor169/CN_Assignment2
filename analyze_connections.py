import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Load extracted data
data = pd.read_csv('connections.txt', sep='\t', engine='python', on_bad_lines='skip')

# Dictionary to track connection details
connection_times = defaultdict(lambda: {'start': None, 'end': None, 'has_fin_ack': False})

# Tracking SYN packets for potential SYN flood detection
syn_counts = defaultdict(int)

# Identify start, end, and SYN flood risks
for _, row in data.iterrows():
    conn_key = (row['src_ip'], row['dst_ip'], row['src_port'], row['dst_port'])

    # Track SYN packets for SYN flood detection
    if 'S' in row['flags'] and 'A' not in row['flags']:
        syn_counts[conn_key] += 1  # Possible SYN flood attempt

    # Connection start (SYN)
    if 'S' in row['flags'] and 'A' not in row['flags']:
        if connection_times[conn_key]['start'] is None:
            connection_times[conn_key]['start'] = row['start_time']

    # Connection end (ACK after FIN-ACK or RESET)
    if 'F' in row['flags'] and 'A' in row['flags']:
        connection_times[conn_key]['has_fin_ack'] = True
    if 'R' in row['flags'] or ('F' in row['flags'] and connection_times[conn_key]['has_fin_ack']):
        connection_times[conn_key]['end'] = row['start_time']

# Calculate connection durations
durations = []
start_times = []
for conn, times in connection_times.items():
    if times['start']:
        start_time = float(times['start'])
        end_time = float(times['end']) if times['end'] else start_time + 100  # Default 100s if no proper closure
        duration = end_time - start_time

        durations.append(duration)
        start_times.append(start_time)

# Plotting Connection Duration vs. Start Time
plt.figure(figsize=(10, 6))
plt.scatter(start_times, durations, label='Connection Duration')

# Marking potential SYN flood attack
if syn_counts:
    attack_start = min(start_times)  # Assume attack started at the earliest connection
    attack_end = max(start_times)   # Assume attack ended at the latest connection
    plt.axvline(x=attack_start, color='red', linestyle='--', label='Attack Start')
    plt.axvline(x=attack_end, color='green', linestyle='--', label='Attack End')

plt.xlabel('Connection Start Time (Seconds)')
plt.ylabel('Connection Duration (Seconds)')
plt.title('Connection Duration vs. Start Time')
plt.legend()
plt.grid(True)
plt.savefig('connection_analysis_plot.png')
plt.show()

print("✅ Analysis complete. Results saved as 'connection_analysis_plot.png'")
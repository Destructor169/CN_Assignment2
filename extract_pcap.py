from scapy.all import PcapReader, TCP
import pandas as pd

# Load pcap file in chunks
data = []
chunk_size = 100000  # Define chunk size
chunk_count = 0      # Track number of chunks

with PcapReader('capture.pcap') as packets:
    for pkt in packets:
        if pkt.haslayer(TCP):  # Only consider TCP packets
            data.append({
                'src_ip': pkt['IP'].src,
                'dst_ip': pkt['IP'].dst,
                'src_port': pkt[TCP].sport,
                'dst_port': pkt[TCP].dport,
                'start_time': pkt.time,
                'flags': pkt[TCP].flags  # Extract TCP flags
            })

        # Write data in chunks to avoid memory overflow
        if len(data) >= chunk_size:
            pd.DataFrame(data).to_csv(
                'connections.txt', 
                sep='\t', 
                mode='a', 
                header=not pd.io.common.file_exists('connections.txt'), 
                index=False
            )
            chunk_count += 1
            print(f"✅ Processed {chunk_count * chunk_size} packets so far...")
            data.clear()  # Clear list for next batch

# Final write for remaining packets
if data:
    pd.DataFrame(data).to_csv(
        'connections.txt', 
        sep='\t', 
        mode='a', 
        header=not pd.io.common.file_exists('connections.txt'), 
        index=False
    )
    print(f"✅ Final batch processed. Total packets processed: {chunk_count * chunk_size + len(data)}")

print("✅ Data extraction complete! Saved to 'connections.txt'")

# CS 331: Computer Networks - Assignment 2

## Submission Details
- **Deadline:** Before 08-03-2025, 11:59 PM
- **Teamwork:** The assignment must be completed in pairs of two students. Only one team member (Member 1) must submit the assignment on behalf of the group.
- **Submission Format:** Report should be named as `TeamID-RollNumber1_RollNumber2.pdf` (e.g., `1-23210122_23210023.pdf`).
- **GitHub Repository:** Include a link to your GitHub repository containing all the programs and scripts used for the assignment.

## Protocol Assignment Scheme
Each team will work on three congestion control protocols based on their team number using the following formula:

1. **Protocol 1** → (team_number % 10)
2. **Protocol 2** → ((team_number + 3) % 10)
3. **Protocol 3** → ((team_number + 6) % 10)

### List of Available Protocols:
| Protocol No. | Protocol |
|-------------|----------|
| 0 | Reno |
| 1 | CUBIC |
| 2 | BBR |
| 3 | BIC |
| 4 | Vegas |
| 5 | Westwood |
| 6 | HighSpeed |
| 7 | H-TCP |
| 8 | Scalable |
| 9 | Yeah |

---
## Task-1: Comparison of Congestion Control Protocols (50 Points)

### Mininet Topology Setup
- Create a **Mininet topology** as shown in the provided diagram.
- Hosts H1 to H6 are **TCP clients**, and H7 is the **TCP server**.
- Run an **iPerf3 client-server setup** to generate TCP traffic.

#### Experiments
##### (a) Run the client on H1 and the server on H7. Measure the following parameters:
1. **Throughput over time** (Wireshark I/O graphs)
2. **Goodput**
3. **Packet loss rate**
4. **Maximum window size achieved** (Wireshark I/O graphs)

##### (b) Run clients on H1, H3, and H4 in a staggered manner:
- H1 starts at T=0s, runs for 150s.
- H3 starts at T=15s, runs for 120s.
- H4 starts at T=30s, runs for 90s.
- Server runs on H7.
- Measure and analyze the parameters as in part (a) for all three congestion schemes.

##### (c) Configure the links with specific bandwidths:
- **Link S1-S2:** 100 Mbps
- **Link S2-S3:** 50 Mbps
- **Link S3-S4:** 100 Mbps

Analyze performance for these conditions:
1. Link S2-S4 active with client on H3 and server on H7.
2. Link S1-S4 active:
   - (i) Clients: H1, H2 → Server: H7
   - (ii) Clients: H1, H3 → Server: H7
   - (iii) Clients: H1, H3, H4 → Server: H7

##### (d) Configure **1% and 5% link loss** on S2-S3 and repeat part (c).

---
## Task-2: Implementation and Mitigation of SYN Flood Attack (100 Points)

### **(A) Implementation of SYN Flood Attack**
1. Modify the **Linux kernel** settings of the receiver (server) to optimize the attack:
   - `net.ipv4.tcp_max_syn_backlog`
   - `net.ipv4.tcp_syncookies`
   - `net.ipv4.tcp_synack_retries`
2. Experiment Steps:
   - Start **packet capture** on the client using `tcpdump`.
   - Start **legitimate traffic**.
   - After **20 seconds**, start the **attack**.
   - Stop the attack after **100 seconds**.
   - After **20 more seconds**, stop the legitimate traffic.
   - Stop `tcpdump` and save the file.

#### Analyze the output PCAP file and:
- Calculate **connection duration** for each TCP connection.
- Define connection duration as:
  - Time from **first SYN** to **ACK after FIN-ACK**.
  - Or, time from **first SYN** to **first RESET** if no FIN-ACK.
  - Default **100 seconds** if no ACK is found.
- Plot **connection duration vs. connection start time**.
- Mark **attack start and end times** on the plot.
- Attach **Wireshark screenshots** showing packet status.

### **(B) SYN Flood Attack Mitigation**
- Implement **any SYN flood mitigation strategy**.
- Repeat the **same experiment** as in part (A).
- Compare **before and after mitigation** using:
  - **Graphs of connection duration vs. connection start time**.
  - **Wireshark screenshots**.

---
## Task-3: Effect of Nagle’s Algorithm on TCP/IP Performance (50 Points)

### **Experiment Setup**
- Transmit a **4 KB file** over a TCP connection for **~2 minutes** at **40 bytes/sec**.
- Perform **four configurations**:

| Nagle’s Algorithm | Delayed-ACK |
|-------------------|------------|
| Enabled | Enabled |
| Enabled | Disabled |
| Disabled | Enabled |
| Disabled | Disabled |

### **Measure and compare the following performance metrics:**
1. **Throughput**
2. **Goodput**
3. **Packet loss rate**
4. **Maximum packet size achieved**

---
## References
- [Mininet Walkthrough](https://mininet.org/walkthrough/)
- [Mininet Examples](https://github.com/mininet/mininet/tree/master/examples)
- [iPerf Documentation](https://iperf.fr/)

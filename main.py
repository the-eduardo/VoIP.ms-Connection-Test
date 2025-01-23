import socket
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

# voip.ms servers mapping with both domain and IP addresses
# Format: 'server_domain': ('server_ip', 'server_location')
voip_servers = {
    # Atlanta Servers
    'atlanta1.voip.ms': ('208.100.60.17', 'Atlanta 1, GA'),
    'atlanta2.voip.ms': ('208.100.60.18', 'Atlanta 2, GA'),

    # Chicago Servers
    'chicago1.voip.ms': ('208.100.60.8', 'Chicago, IL'),
    'chicago2.voip.ms': ('208.100.60.9', 'Chicago 2, IL'),
    'chicago3.voip.ms': ('208.100.60.10', 'Chicago 3, IL'),
    'chicago4.voip.ms': ('208.100.60.6', 'Chicago 4, IL'),

    # Dallas Servers
    'dallas1.voip.ms': ('208.100.60.29', 'Dallas 1, TX'),
    'dallas2.voip.ms': ('208.100.60.30', 'Dallas2,TX'),

    # Denver Servers
    'denver1.voip.ms': ('208.100.60.32', 'Denver 1, CO'),
    'denver2.voip.ms': ('208.100.60.33', 'Denver 2, CO'),

    # Fax Servers
    'fax1.voip.ms': ('208.100.60.81', 'Fax Server 1'),
    'fax2.voip.ms': ('208.100.60.82', 'Fax Server 2'),

    # Houston Servers
    'houston1.voip.ms': ('208.100.60.15', 'Houston 1, TX'),
    'houston2.voip.ms': ('208.100.60.16', 'Houston 2, TX'),

    # Los Angeles Servers
    'losangeles1.voip.ms': ('208.100.60.35', 'Los Angeles 1, CA'),
    'losangeles2.voip.ms': ('208.100.60.36', 'Los Angeles 2, CA'),
    'losangeles3.voip.ms': ('208.100.60.37', 'Los Angeles 3, CA'),
    'losangeles4.voip.ms': ('208.100.60.38', 'Los Angeles 4, CA'),

    # New York Servers
    'newyork1.voip.ms': ('208.100.60.66', 'New York 1, NY'),
    'newyork2.voip.ms': ('208.100.60.67', 'New York 2, NY'),
    'newyork3.voip.ms': ('208.100.60.68', 'New York 3, NY'),
    'newyork4.voip.ms': ('208.100.60.69', 'New York 4, NY'),
    'newyork5.voip.ms': ('208.100.60.11', 'New York 5, NY'),
    'newyork6.voip.ms': ('208.100.60.12', 'New York 6, NY'),
    'newyork7.voip.ms': ('208.100.60.13', 'New York 7, NY'),
    'newyork8.voip.ms': ('208.100.60.14', 'New York 8, NY'),

    # San Jose Servers
    'sanjose1.voip.ms': ('208.100.60.40', 'San Jose 1, CA'),
    'sanjose2.voip.ms': ('208.100.60.41', 'San Jose 2, CA'),

    # Seattle Servers
    'seattle1.voip.ms': ('208.100.60.42', 'Seattle 1, WA'),
    'seattle2.voip.ms': ('208.100.60.43', 'Seattle 2, WA'),
    'seattle3.voip.ms': ('208.100.60.44', 'Seattle 3, WA'),
    'seattle-test.voip.ms': ('208.100.60.85', 'Seattle Test, WA (bt)'),

    # Tampa Servers
    'tampa1.voip.ms': ('208.100.60.46', 'Tampa 1, FL'),
    'tampa2.voip.ms': ('208.100.60.47', 'Tampa 2, FL'),
    'tampa3.voip.ms': ('208.100.60.48', 'Tampa 3, FL'),
    'tampa4.voip.ms': ('208.100.60.49', 'Tampa 4, FL'),

    # Washington DC Servers
    'washington1.voip.ms': ('208.100.60.63', 'Washington, DC'),
    'washington2.voip.ms': ('208.100.60.64', 'Washington 2, DC'),

    # International Servers
    'intl.voip.ms': ('208.100.60.99', 'International 01'),
    'amsterdam1.voip.ms': ('208.100.60.65', 'Amsterdam 1, NL'),
    'london1.voip.ms': ('208.100.60.34', 'London 1, UK'),
    'paris1.voip.ms': ('208.100.60.39', 'Paris 1, FR'),
    'sydney1.voip.ms': ('208.100.60.45', 'Sydney 1, AU'),

    # Canada Servers
    'ca.voip.ms': ('208.100.60.166', 'Canada Help (BETA)'),

    # Montreal
    'montreal1.voip.ms': ('208.100.60.19', 'Montreal 01, QC'),
    'montreal2.voip.ms': ('208.100.60.20', 'Montreal 02, QC'),
    'montreal3.voip.ms': ('208.100.60.21', 'Montreal 03, QC'),
    'montreal4.voip.ms': ('208.100.60.22', 'Montreal 04, QC'),
    'montreal5.voip.ms': ('208.100.60.23', 'Montreal 05, QC'),
    'montreal6.voip.ms': ('208.100.60.24', 'Montreal 06, QC'),
    'montreal7.voip.ms': ('208.100.60.25', 'Montreal 07, QC'),
    'montreal8.voip.ms': ('208.100.60.26', 'Montreal 08, QC'),
    'montreal9.voip.ms': ('208.100.60.27', 'Montreal 09, QC'),
    'montreal10.voip.ms': ('208.100.60.28', 'Montreal 10, QC'),

    # Toronto
    'toronto1.voip.ms': ('208.100.60.50', 'Toronto 01, ON'),
    'toronto2.voip.ms': ('208.100.60.51', 'Toronto 02, ON'),
    'toronto3.voip.ms': ('208.100.60.52', 'Toronto 03, ON'),
    'toronto4.voip.ms': ('208.100.60.53', 'Toronto 04, ON'),
    'toronto5.voip.ms': ('208.100.60.54', 'Toronto 05, ON'),
    'toronto6.voip.ms': ('208.100.60.55', 'Toronto 06, ON'),
    'toronto7.voip.ms': ('208.100.60.56', 'Toronto 07, ON'),
    'toronto8.voip.ms': ('208.100.60.57', 'Toronto 08, ON'),
    'toronto9.voip.ms': ('208.100.60.58', 'Toronto 09, ON'),
    'toronto10.voip.ms': ('208.100.60.59', 'Toronto 10, ON'),

    # Vancouver
    'vancouver1.voip.ms': ('208.100.60.60', 'Vancouver 1, BC'),
    'vancouver2.voip.ms': ('208.100.60.61', 'Vancouver 2, BC'),
    'vancouver3.voip.ms': ('208.100.60.62', 'Vancouver 3, BC')
}


def test_server_connection(server_info):
    """
    Test TCP connection time to a server's SIP port (5060)
    """
    domain, (ip, location) = server_info
    port = 5060  # Standard SIP port
    timeout = 5  # seconds
    attempts = 3
    latencies = []

    for _ in range(attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            # Measure connection time
            start_time = time.time()
            result = sock.connect_ex((ip, port))
            end_time = time.time()

            sock.close()

            if result == 0:  # Connection successful
                latency = (end_time - start_time) * 1000  # Convert to milliseconds
                latencies.append(latency)

        except socket.error:
            continue

    # Calculate average latency
    avg_latency = statistics.mean(latencies) if latencies else float('inf')

    return {
        'domain': domain,
        'ip': ip,
        'location': location,
        'latency': avg_latency,
        'status': 'success' if latencies else 'failed'
    }


def print_results(results):
    """
    Print connection test results in a formatted, color-coded table
    """
    # Sort results by latency
    sorted_results = sorted(results, key=lambda x: x['latency'])

    # Find latency thresholds for color coding
    valid_latencies = [r['latency'] for r in results if r['latency'] != float('inf')]
    if valid_latencies:
        median_latency = statistics.median(valid_latencies)
        good_threshold = median_latency * 0.95  # 5% below median (good)
        poor_threshold = median_latency * 1.1  # 10% above median (poor)
    else:
        good_threshold = 50
        poor_threshold = 100

    # Print a timestamp and header
    print(f"\nConnection Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 88)
    print(f"{'Location':<25} {'Domain':<25} {'IP':<15} {'Latency':>10} {'Status':>8}")
    print("=" * 88)

    # Print results
    for result in sorted_results:
        latency = result['latency']

        # Choose color based on latency
        if latency == float('inf'):
            color = Fore.RED
            latency_str = "---"
            status = "CLOSED"
        elif latency < good_threshold:
            color = Fore.GREEN
            latency_str = f"{latency:.1f}ms"
            status = "FAST"
        elif latency < poor_threshold:
            color = Fore.YELLOW
            latency_str = f"{latency:.1f}ms"
            status = "OPEN"
        else:
            color = Fore.RED
            latency_str = f"{latency:.1f}ms"
            status = "SLOW"

        print(
            f"{color}{result['location']:<25} {result['domain']:<25} {result['ip']:<15} {latency_str:>10} {status:>8}{Style.RESET_ALL}")

    print("=" * 85)


def main():
    print("\nStarting voip.ms server connection tests...\n")

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(test_server_connection, voip_servers.items()))

    print_results(results)
    # input("\nPress Enter to exit...") # Used when compiling to exe


if __name__ == "__main__":
    main()

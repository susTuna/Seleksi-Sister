import subprocess, sys, requests

def conn(url):
    print(f"Connecting to {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Connection successful")
            print("Response:", response.text)
        else:
            print(f"Failed to connect, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while connecting: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def set_static(ip):
    try:
        dhcp_commands = [f'nmcli con mod "Wired connection 1" ipv4.address {ip}/24',
                         'nmcli con mod "Wired connection 1" ipv4.gateway 11.70.13.0',
                            'nmcli con mod "Wired connection 1" ipv4.dns 11.70.13.11',
                         'nmcli con mod "Wired connection 1" ipv4.method manual']
        for command in dhcp_commands : subprocess.run(command, shell=True, check=True)
        print(f"Static IP set to {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set static IP: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def set_dhcp():
    try:
        dhcp_command = 'nmcli con mod "Wired connection 1" ipv4.method auto ipv4.address "" ipv4.gateway "" ipv4.dns 11.70.13.11'
        subprocess.run(dhcp_command, shell=True, check=True)
        print("DHCP enabled")
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable DHCP: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def restart_network():
    try:
        restart_command = 'nmcli con down "Wired connection 1" && nmcli con up "Wired connection 1"'
        subprocess.run(restart_command, shell=True, check=True)
        print("Network restarted")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart network: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def curl():
    try:
        curl_command = 'curl -s http://mio.deusexmachina.tech'
        result = subprocess.run(curl_command, shell=True, check=True, capture_output=True, text=True)
        print("Curl output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute curl: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    choice = int(input("Choose an option:\n1. Set Static IP\n2. Enable DHCP\nEnter your choice (1/2): "))
    if choice == 1:
        ip = input("Enter the static IP address (Range 11.70.13.1 to 254): ")
        set_static(ip)
    else:
        set_dhcp()
    restart_network()
    conn("http://mio.deusexmachina.tech")
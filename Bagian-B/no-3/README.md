# DNS
## Requirements
**1. VirtualBox**
**2. Minimal Arch Install with NetworkManager**

## Configuration
**0. Prereq**
- Set VMs into internal network with DHCP server
```bash
VBoxManage dhcpserver add --netname mio --ip 11.70.13.0 --netmask 255.255.255.0 --lowerip 11.70.13.100 --upperip 11.70.13.254 --enable
```
- Install the following on respective VMs
```bash
sudo pacman -S bind #VM 1
sudo pacman -S apache #VM 2
sudo pacman -S git python python-pip #VM 3, 4
sudo pacman -S ufw #VM 4
```
- Static IP Setup
```bash
nmcli con mod "Wired connection 1" ipv4.address 11.70.13.11/24 ipv4.gateway 11.70.13.0 ipv4.method manual #VM 1
nmcli con mod "Wired connection 1" ipv4.address 11.70.13.69/24 ipv4.gateway 11.70.13.0 ipv4.method manual #VM 2
nmcli con mod "Wired connection 1" ipv4.address 11.70.13.100/24 ipv4.gateway 11.70.13.0 ipv4.method manual #VM 4
nmcli net off && nmcli net on #VM 1, 2, 4
```
- Do this for VM 2 and VM 3
Clone this repository
```bash
git clone https://github.com/susTuna/Seleksi-Sister.git
```
Navigate to no-3, create venv, and install requirements
```bash
cd Seleksi-Sister/Bagian-B/no-3
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**1. Backend Server Setup**
- Change listen port
```bash
vim /etc/httpd/conf/httpd.conf
```
Find this line `Listen 80` and change it to `Listen 8080`
- Enable httpd service
```bash
sudo systemctl enable --now  httpd
```
**2. Reverse Proxy Setup**
- Create the .env file
```bash
touch .env
vim .env
```
and fill it with `BACKEND_SERVER_URL = "http://11.70.13.69:8080"`
- Set the firewall
```bash
sudo systemctl enable --now ufw
sudo ufw deny from 11.70.13.0/28 to any #block incoming from 11.70.13.1 - 11.70.13.15
sudo ufw allow 8080 #allow traffic for port 8080
sudo ufw allow http #allow traffic for 8080
sudo ufw deny from any to any #block traffic for anything other than 8080 and http
```
- Run the reverse proxy
```bash
su #change to root if running in user space
uvicorn reverseproxy:app --host 11.70.13.100 --port 80 --reload
```
**3. DNS Server Setup**
- Enable DNS Service
```bash
sudo systemctl enable --now  httpd
```
- Add these lines to the config file
```bash
sudo vim /etc/named.conf
```
```
acl "trusted" {
    127:0:0:1;
    ::1;
    11.70.13.0/24;
};

options {
    ...
    listen-on { 11.70.13.11; };
    allow-query { any; };
    allow-recursion { trusted; };
    allow-query-cache { trusted; };
    ...
};

...

zone "deusexmachina.tech" IN {
    type primary;
    file "deusexmachina.tech.zone";
    allow-update { none; };
};
...
```
- Create Zonefile
```bash
touch /var/named/deusexmachina.tech.zone
sudo vim /var/named/deusexmachina.tech.zone
```
```
$ORIGIN deusexmachina.tech.
$TTL 2h
@ IN SOA ns1 hostmaster(
                2018111111 ; Serial
                8h         ; Refresh
                30m        ; Retry
                1w         ; Expire
                1h )       ; Negative Cache TTL
  IN NS ns1
ns1 IN A 11.70.13.11
mio IN A 11.70.13.100
```
- Restart the service
```bash
sudo systemctl restart named
```

## Running the program
**1. Run main.py**
```bash
python main.py
```


### Raspberry Pi4 monitoring utility

Since `systemd` is the "proper" way to manage Linux services,  
this is a playground(work in progress), to monitor my home rpi4 with systemd and python.

### TODOs, 


1. installation script ->  
    use proper path/venv for execution via systemD

2. test test test
3. file log DEFAULT path -> /var/log/\<name\>
4. secure systemd - systemd-analyze util, cgroups, dedicated user? protectHome, etc.

5. finish README.md

6. maybe add smart readings -> useful for the temperature - 
#   smartctl -A /dev/sda | awk '/0x0022/ {print $10}' 


### Raspberry Pi4 monitoring utility

Since `systemd` is the "proper" way to manage Linux services,  
this is a playground(work in progress), to monitor my home rpi4 with systemd and python.

### TODOs, 


1. installation script ->  
    use proper path/venv for execution via systemD

2. test test test
3. logs rotation ->  
    default behaviour: keep logs for 7 days + file size limit
    file log DEFAULT path -> /var/log/\<name\>
4. secure systemd - systemd-analyze util, cgroups, dedicated user? protectHome, etc.

5. finish README.md
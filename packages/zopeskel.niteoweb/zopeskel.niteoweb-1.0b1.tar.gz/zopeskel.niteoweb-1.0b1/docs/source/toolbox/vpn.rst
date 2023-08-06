***********************
Virtual Private Network
***********************

`Virtual Private Networks`_ or VPNs are just so great. You can lock all your servers down to listen for SSH requests only from your office's IP. And with VPN you can remotely connect to your office LAN and work as if you were physically there. Besides that, all traffic from you to your office is encrypted so you can safely work even when on public WiFi networks. 

This chapter will guide you step-by-step on how to install OpenVPN server on an affordable `Linksys WRT54G`_ wireless router and how to setup Linux and OS X clients for accessing your brand new VPN.

You can probably use any router capable of running `DD-WRT`_ firmware but this guide assumes you have a Linksys WRT54G router.

Certificates
============

First off, you need to create certificates for authorization and encryption of VPN tunnels.

Let's not install extra libraries on our local machines just so we can generate some keys. Instead, let's leverage Rackspace Cloud servers. Creating a temporary 256MB Ubuntu instance is just 2 minutes away and costs only $0.015 per hour.

.. note::

    After you are done creating certificate remember to shut down this temporary Ubuntu server to not spend resources.

Tutorial
--------

Once you have a temporary Ubuntu instance up, follow instruction below. For more information on executed commands, read this `tutorial on dd-wrt.com`_.

Variables
---------
The tutorial suggests setting *vars*. Do that by editing file ``vars`` and making the bottom lines look like this::

    local-macbook:~ bob$ ssh root@174.143.210.69
    root@vpn:~# cd /usr/share/doc/openvpn/examples/easy-rsa/2.0/
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# cp vars vars-org
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# nano vars

    export KEY_COUNTRY="SI"
    export KEY_PROVINCE="Slovenia"
    export KEY_CITY="Ljubljana"
    export KEY_ORG="Plone Boutique"
    export KEY_EMAIL="info@ploneboutique.com"

Generating certificates
-----------------------

Now start creating certificates::

    local-macbook:~ bob$ ssh root@174.143.210.69
    root@vpn:~# apt-get install openvpn openssl
    root@vpn:~# cd /usr/share/doc/openvpn/examples/easy-rsa/2.0/
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# source ./vars
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./clean-all
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./build-ca
    Country Name (2 letter code) [SI]:
    State or Province Name (full name) [Slovenia]:
    Locality Name (eg, city) [Ljubljana]:
    Organization Name (eg, company) [Plone Boutique]:
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) [Plone Boutique CA]:
    Name []:
    Email Address [info@ploneboutique.com]:
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./build-key-server server
    Country Name (2 letter code) [SI]:
    State or Province Name (full name) [Slovenia]:
    Locality Name (eg, city) [Ljubljana]:
    Organization Name (eg, company) [Plone Boutique]:
    Organizational Unit Name (eg, section) []: 
    Common Name (eg, your name or your server's hostname) [server]:
    Name []:
    Email Address [info@ploneboutique.com]:
    A challenge password []:
    An optional company name []:
    Sign the certificate? [y/n]: y
    1 out of 1 certificate requests certified, commit? [y/n] y
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./build-key bob
    Country Name (2 letter code) [SI]:
    State or Province Name (full name) [Slovenia]:
    Locality Name (eg, city) [Ljubljana]:
    Organization Name (eg, company) [Plone Boutique]:
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) [bob]:
    Name []:
    Email Address [info@ploneboutique.com]:bob@ploneboutique.com
    A challenge password []:
    An optional company name []:
    Sign the certificate? [y/n]:y
    1 out of 1 certificate requests certified, commit? [y/n]y
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./build-dh
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ls keys
    01.pem  ca.key      index.txt.attr      serial      server.csr  bob.csr
    02.pem  dh1024.pem  index.txt.attr.old  serial.old  server.key  bob.key
    ca.crt  index.txt   index.txt.old       server.crt  bob.crt

Archiving certificates
----------------------

You need to store generated certificates so you can give them to colleagues that will use VPN to remotely connect to your office LAN. 

In order to be able to create new certificates later on you also need to store other files in folder ``keys``. So the best approach here is to compress and encrypt the whole ``vars`` folder and save it to your OnlineDisk. Save the encryption password to KeePass.

First, copy ``vars`` file to keys folder, so we also archive this file::

    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# cp vars keys/

Now you are ready to compress/encrypt ``keys`` folder and download it to your local machine to archive it to your OnlineDisk::
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# tar cz keys | openssl enc -aes-256-cbc -e > keys.tar.gz.enc
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# apt-get install rsync
    local-macbook:~ bob$ rsync -avzhP root@174.143.210.69:/usr/share/doc/openvpn/examples/easy-rsa/2.0/keys.tar.gz.enc /Users/bob/OnlineDisk/vpn_keys.tar.gz.enc

Creating additional certificates
--------------------------------

Inevitably you'll be faced with creating additional certificates. Either you get a new team member or someone will loose their certificate. Since we have the everything we need archived on OnlineDisk, this is fairly easy. 

Create a new Ubuntu cloud server instance and install ``openssl`` and ``rsync``::
    
    local-macbook:~ bob$ ssh root@174.143.210.69
    root@vpn:~# apt-get install openvpn openssl rsync

Upload keys to temporary server::

    local-macbook:~ bob$ rsync -avzhP /Users/bob/OnlineDisk/vpn_keys.tar.gz.enc   root@174.143.210.69:/usr/share/doc/openvpn/examples/easy-rsa/2.0/keys.tar.gz.enc

Decrypt and decompress keys on the server::

    local-macbook:~ bob$ ssh root@174.143.210.69
    root@vpn:~# cd /usr/share/doc/openvpn/examples/easy-rsa/2.0/
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# openssl enc -d -aes-256-cbc -in keys.tar.gz.enc -out keys.tar.gz
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# tar xf keys.tar.gz
    
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ls keys
    01.pem  ca.key      index.txt.attr      serial      server.csr  bob.crt
    02.pem  dh1024.pem  index.txt.attr.old  serial.old  server.key  bob.csr
    ca.crt  index.txt   index.txt.old       server.crt  vars        bob.key

Move file ``vars`` back to where it's expected to be find::

    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# cp vars vars_orig
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# cp keys/vars vars

Create a new certificate::

    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# source ./vars
    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ./build-key jane

    Country Name (2 letter code) [SI]:
    State or Province Name (full name) [Slovenia]:
    Locality Name (eg, city) [Ljubljana]:
    Organization Name (eg, company) [Plone Boutique]:
    Organizational Unit Name (eg, section) []:
    Common Name (eg, your name or your server's hostname) [jane]:
    Name []:
    Email Address [jane@ploneboutique.com]:
    A challenge password []:
    An optional company name []:
    Sign the certificate? [y/n]:y
    1 out of 1 certificate requests certified, commit? [y/n]y

    root@vpn:/usr/share/doc/openvpn/examples/easy-rsa/2.0# ls keys
    01.pem  ca.crt       jane.csr  index.txt           index.txt.old  server.crt  vars      bob.key
    02.pem  ca.key       jane.key  index.txt.attr      serial         server.csr  bob.crt
    03.pem  jane.crt  dh1024.pem   index.txt.attr.old  serial.old     server.key  bob.csr

Archive the newly created certificate by repeating the procedure from the previous chapter (archiving the whole ./keys folder to OnlineDisk).

OpenVPN Server
==============

Now that we have certificates prepared we can start setting up an OpenVPN server on the WRT54G router.

Installing
----------

Go to the DD-WRT download page and grab the package that also has OpenVPN support (dd-wrt.v24_vpn_generic.bin). Follow official DD-WRT instructions on how to flash of the router's firmware and continue below.

Configuring
-----------

- Enable OpenVPN server in Services tab and set it's Start type to WAN Up.
- Paste in certificates created in advance on a temporary Ubuntu cloud instance.
    - To field ``Public Server Cert for OpenVPN`` insert contents of file ``ca.crt``
    - To field ``Public Client Cert for OpenVPN`` insert contents of file ``server.crt``
    - To field ``Private Client Cert for OpenVPN`` insert contents of file ``server.key``
    - To field ``DH PEM for OpenVPN`` insert contents of file ``dh1024.pem``
    
- Paste in OpenVPN server config::

    push "route 192.168.1.0 255.255.255.0"
    server 192.168.2.0 255.255.255.0

    dev tun0
    proto udp
    keepalive 10 120
    dh /tmp/openvpn/dh.pem
    ca /tmp/openvpn/ca.crt
    cert /tmp/openvpn/cert.pem
    key /tmp/openvpn/key.pem

    # management parameter allows DD-WRT's OpenVPN Status web page to access the server's management port
    # port must be 5001 for scripts embedded in firmware to work
    management localhost 5001

- Configure *iptables* firewall by going to Administration -> Commands, pasting in iptables config and clicking save firewall::

    # enable tunnel
    iptables -I INPUT 1 -p udp --dport 1194 -j ACCEPT
    iptables -I FORWARD 1 --source 192.168.2.0/24 -j ACCEPT
    iptables -I FORWARD -i br0 -o tun0 -j ACCEPT
    iptables -I FORWARD -i tun0 -o br0 -j ACCEPT

    # NAT the VPN client traffic to the internet
    iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -o eth0 -j MASQUERADE

- Restart router.

OpenVPN Clients
===============

Ok, we have certificates and we also have a running OpenVPN. Time to install OpenVPN client on your local machine and connect!

OS X
----

For OS X users the recommended application for using OpenVPN is Tunnelblick.

#. Go to `Tunnelblick's website`_, download Tunnelblick 3.0 application and install it.

#. Run Tunnelblick. Click ``install and edit sample configuration file`` and paste into it this client configuration (replace ``bob`` with your nickname and add your office IP and your ISP's DNS)::

    # Specify that we are a client and that we will be pulling certain config file directives from the server.
    client

    # Use the same setting as you are using on the server.
    # On most systems, the VPN will not function unless you partially or fully disable the firewall for the TUN/TAP interface.
    dev tun0

    # Are we connecting to a TCP or # UDP server?  Use the same setting as on the server.
    proto udp

    # The hostname/IP and port of the server.
    remote <your office IP> 1194

    # Keep trying indefinitely to resolve the host name of the OpenVPN server.  
    # Very useful on machines which are not permanently connected to the internet such as laptops.
    resolv-retry infinite

    # Most clients don't need to bind to a specific local port number.
    nobind

    # Downgrade privileges after initialization (non-Windows only)
    # NOTE: this cause problems with reverting to default route once VPN is disconnected
    # user bob
    # group bob

    # Try to preserve some state across restarts.
    persist-key
    persist-tun

    # Wireless networks often produce a lot of duplicate packets.  Set this flag to silence duplicate packet warnings.
    mute-replay-warnings

    # SSL/TLS parms.
    ca ca.crt
    cert bob.crt
    key bob.key

    # Enable compression on the VPN link. Don't enable this unless it is also enabled in the server config file.
    ;comp-lzo

    # Set log file verbosity.
    verb 3

    # from wiki
    remote-cert-tls server
    float

    # route all traffic through VPN
    # if you don't know what to enter, you can use 8.8.8.8 and 8.8.4.4, Google's Public DNSes
    redirect-gateway def1
    dhcp-option DNS <your ISP's primary DNS IP>
    dhcp-option DNS <your ISP's secondary DNS IP>

#. Use Terminal to add certificate keys to your Tunnelblick configuration (keys created on Ubuntu cloud instance), again replacing ``bob`` in filename::

    nano ~/Library/Application\ Support/Tunnelblick/Configurations/ca.crt
    nano ~/Library/Application\ Support/Tunnelblick/Configurations/bob.crt
    nano ~/Library/Application\ Support/Tunnelblick/Configurations/bob.key
    
Now you are ready to use your VPN. Click on Tunnelblick icon next to *current time* in the top-right corner of your screen and select ``connect openvpn``. All your traffic should now be routed through a secure tunnel to your office.

Confirm this by visiting `whatismyip.com`_. The IP displayed should be your office's IP, meaning you are accessing internet through a tunnel from your office. Hooray!

Ubuntu
------

For Ubuntu users it's best to just use command-line commands from OpenVPN package.

#. Install with ``sudo apt-get install openvpn``

#. Add certificates keys created on temporary Ubuntu cloud instance ``~/.ssh/``. You need to copy ``ca.crt``, ``bob.crt`` and ``bob.key`` (replace ``bob`` with your nickname).

#. Configure OpenVPN by copying this configuration to ``/etc/openvpn/client.conf``. Change paths to certificate keys so that they match your real paths::

    # Specify that we are a client and that we will be pulling certain config file directives from the server.
    client

    # Use the same setting as you are using on the server.
    # On most systems, the VPN will not function unless you partially or fully disable the firewall for the TUN/TAP interface.
    dev tun0

    # Are we connecting to a TCP or # UDP server?  Use the same setting as on the server.
    proto udp

    # The hostname/IP and port of the server.
    remote <your office IP> 1194

    # Keep trying indefinitely to resolve the host name of the OpenVPN server.  
    # Very useful on machines which are not permanently connected to the internet such as laptops.
    resolv-retry infinite

    # Most clients don't need to bind to a specific local port number.
    nobind

    # Downgrade privileges after initialization (non-Windows only)
    # NOTE: this cause problems with reverting to default route once VPN is disconnected
    # user bob
    # group bob

    # Try to preserve some state across restarts.
    persist-key
    persist-tun

    # Wireless networks often produce a lot of duplicate packets.  Set this flag to silence duplicate packet warnings.
    mute-replay-warnings

    # SSL/TLS parms.
    ca ca.crt
    cert bob.crt
    key bob.key

    # Enable compression on the VPN link. Don't enable this unless it is also enabled in the server config file.
    ;comp-lzo

    # Set log file verbosity.
    verb 3

    # from wiki
    remote-cert-tls server
    float

    # route all traffic through VPN
    # if you don't know what to enter, you can use 8.8.8.8 and 8.8.4.4, Google's Public DNSes
    redirect-gateway def1
    dhcp-option DNS <your ISP's primary DNS IP>
    dhcp-option DNS <your ISP's secondary DNS IP>

#. Start by running ``sudo openvpn --config /etc/openvpn/client.conf``.

Confirm that you are using VPN by visiting `whatismyip.com`_. The IP displayed should be your office's IP, meaning you are accessing internet through a tunnel from your office. Hooray!



.. URLs for links in content.

.. _Linksys WRT54G: http://en.wikipedia.org/wiki/Linksys_WRT54G_series
.. _DD-WRT: http://www.dd-wrt.com/
.. _Virtual Private Networks: http://en.wikipedia.org/wiki/Virtual_private_network
.. _whatismyip.com: http://whatismyip.com
.. _Tunnelblick's website: http://code.google.com/p/tunnelblick/
.. _tutorial on dd-wrt.com: http://www.dd-wrt.com/wiki/index.php/VPN_(the_easy_way)_v24%2B#Creating_Certificates_using_Ubuntu_Linux.

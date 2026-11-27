# 24. Configuring and Enabling Core Server Services

One of Slackware's greatest strengths as a server operating system is its simplicity and predictability. Unlike modern Linux distributions that rely on complex initialization daemons and unit configuration targets, Slackware adheres strictly to a traditional BSD-style init system.

In Slackware, server services and network daemons are managed via standalone shell scripts stored in `/etc/rc.d/`. All server software provided by default—such as web servers, database engines, mail transfer agents, and file shares—is installed out-of-the-box in a disabled state for safety.



## 24.1 The Slackware Service Management Philosophy

To enable or disable a server service in Slackware, you simply change the execute permissions of its corresponding init script in `/etc/rc.d/`.

1. Enabling a Service for Automatic Boot Startup
To configure a service to start automatically whenever the system boots, grant execution permissions (`+x`) to its script:

```bash
darkstar:~# chmod +x /etc/rc.d/rc.<service>
```

2. Disabling a Service
To prevent a service from launching at boot time, remove execution permissions (`-x`):

```bash
darkstar:~# chmod -x /etc/rc.d/rc.<service>
```

3. Controlling Running Services Manually
Regardless of whether a service is enabled at boot, you can manually start, stop, restart, or check its status as `root`:

```bash
darkstar:~# /etc/rc.d/rc.<service> start
darkstar:~# /etc/rc.d/rc.<service> stop
darkstar:~# /etc/rc.d/rc.<service> restart
darkstar:~# /etc/rc.d/rc.<service> status
```

## 24.2 Core Server Services Available in Slackware

Below is a categorized breakdown of the primary server-grade daemons included in the default Slackware software repositories (from the `n/`, `ap/`, and `a/` package sets).

> **Note:** The goal of this section is not to provide an in-depth technical explanation of how each underlying protocol or service functions, but rather to show you how to enable, configure, and manage these daemons within a Slackware environment.



### 24.2.1. Web and Database Stack (LAMP)

**Apache HTTP Server (`httpd`)**

* **Package:** `httpd` (Apache HTTP Server)
* **Init Script:** `/etc/rc.d/rc.httpd`
* **Configuration:** `/etc/httpd/httpd.conf`
* **Description:** The industry-standard Apache web server. Out-of-the-box, it includes support for SSL/TLS, Virtual Hosts, and module integration (such as PHP).
* **Official Web site:** [https://httpd.apache.org/](https://httpd.apache.org/)


**Enabling and starting Apache:**
```bash
darkstar:~# chmod +x /etc/rc.d/rc.httpd
darkstar:~# /etc/rc.d/rc.httpd start
```

**MariaDB Database Server (`mariadb`)**

* **Package:** `mariadb` (Drop-in replacement for MySQL Database Server)
* **Init Script:** `/etc/rc.d/rc.mysqld`
* **Configuration:** `/etc/my.cnf` and `/etc/my.cnf.d/`
* **Description:** Enterprise open-source relational database server.
* **Official Web site:** [https://mariadb.org/](https://mariadb.org/)


**Initial Setup & Activation:**
Before launching MariaDB for the first time, initialize the system database files:
```bash
darkstar:~# mariadb-install-db --user=mysql
darkstar:~# chmod +x /etc/rc.d/rc.mysqld
darkstar:~# /etc/rc.d/rc.mysqld start
darkstar:~# mariadb-secure-installation
```

**PHP Scripting Language Engine (`php`)**
* **Package:** `php` is a general-purpose scripting language geared toward web development.
* **Configuration:** `/etc/httpd/mod_php.conf` and `/etc/php.ini`
* **Description:** Enables PHP execution within the Apache web server.
* **Activation:** Uncomment the PHP module loader line inside `/etc/httpd/httpd.conf`:

  ```apache
  Include /etc/httpd/mod_php.conf
  ```
  
* **Official Web site:** [https://www.php.net/](https://www.php.net/)


  
### 24.2.2. Secure Remote Access and Management

**OpenSSH Daemon (`openssh`)**
* **Package:** `openssh` is the premier connectivity tool for remote login with the SSH protocol.
* **Init Script:** `/etc/rc.d/rc.sshd`
* **Configuration:** `/etc/ssh/sshd_config`
* **Description:** Encrypted remote shell access and secure file transfer (SFTP/SCP).
* **Official Web site:** [https://www.openssh.org/](https://www.openssh.org/)

**Enabling OpenSSH:**
```bash
darkstar:~# chmod +x /etc/rc.d/rc.sshd
darkstar:~# /etc/rc.d/rc.sshd start
```

### 24.2.3. File Sharing and Network Storage

**Samba File and Print Server (`samba`)**
* **Package:** `samba` is the most feature-rich Open Source implementation of the SMB and Active Directory protocols for Linux and UNIX-like systems.
* **Init Script:** `/etc/rc.d/rc.samba`
* **Configuration:** `/etc/samba/smb.conf`
* **Description:** Provides SMB/CIFS file and print sharing for Windows, macOS, and Linux clients, as well as Active Directory integration.
* **Official Web site:** [https://www.samba.org/](https://www.samba.org/)

**Enabling Samba:**
```bash
darkstar:~# cp /etc/samba/smb.conf-sample /etc/samba/smb.conf
darkstar:~# chmod +x /etc/rc.d/rc.samba
darkstar:~# /etc/rc.d/rc.samba start
```


### 24.2.4 Network File System (`nfs-utils`)

* **Package:** `nfs-utils` is a protocol allowing remote access to a filesystem through the network
* **Init Script:** `/etc/rc.d/rc.nfsd`
* **Configuration:** `/etc/exports`
* **Description:** High-performance native UNIX/Linux network file sharing.
* **Official Web site:** [https://linux-nfs.org/](https://linux-nfs.org/)

**Enabling NFS Server:**
```bash
darkstar:~# chmod +x /etc/rc.d/rc.nfsd
darkstar:~# /etc/rc.d/rc.nfsd start
```

### 24.2.5 FTP Daemons (`vsftpd` / `proftpd`)
* **Packages:** `vsftpd` (Very Secure FTP Daemon) / `proftpd` (ftp server written for use on Unix and Unix-a-like operating systems)
* **Init Scripts:** `/etc/rc.d/rc.inetd` / `/etc/rc.d/rc.inetd`
* **Description:** Secure, high-speed FTP server implementations.
* **Official Web site:** [https://security.appspot.com/vsftpd.html](https://security.appspot.com/vsftpd.html) and [http://www.proftpd.org/](http://www.proftpd.org/)


**To enable vsftpd**

```bash
darkstar:~# vi /etc/inetd.conf
```

Uncomment the line, removing the symbol `#`

```text
ftp     stream  tcp     nowait  root    /usr/sbin/tcpd  vsftpd
```

**To enable proftpd**

```bash
darkstar:~# vi /etc/inetd.conf
```

Uncomment the line, removing the symbol `#`

```text
ftp     stream  tcp     nowait  root    /usr/sbin/tcpd  proftpd
```

And restart the service inetd

```bash
darkstar:~# chmod +x /etc/rc.d/rc.inetd
darkstar:~# /etc/rc.d/rc.inetd restart
```

### 24.2.6 Domain Name System (DNS) and DHCP

**BIND DNS Server (`bind`)**
* **Package:** `bind` is a DNS server
* **Init Script:** `/etc/rc.d/rc.bind`
* **Configuration:** `/etc/named.conf`
* **Description:** The Internet standard Domain Name System (`named`) daemon for authoritative and caching name servers.
* **Official Web site:** [https://www.isc.org/bind/](https://www.isc.org/bind/)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.bind
darkstar:~# /etc/rc.d/rc.bind start
```

**Dnsmasq DNS/DHCP Server (`dnsmasq`)**
* **Package:** `dnsmasq` provides network infrastructure for networks
* **Init Script:** `/etc/rc.d/rc.dnsmasq`
* **Configuration:** `/etc/dnsmasq.conf`
* **Description:** A lightweight DNS forwarder, DHCP server, and router advertisement daemon ideal for small business networks or home routers.
* **Official Web site:** [https://thekelleys.org.uk/dnsmasq/doc.html](https://thekelleys.org.uk/dnsmasq/doc.html)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.dnsmasq
darkstar:~# /etc/rc.d/rc.dnsmasq start
```

### 24.2.7. Mail Services (MTA / IMAP / POP3)

**Postfix Mail Transfer Agent (`postfix`)**
* **Package:** `postfix`  is mail server and as an alternative to the widely-used Sendmail program.
* **Init Script:** `/etc/rc.d/rc.postfix`
* **Configuration:** `/etc/postfix/main.cf`
* **Description:** High-performance, secure SMTP mail transfer agent. Slackware also includes classic `sendmail` as an alternative.
* **Official Web site:** [https://www.postfix.org/](https://www.postfix.org/)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.postfix
darkstar:~# /etc/rc.d/rc.postfix start
```

**Dovecot IMAP/POP3 Server (`dovecot`)**
* **Package:** `dovecot` is an open source email server for Linux/UNIX-like systems
* **Init Script:** `/etc/rc.d/rc.dovecot`
* **Configuration:** `/etc/dovecot/dovecot.conf`
* **Description:** Secure, enterprise-grade IMAP and POP3 server for mail client access.
* **Official Web site:** [https://dovecot.org/](https://dovecot.org/)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.dovecot
darkstar:~# /etc/rc.d/rc.dovecot start
```

### 24.2.8. Network Infrastructure and Security

**Network Time Protocol (`ntp`)**
* **Package:** `ntp` is a protocol designed to synchronize the clocks of computers over a network to a common timebase
* **Init Script:** `/etc/rc.d/rc.ntpd`
* **Configuration:** `/etc/ntp.conf`
* **Description:** Keeps system clock precisely synchronized across the network.
* **Official Web site:** [https://www.ntp.org/](https://www.ntp.org/)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.ntpd
darkstar:~# /etc/rc.d/rc.ntpd start
```

### 24.2.9 OpenVPN Server (`openvpn`)
* **Package:** `openvpn`  is a full-featured open source SSL VPN solution
* **Init Script:** `/etc/rc.d/rc.openvpn`
* **Configuration:** `/etc/openvpn/`
* **Description:** SSL/TLS Virtual Private Network server for secure site-to-site or road-warrior access.
* **Official Web site:** [https://community.openvpn.net/](https://community.openvpn.net/)

```bash
darkstar:~# chmod +x /etc/rc.d/rc.openvpn
darkstar:~# /etc/rc.d/rc.openvpn start
```



## 24.3 Server Services Reference Summary

| Service Category | Daemon / Software | Init Script Path | Primary Config File |
| :--- | :--- | :--- | :--- |
| **Web Server** | Apache (`httpd`) | `/etc/rc.d/rc.httpd` | `/etc/httpd/httpd.conf` |
| **Database** | MariaDB (`mariadb`) | `/etc/rc.d/rc.mysqld` | `/etc/my.cnf` |
| **Remote Access** | OpenSSH (`sshd`) | `/etc/rc.d/rc.sshd` | `/etc/ssh/sshd_config` |
| **File Sharing (SMB)** | Samba (`smbd`/`nmbd`) | `/etc/rc.d/rc.samba` | `/etc/samba/smb.conf` |
| **File Sharing (NFS)** | NFS Utilities | `/etc/rc.d/rc.nfsd` | `/etc/exports` |
| **FTP** | vsftpd | `/etc/rc.d/rc.vsftpd` | `/etc/vsftpd.conf` |
| **DNS Server** | BIND (`named`) | `/etc/rc.d/rc.bind` | `/etc/named.conf` |
| **DNS / DHCP** | Dnsmasq | `/etc/rc.d/rc.dnsmasq` | `/etc/dnsmasq.conf` |
| **Mail Transfer** | Postfix | `/etc/rc.d/rc.postfix` | `/etc/postfix/main.cf` |
| **Mail Delivery** | Dovecot | `/etc/rc.d/rc.dovecot` | `/etc/dovecot/dovecot.conf` |
| **Time Sync** | NTP (`ntpd`) | `/etc/rc.d/rc.ntpd` | `/etc/ntp.conf` |
| **VPN** | OpenVPN | `/etc/rc.d/rc.openvpn` | `/etc/openvpn/*.conf` |


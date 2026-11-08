# 11. Working with Filesystems

## 11.1 The Filesystem Hierarchy

Slackware Linux stores all of its files and directories under a single `/` directory, typically referred to as "root". This is in stark contrast to what you may be familiar with in Microsoft Windows. Different hard disk partitions, USB flash drives, memory cards (and even CD-ROMs and/or floppy disks, if you still use them) can all be mounted in directories under `/`, rather than relying on "drive letters" (such as `C:` or `D:`).

While these devices can technically be mounted almost anywhere, Slackware provides sensible default locations:

* **The `/mnt` directory:** Its primary purpose is to provide a location for system administrators to mount block devices temporarily. You can mount volumes directly on `/mnt` (the traditional UNIX approach), use predefined subdirectories such as `/mnt/hd` or `/mnt/tmp`, or create custom mount points as needed.

* **The `/media` directory:** Its purpose is to provide a standardized location across different Linux systems for users and desktop applications to mount removable media. For example, desktop environments (such as KDE) or file managers (like Konqueror) can utilize `/media` for auto-mounting devices. While Slackware traditionally defaults to using `/mnt` (e.g., `/mnt/cdrom` as the CD-ROM mount point in `/etc/fstab`), you can edit `/etc/fstab` if you prefer to strictly follow FHS (Filesystem Hierarchy Standard) recommendations.

Below is a breakdown of the standard directories found on virtually all Slackware Linux installations and their primary functions:

| Directory | Description |
| --- | --- |
| **`/`** | The root directory, under which all others exist |
| **`/bin`** | Minimal set of binary programs for all users |
| **`/boot`** | The kernel, initrd, and other requirements for booting Slackware |
| **`/dev`** | Collection of special files allowing direct access to hardware |
| **`/etc`** | System configuration files |
| **`/home`** | User directories where personal files and settings are stored |
| **`/lib`** | Core shared libraries needed to boot the system and run binaries in `/bin` and `/sbin` |
| **`/lib64`** | Essential 64-bit system libraries (on 64-bit Slackware architectures) |
| **`/lost+found`** | Directory where `fsck` stores recovered file fragments after an unclean shutdown |
| **`/media`** | Directory for auto-mounting features in DBUS/HAL |
| **`/mnt`** | Places to temporarily mount removable media |
| **`/opt`** | Directory where some (typically proprietary) software may be installed |
| **`/proc`** | Kernel exported filesystem for process information |
| **`/root`** | The root user's home directory |
| **`/run`** | Volatile runtime data describing system state since the last boot (`tmpfs`) |
| **`/sbin`** | Minimal set of system or superuser binaries |
| **`/srv`** | Site-specific data such as web pages served by this system |
| **`/sys`** | Special kernel implimentation details |
| **`/tmp`** | Directory reserved for temporary files for all users |
| **`/usr`** | All non-essential programs, libraries, and shared files |
| **`/var`** | Regularly changing data such as log files |

## 11.2 Local Filesystem Types

The Linux kernel supports a wide variety of filesystems, allowing you to choose from a rich set of features tailored to your specific needs. Fortunately, the default filesystem choices in Slackware Linux are well-suited for almost any scenario, from general-purpose desktop computing to high-performance enterprise servers.

The filesystem types listed below are enabled and supported during the Slackware installation process:


### 11.2.1 ext2

ext2 is the oldest filesystem included in Slackware Linux for storing data on hard disks. Compared to other filesystems, ext2 is simplistic. It is faster than most others for reading and writing data, but does **not include any journaling capability**. This means that after a hard crash, the filesystem must be exhaustively checked to discover and (hopefully) fix any errors.

`ext2` is the oldest filesystem in the `ext` family included with Linux for storing data on block devices. Compared to modern filesystems, `ext2` is simplistic. While it offers fast read and write speeds due to its low metadata overhead, it does **not include journaling capabilities**. Consequently, after an unclean shutdown or hard system crash, the entire filesystem must undergo an exhaustive consistency check (`fsck`) to discover and repair errors. Today, `ext2` is primarily used for small boot partitions or solid-state flash media where minimizing write cycles is critical.


### 11.2.2 ext3

`ext3` is the direct successor to `ext2`. It was designed to replace `ext2` by adding **journaling support** while maintaining backwards compatibility with the existing `ext2` codebase. Journaling logs pending filesystem changes to a dedicated area before committing them to main storage, drastically reducing recovery times after a system power failure. In fact, `ext2` and `ext3` share a nearly identical on-disk structure, allowing seamless in-place conversion between the two without data loss. While highly reliable and supported by extensive recovery utilities, `ext3` requires periodic, full `fsck` checks at boot time, which can cause noticeable delays on large volumes.


### 11.2.3 ext4

`ext4` is the default and most widely recommended general-purpose filesystem for Slackware Linux across desktops, laptops, and a lot of enterprise servers. Building upon the foundation of `ext3`, `ext4` introduces substantial performance, capacity, and reliability improvements:

* **Extents:** Replaces traditional block mapping with extents, improving large file performance and reducing disk fragmentation.
* **Delayed Allocation:** Optimizes block allocation decisions right before writing data to disk, enhancing write speed and storage efficiency.
* **Scalability:** Supports volume sizes up to 1 Exabyte (EB) and individual files up to 16 Terabytes (TB).
* **Faster Filesystem Checks:** Unallocated block groups are skipped during `fsck`, making maintenance checks significantly faster than on `ext3`.

For the vast majority of modern Slackware desktop and server installations, `ext4` provides the optimal balance of rock-solid stability and high performance.


### 11.2.4 JFS

`JFS` was contributed to the Linux kernel by IBM and is renowned for its low CPU usage and rapid responsiveness even under heavy server workloads. Designed for high-end enterprise systems, `JFS` handles scaling across massive storage volumes with ease. Its long history of rigorous testing makes it one of the most stable and reliable journaling filesystems available for Linux, particularly for Network-Attached Storage (NAS) appliances.


### 11.2.5 btrfs

`Btrfs` is a modern **Copy-on-Write (CoW)** filesystem designed for advanced storage management and data integrity. Key features of `Btrfs` include:

* **Snapshots & Subvolumes:** Allows creating near-instantaneous, writable or read-only point-in-time system snapshots.
* **Data Integrity:** Computes checksums for both data and metadata, enabling automatic detection and recovery from silent data corruption (*bit rot*).
* **Transparent Compression:** Supports real-time data compression algorithms (such as `zstd`, `lzo`, and `zlib`) to save storage space and increase write throughput.
* **Integrated Volume Management:** Supports multi-device pooling and RAID configurations directly at the filesystem level.

`Btrfs` is ideal for users who require advanced features like system rollbacks and storage pooling without relying on external logical volume managers.


### 11.2.6 f2fs

`F2FS` was developed by Samsung specifically for NAND flash-based storage devices, such as Solid-State Drives (SSDs), NVMe storage, micro-SD cards, and eMMC chips. Unlike traditional filesystems designed around the geometry of spinning hard disk platters, `F2FS` uses a log-structured layout optimized for the internal characteristics of flash memory. This layout minimizes write amplification, extends drive lifespan, and delivers superior read/write performance on flash storage media.


### 11.2.7 xfs

Originally developed by Silicon Graphics (SGI) for enterprise UNIX platforms, `XFS` is a mature 64-bit journaling filesystem engineered for high performance, high concurrency, and massive scalability. `XFS` excels at managing large files and colossal storage arrays, using extent-based allocation and dynamic inode allocation. While `XFS` consumes slightly more system RAM than simpler filesystems, its exceptional parallel I/O throughput makes it the premier choice for database servers, media rendering hosts, and large data repositories.


### 11.2.8 swap

Unlike standard filesystems designed to store files and directories, a `swap` partition (or swap file) serves as **virtual memory** for the Linux kernel. When physical RAM approaches full capacity, the kernel moves inactive memory pages out of RAM and writes them into swap space, preventing Out-Of-Memory (OOM) process crashes. 

Because accessing physical disk storage is exponentially slower than system RAM, heavy swap utilization results in system latency (*disk thrashing*). Swap should be treated as an essential safety net rather than a substitute for physical memory; if your system frequently relies on swap, adding more RAM is recommended.


### 11.2.9 iso9660

`iso9660` is a standard filesystem specifically designed for optical media such as CDs and DVDs, as well as disk image files (`.iso`). Because optical media are read-only by nature, the Linux kernel includes native read support for `iso9660`, but does not support direct in-kernel writing. To master or generate `iso9660` images, user-space tools such as `mkisofs`, `xorriso`, or `growisofs` are used.

In Slackware Linux, `iso9660` plays a crucial role: the official installation media (such as installer DVDs and live ISOs) use this format combined with **Rock Ridge extensions**, which allow POSIX file permissions, symbolic links, and long filenames to be preserved on optical media.




## 11.3 Other suportted filesystems

In addition to the primary filesystems configured during installation, Slackware Linux supports a wide variety of additional filesystems through kernel drivers and user-space tools. Below is a breakdown of these filesystems and their primary use cases:

* **`bcachefs`** — A modern Copy-on-Write (CoW) filesystem engineered for high performance, reliability, and advanced features such as multi-device caching, native encryption, data checksumming, and transparent compression.
* **`bfs`** — The legacy Boot Filesystem used by UnixWare systems. Linux includes read-only support primarily for mounting and retrieving files from old UnixWare boot partitions.
* **`cramfs`** — Compressed ROM Filesystem, a lightweight, read-only filesystem designed for memory-constrained embedded systems and bootable ROM images where storage space is critical.
* **`exfat`** — Extended File Allocation Table, a proprietary filesystem created by Microsoft for high-capacity flash storage (such as SDXC cards and large USB drives). It removes the 4 GB individual file size limit of FAT32 while offering broad cross-platform compatibility.
* **`f2fs`** — Flash-Friendly File System, developed by Samsung specifically for NAND flash memory media (SSDs, NVMe drives, SD cards, eMMC). It utilizes a log-structured architecture optimized to reduce write amplification and extend drive longevity.
* **`fat`** — The core Linux kernel module providing underlying driver support for File Allocation Table filesystems (including FAT12, FAT16, and FAT32).
* **`fuse.bcachefs`** — A user-space implementation of `bcachefs` operating via FUSE (Filesystem in Userspace), allowing systems lacking native in-kernel `bcachefs` driver modules to mount and access `bcachefs` volumes.
* **`fuseblk.bcachefs`** — A block-device variant of FUSE utilized by mount helpers when accessing `bcachefs` volumes on physical block devices via user space.
* **`minix`** — The historic filesystem created for the MINIX operating system. As the very first filesystem supported by the Linux kernel, it is retained today mainly for legacy compatibility and creating small floppy disk images.
* **`msdos`** — The legacy MS-DOS FAT filesystem driver using strict 8.3 filename conventions, lacking support for modern long filenames.
* **`ntfs`** — New Technology File System, the default filesystem for modern Microsoft Windows operating systems. Linux supports reading and writing NTFS partitions natively through kernel modules and user-space utilities such as `ntfs-3g`.
* **`vfat`** — Virtual FAT, an extension to the MS-DOS FAT filesystem introduced with Microsoft Windows 95 to support long filenames (up to 255 characters). Sometimes you may need to share data between Windows and Linux computers when network transfer isn't an option, making `vfat` a reliable choice due to its universal operating system support. However, because it does not store POSIX Linux permissions, special mount options (such as `uid`, `gid`, and `umask`) must be used to allow non-root users proper access.


## 11.4 Creating and Formatting a Filesystem

Now that we have covered the different filesystems available in Slackware Linux, the next logical step is learning how to add, partition, and format a new storage drive.

To demonstrate this process, we will add a new 30 GB virtual hard disk to our test machine.


Before modifying any storage drive, list the existing disks and partition layouts using `fdisk -l`:


```bash
root@darkstar:~# fdisk -l
Disk /dev/vda: 30 GiB, 32212254720 bytes, 62914560 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk /dev/sda: 90 GiB, 96636764160 bytes, 188743680 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: AEAF9752-02D6-494B-8878-6BB396807DF7

Device         Start       End   Sectors  Size Type
/dev/sda1       2048    206847    204800  100M EFI System
/dev/sda2     206848   2303999   2097152    1G Linux filesystem
/dev/sda3    2304000  10692607   8388608    4G Linux swap
/dev/sda4   10692608 188741631 178049024 84.9G Linux filesystem
root@darkstar:~#
```

In this output, `/dev/sda` contains the operating system, while `/dev/vda` is the newly added, unpartitioned 30 GiB drive.

> Warning: Disk partitioning and formatting are inherently destructive operations. Always verify that you are targeting the correct device node (such as `/dev/vda`), as executing partition or format commands on the wrong disk will cause permanent data loss!

Execute `fdisk` pointing directly to the target device:

Inside the interactive `fdisk` interface, execute the following sequence (pressing <kbd>Enter</kbd> after each command):

1. Type `n` — Creates a new partition.
2. Type `p` — Selects a primary partition type. (Note: On GPT disks or certain fdisk versions, it may skip this prompt and move directly to partition numbering).
3. Type `1` — Assigns `1` as the partition number.
4. Press <kbd>Enter</kbd> — Accepts the default starting sector (2048).
5. Press <kbd>Enter</kbd> — Accepts the default ending sector, allocating the full 30 GiB capacity to the partition.
6. Type `w` — Writes the new partition table to disk and exits fdisk.

Here is the complete terminal interaction:


```bash
root@darkstar:~# fdisk /dev/vda

Welcome to fdisk (util-linux 2.42.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS (MBR) disklabel with disk identifier 0x66aa0c2c.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-62914559, default 2048): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-62914559, default 62914559): 

Created a new partition 1 of type 'Linux' and of size 30 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

To verify that the new partition was created successfully, execute:

```bash
root@darkstar:~# fdisk -l
Disk /dev/vda: 30 GiB, 32212254720 bytes, 62914560 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x66aa0c2c

Device     Boot Start       End  Sectors Size Id Type
/dev/vda1        2048  62914559 62912512  30G 83 Linux


Disk /dev/sda: 90 GiB, 96636764160 bytes, 188743680 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: AEAF9752-02D6-494B-8878-6BB396807DF7

Device         Start       End   Sectors  Size Type
/dev/sda1       2048    206847    204800  100M EFI System
/dev/sda2     206848   2303999   2097152    1G Linux filesystem
/dev/sda3    2304000  10692607   8388608    4G Linux swap
/dev/sda4   10692608 188741631 178049024 84.9G Linux filesystem
```

Now that `/dev/vda1` exists, a filesystem must be written to the partition before it can store data. In Linux, filesystems are created using tools from the mkfs (make filesystem) family.

To format the partition with ext4 (the standard general-purpose filesystem in Slackware):

```bash
root@darkstar:~# mkfs.ext4 /dev/vda1
mke2fs 1.47.4 (6-Mar-2025)
64-bit filesystem support is not enabled.  The larger fields afforded by this fe
Discarding device blocks: done
Creating filesystem with 7864064 4k blocks and 1966080 inodes
Filesystem UUID: 9fc1a090-b99a-468c-9dcd-15a82503ef5f
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
```

> Note: To format the partition using a different filesystem, use the corresponding tool, such as `mkfs.xfs /dev/vda1`, `mkfs.btrfs /dev/vda1`, or `mkfs.vfat /dev/vda1`.


That it! The disk is done to use.


## 11.5 Using `mount`, `umount`, and `/etc/fstab`

Now that a partition has been created and formatted (as demonstrated in the previous section with `/dev/vda1`), the filesystem must be **mounted** onto a directory before it can be used. 

In Linux, all storage devices are attached somewhere beneath the single root directory (`/`). There are no drive letters (such as `C:` or `D:`) like those found in Microsoft Windows.

To attach a filesystem to the directory tree, we use the `mount` command. The target directory where the filesystem is attached is called a **mount point**. A standard location for temporarily mounting storage drives in Slackware is under `/mnt` (for example, `/mnt/hd`).

The basic syntax for the `mount` command is:

```bash
darkstar:~# mount -t ext4 /dev/vda1 /mnt/hd

```

By default, when no specific options are declared, `mount` attaches the disk in read-write mode (`rw`) with standard system defaults. However, custom behavior can be defined using the `-o` flag.

Below are some of the most common mount options:


| ro | read-only |
| --- | --- |
| `rw` | Mounts the filesystem in read-write mode (default) |
| `ro` | Mounts the filesystem in read-only mode (prevents any changes) |
| `defaults` | Applies standard default options (rw, suid, dev, exec, auto, nouser, async). |
| `noexec` | prevent execution of any files on the filesystem |
| `nosuid` | Disables Set-User-Identifier (SUID) and Set-Group-Identifier (SGID) bits for security |
| `uid=user` | Sets the user owner for all files (essential for non-POSIX filesystems like vfat or exfat) |
| `gid=group` | Sets the group owner for all files (essential for vfat, exfat, or ntfs) |
| `umask=mask` | Defines default permission masks for filesystems lacking native Linux permissions |


When you finish using a mounted storage device (especially removable devices like USB flash drives or optical media), you must safely unmount it before removal. This ensures that all cached data in memory is completely written (flushed) to physical storage.
Unmounting is performed using the `umount` command, passing either the device node or the mount point directory:

```bash
darkstar:~# umount /mnt/hd

```


> Troubleshooting: "Target is busy" If `umount` fails with a `target is busy` (or `device is busy`) error, a process or open terminal shell is actively using a file or directory inside that mount point. Move your terminal session out of the directory (e.g., run `cd /`), close any programs accessing files on that volume, and retry `umount`.



Manually typing `mount` with full arguments every time the system boots or whenever a disk is inserted quickly becomes tedious. To automate this process, Slackware Linux relies on the `/etc/fstab` (Filesystem Table) configuration file.

The `/etc/fstab` file acts as a system table listing all block devices, their assigned mount points, filesystem types, and default options.

Let's inspect a typical Slackware `/etc/fstab` file using `cat`:

```bash
root@darkstar:~# cat /etc/fstab
/dev/sda3        swap             swap        pri=1               0   0
/dev/sda4        /                ext4        defaults            1   1
/dev/sda2        /boot            ext4        defaults            1   2
/dev/sda1        /boot/efi        vfat        defaults            1   0
#/dev/cdrom      /mnt/cdrom       auto        noauto,owner,ro,comment=x-gvfs-sho
/dev/fd0         /mnt/floppy      auto        noauto,owner        0   0
devpts           /dev/pts         devpts      gid=5,mode=620      0   0
proc             /proc            proc        defaults            0   0
tmpfs            /dev/shm         tmpfs       nosuid,nodev,noexec 0   0
```


The `/etc/fstab` file uses 6 distinct columns:

1. **Device Specifier**: The block device node (e.g., `/dev/sda1`, `/dev/sda2`)
2. **Mount Point**: The target directory where the volume is attached (e.g., `/boot` or `/`).
3. **Filesystem Type**: The filesystem driver (e.g., `ext4, vfat, swap, auto`).
4. **Mount Options**: Comma-separated mount parameters (e.g., `defaults, noauto,owner,ro,users`).
5. **Dump Frequency**: Used by the legacy dump backup utility (`0` disables dump backups).
6. **FSCK Pass Number**: Determines the check sequence for fsck at boot time (`1` for root `/`, `2` for secondary local filesystems, `0` to skip).


To ensure that the newly created partition `/dev/vda1` is automatically mounted every time Slackware Linux boots, you can add an entry for it in the `/etc/fstab` configuration file.

Using a text editor like `vi` (as covered in Chapter 12), open `/etc/fstab` with `root` privileges:


```bash
root@darkstar:~# cat /etc/fstab
/dev/sda3        swap             swap        pri=1               0   0
/dev/sda4        /                ext4        defaults            1   1
/dev/sda2        /boot            ext4        defaults            1   2
/dev/sda1        /boot/efi        vfat        defaults            1   0
/dev/vda1        /mnt/hd          ext4        defaults            0   2
#/dev/cdrom      /mnt/cdrom       auto        noauto,owner,ro,comment=x-gvfs-sho
/dev/fd0         /mnt/floppy      auto        noauto,owner        0   0
devpts           /dev/pts         devpts      gid=5,mode=620      0   0
proc             /proc            proc        defaults            0   0
tmpfs            /dev/shm         tmpfs       nosuid,nodev,noexec 0   0
```

With this entry in place, `/dev/vda1` will automatically mount to `/mnt/hd` upon every system reboot (or whenever `mount -a` is executed), making storage immediately accessible without manual intervention.


## 11.6 Network Filesystems

In addition to local filesystems, Slackware supports a number of network filesystems as both client and server. This allows you to share data between multiple computers transparently. We'll discuss the two most common: NFS and SMB.

### 11.6.1 NFS

NFS (Network File System) is a widely used protocol in UNIX and Linux environments for sharing files and directories across a network. One of its primary advantages is that it preserves native POSIX Linux file permissions (ownership, groups, and access rights) seamlessly between the client and server.

Before mounting a remote NFS share in Slackware Linux, the Remote Procedure Call (RPC) daemon must be running. Slackware manages RPC services through the `/etc/rc.d/rc.rpc` initialization script.

To enable RPC automatically at boot and start it for your current session, make the script executable and launch it:

```bash
darkstar:~# chmod +x /etc/rc.d/rc.rpc 
darkstar:~# /etc/rc.d/rc.rpc start

```

Mounting an NFS share is very similar to mounting a local filesystem. Instead of specifying a physical block device (such as `/dev/vda1`), you pass the remote server's hostname or IP address, followed by a colon (`:`) and the path to the remote exported directory:


```bash
darkstar:~# mount -t nfs darkstar.example.com:/home /home
```

In this example, the local directory `/home` acts as the mount point. All files and directories inside `/home` appear and function as if they were stored on the local hard drive, even though the data actually resides on the remote server (`darkstar.example.com`).

> Note: Setting up an NFS server requires configuring exported directories in `/etc/exports` and running `/etc/rc.d/rc.nfsd`. For details on server-side configuration, consult the exports(5) man page or official Slackware documentation.


### 11.6.2 SMB

SMB (Server Message Block) is the standard network file-sharing protocol used in Microsoft Windows environments. Connecting to SMB shares (commonly referred to as Samba shares) from a Slackware Linux client is straightforward and allows seamless connectivity across heterogeneous networks.

> Note: Exporting SMB shares from a Slackware server is handled by the Samba suite and configured via `/etc/samba/smb.conf`. Configuring Samba as a server service is beyond the scope of this chapter; consult the `smb.conf`(5) manual page or official documentation for server-side setup.

Mounting a remote SMB share works similarly to mounting an NFS share or a local filesystem. However, SMB requires specifying network location parameters, a target share name, and valid authentication credentials (username and password):

```bash
darkstar:~# mount -t cifs //darkstar/home /home -o username=name,password=secret
```

**Why cifs instead of smbfs?**

You might notice that the filesystem type specified is `cifs` rather than `smbfs`. In older Linux kernels, `smbfs` was used to mount Samba shares. However, `smbfs` has been deprecated and replaced by the modern CIFS (Common Internet File System) driver, which provides significantly better performance, enhanced security, and full POSIX compliance.


**Secure Credential Management**

Passing a clear-text password directly on the command line or storing it inside `/etc/fstab` poses a security risk. To protect sensitive credentials, you can store your login information in a restricted credentials file and reference it with the `credentials` mount option.

First, create the credentials file containing your username and password:


```bash
darkstar:~# echo "username=user" > /etc/creds-home 
darkstar:~# echo "password=secret" >> /etc/creds-home 
```

Next, restrict file permissions so that only the root superuser can read it:


```bash
darkstar:~# chmod 600 /etc/creds-home
```


Finally, mount the SMB share using the `credentials` file option:

```bash
darkstar:~# mount -t cifs //darkstar/home -o credentials=/etc/creds-home
```

Using a secured credentials file prevents unauthorized local users from viewing your network passwords in process lists or system configuration files.

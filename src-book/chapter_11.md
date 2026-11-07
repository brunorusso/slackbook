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




### 11.3. Other suportted filesystems

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


## 11.3 Using mount

Now that we've learned what (some of) the different filesystems available in Linux are, it's time we looked at how to use them. In order to read or write data on a filesystem, that filesystem must first be mounted. To do this, we (naturally) use `mount` (8). The first thing we must do is decide where we want the filesystem located. Recall that there are no such things are drive letters denoting filesystems in Linux. Instead, all filesystems are mounted on directories. The base filesystem on which you install Slackware is always located at `/` and others are always located in subdirectories of `/` . `/mnt/hd` is a common place to temporarily locate a partition, so we'll use that in our first example. In order to mount a filesystem's contents, we must tell mount what kind of filesystem we have, where to mount it, and any special options to use.

```text

darkstar:~# mount -t ext3 /dev/hda3 /mnt/hd -o ro

```

Let's disect this. We have an ext3 filesystem located on the third partition of the first IDE device, and we've decided to mount its contents on the directory `/mnt/hd` . Additionally, we have mounted it read-only so no changes can be made to these contents. The `-t ext3` argument tells `mount` what type of filesystem we are using, in this case it is ext3. This lets the kernel know which driver to use. Often `mount` can determine this for itself, but it never hurts to explicitly declare it. Second, we tell `mount` where to locate the filesystem's contents. Here we've chosen `/mnt/hd` . Finally, we must decide what options to use if any. These are declared with the `-o` argument. A short-list of the most common options follows.

| ro | read-only |
| --- | --- |
| rw | read-write (default) |
| uid | user to own the contents of the filesystem |
| gid | group to own the contents of the filesystem |
| noexec | prevent execution of any files on the filesystem |
| defaults | sane defaults for most filesystems |

If this is your first Linux installation, the only options you typically need to be concerned about are `ro` and `rw` . The exception to this rule comes when you are dealing with filesystems that don't handle traditional Linux permissions such as vfat or NTFS. In those cases you'll need to use the `uid` or `gid` options to allow non-root users access to these filesystems.

```text

darkstar:~# mount -t vfat /dev/hda4 /mnt/hd -o uid=alan

```

But Alan, that's appalling! I don't want to have to tell mount what filesystem or options to use everytime I load a CD. It should be easier than that. Well thankfully, it is. The `/etc/fstab` file contains all this information for filesystems that the installer sets up for you, and you can make additions to it as well. `fstab` (5) looks like a simple table containing the device to mount along with its filesystem type and optional arguments. Let's take a look.

```text

darkstar:~# cat /etc/fstab
/dev/hda1        /                reiserfs    defaults               1   1
/dev/hda2        /home            reiserfs    defaults               1   2
/dev/hda3        swap             swap        defaults               0   0
/dev/cdrom       /mnt/cdrom       auto        noauto,owner,ro,users  0   0
/dev/fd0         /mnt/floppy      auto        noauto,owner           0   0
devpts           /dev/pts         devpts      gid=5,mode=620         0   0
proc             /proc            proc        defaults               0   0

```

If you have an entry in `fstab` for your filesystem, you need only tell mount the device node or the mount location.

```text

darkstar:~# mount /dev/cdrom 
darkstar:~# mount /home

```

One final use for `mount` is to tell you what filesystems are currently mounted and with what options. Simply run `mount` without any arguments to display these.

## 11.4 Network Filesystems

In addition to local filesystems, Slackware supports a number of network filesystems as both client and server. This allows you to share data between multiple computers transparently. We'll discuss the two most common: NFS and SMB.

### 11.4.1 NFS

NFS is the Network File System for Linux as well as several other common operating systems. It has modest performance but supports the full range of permissions for Slackware. In order to use NFS as either a client or a server, you must run the remote procedure call daemon. This is easily accomplished by setting the `/etc/rc.d/rc.rpc` file executable and telling it to start. Once it has been set executable, it will run automatically every time you boot into Slackware.

```text

darkstar:~# chmod +x /etc/rc.d/rc.rpc 
darkstar:~# /etc/rc.d/rc.rpc start

```

Mounting an NFS share is little different than mounting a local filesystem. Rather than specifying a local device, you must tell mount the domain name or IP address of the NFS server and the directory to mount with a colon between them.

```text

darkstar:~# mount -t nfs darkstar.example.com:/home /home

```

Running an NFS server is a little bit different. First, you must configure each directory to be exported in the `/etc/exports` file. `exports` (5) contains information about what directories will be shared, who they will be shared with, and what special permissions to grant or deny.

```text

#See exports(5) for a description. 
#This file contains a list of all directories exported to other computers. 
#It is used by rpc.nfsd and rpc.mountd. 

/home/backup 192.168.1.0/24(sync,rw,no_root_squash)

```

The first column in `exports` is a list of the files to be exported via NFS. The second column is a list of what systems may access the export along with special permissions. You can specify hosts via domain name, IP address, or netblock address (as I have here). Special permissions are always a parenthetical list. For a complete list, you'll need to read the man page. For now, the only special option that matters is `no_root_squash` . Usually the root user on an NFS client cannot read or write an exported share. Instead, the root user is "squashed" and forced to act as the nobody user. `no_root_squash` prevents this.

You'll also need to run the NFS daemon. Starting and stopping NFS server support is done with the `/etc/rc.d/rc.nfsd` rc script. Set it executable and run it just like we did for `rc.rpc` and you are ready to go.

### 11.4.2 SMB

SMB is the Windows network file-sharing protocol. Connecting to SMB shares (commonly called samba shares) is fairly straight forward. Unfortuantely, SMB isn't as strongly supported as NFS. Still, it offers higher performance and connectivity with Windows computers. For these reasons, SMB is the most common network file-sharing protocol deployed on local networks. Exporting SMB shares from Slackware is done through the samba daemon and configured in `smb.conf` (5). Unfortunately configuring samba as a service is beyond the scope of this book. Check online for additional documentation, and as always refer to the man page.

Thankfully mounting an SMB share is easy and works almost exactly like mounting an NFS share. You must tell mount where to find the server and what share you wish to access in exactly the same way. Additionally, you must specify a username and password.

```text

darkstar:~# mount -t cifs //darkstar/home /home -o username=alan,password=secret

```

You may be wondering why the filesystem type is cifs instead of smbfs. In older versions of the Linux kernel, smbfs was used. This has been deprecated in favor of the better performing and more secure general purpose cifs driver.

All SMB shares require the `username` and `password` arguments. This can create a security problem if you wish to place your samba share in fstab. You may avoid this problem by using the `credentials` argument. `credentials` points to a file which contains the username and password information. As long as this file is safely guarded and readable only by root, the likelyhood that your authentication credentials will be compromised is lessened.

```text

darkstar:~# echo "username=alan" > /etc/creds-home 
darkstar:~# echo "password=secret" >> /etc/creds-home 
darkstar:~# mount -t cifs //darkstar/home -o credentials=/etc/creds-home

```

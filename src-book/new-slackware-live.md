# 20. Slackware Live Edition

## 20.1 Introduction to Slackware Live Edition

**Slackware Live Edition** is an official-equivalent, portable live operating system created and maintained by Eric Hameleers (Alien BOB). Built using the `liveslak` toolset, Slackware Live Edition runs entirely from a DVD, USB flash drive, or ISO file without modifying local hard drive partitions unless explicitly commanded to do so.

Unlike many derivative distributions that heavily modify the underlying system, alter desktop themes, or strip out core server utilities, Slackware Live Edition remains 100% faithful to stock Slackware. It ships with un-patched stock kernels, standard Slackware package series, and default configuration files, providing an authentic Slackware experience in a zero-installation format.

### Primary Goals and Design Philosophy

The `liveslak` project was designed around several core principles:

* **Showcase Pure Slackware:** Provide a pristine, unadulterated Slackware environment for evaluation, demonstration, and educational purposes without hiding kernel boot messages or forcing custom branding.
* **Track the Bleeding Edge (`-current`):** Offer a safe, risk-free environment to test Slackware's development tree (`-current`) on real hardware without risking productivity loss or system breakage on primary workstation drives.
* **Deterministic, Scripted Builds:** Generate ISO images completely from scratch using standard Slackware package mirrors via reproducible Bash scripts.
* **KISS Principle (Keep It Simple, Stupid):** Leverage stock Linux kernel features—specifically `OverlayFS` and `SquashFS`—without requiring custom-compiled third-party kernel patches or out-of-tree file system drivers.
* **Portability with Persistence:** Enable users to carry a fully configured Slackware OS in their pocket on a USB stick, retaining file changes, custom software, and encrypted user home directories across reboots.

### Default User Credentials and System State

When booted, Slackware Live Edition configures two standard user accounts:

* **`live`** (Password: `live`): The default unprivileged user account.
* **`root`** (Password: `root`): The system administrator account.

By default, the ISO images boot directly into **runlevel 4** (graphical desktop mode with display manager login), though users can easily select runlevel 3 (multi-user console mode) or single-user mode at the boot prompt.

---

## 20.2 Core Architecture: OverlayFS and SquashFS

Slackware Live Edition achieves its flexibility through a combination of two core Linux kernel technologies: **SquashFS** (a read-only compressed file system) and **OverlayFS** (a union mount file system driver integrated into Linux kernel 4.x and newer).

### File System Assembly

During ISO creation, Slackware packages are grouped and compressed into individual read-only SquashFS archive modules with the `.sxz` extension (SquashFS compressed with `xz` or `zstd`). When the system boots:

1. The initial RAM file system (`initrd`) creates a temporary RAM-based root file system.
2. The `liveslak` `init` script detects the boot media and loop-mounts each `.sxz` module in a specific numeric sequence.
3. **OverlayFS** stacks these read-only layers into a single unified directory tree.
4. On top of the read-only stack, OverlayFS places a **writable upper layer**:
   * **Volatile Mode (RAM):** For read-only media (DVDs) or unconfigured USBs, writes are held in a RAM disk and discarded upon reboot.
   * **Persistent Mode (USB/Disk):** For configured USB drives or container files, write operations are stored permanently on disk.

### Module Naming and Prefix Conventions

Modules in `/liveslak/system/`, `/liveslak/addons/`, and `/liveslak/optional/` follow a strict numeric naming convention (`NNNN-modname-version-arch.sxz`) that dictates their loading order:

| Prefix Range | Module Purpose & Contents |
| :--- | :--- |
| `0000` | Contains the core Slackware `/boot` directory and kernel structures. |
| `0005` | Console OS modules (minimal RAM-based rescue environment). |
| `0010`–`0019` | Modules generated from Slackware series tagfiles (`a`, `ap`, `d`, `l`, `n`, `x`, `xap`, etc.). |
| `0020`–`0029` | Modules generated from custom package lists (`pkglists/*.lst`). |
| `0030`–`0039` | Modules generated from local package directories (`./local/` or `./local64/`). |
| `0099` | Live OS configuration module (`0099-slackware_zzzconf-*.sxz`), containing user setup, hardware tweaks, and system scripts. |
| `0040`–`0098` | Free range reserved for user-created custom addon modules. |

---

## 20.3 Available ISO Variants (Flavors)

The `liveslak` framework supports building multiple official ISO variants tailored to different hardware constraints and workflow requirements:

| Variant Name | Target Desktop Environment | ISO Size | Description & Key Features |
| :--- | :--- | :--- | :--- |
| **`SLACKWARE`** | KDE Plasma | ~4.5 GB | Complete 64-bit Slackware installation containing all official package series. |
| **`XFCE`** | XFCE (with XDM) | ~1.1 GB | Lightweight, compact edition designed to fit on 1 GB USB drives; ideal for older hardware. |
| **`LEAN`** | Minimal Plasma | ~2.5 GB | Reduced package set based on Plasma Desktop without extra heavyweight applications. |
| **`DAW`** | Plasma Desktop | ~3.6 GB | Digital Audio Workstation flavor loaded with digital audio, MIDI, and music production tools. |
| **`MATE`** | MATE (GNOME 2 fork) | ~4.2 GB | Replaces KDE Plasma with the MATE desktop environment. |
| **`CINNAMON`** | Cinnamon | ~4.2 GB | Replaces KDE Plasma with the Cinnamon desktop environment. |

*(Note: Legacy variants such as `DLACKWARE` and `STUDIOWARE` were discontinued after Slackware 14.2).*

---

## 20.4 Downloading Slackware Live

Official pre-built ISO images for stable Slackware releases and the `-current` development branch are hosted across several public mirrors:

* **Primary Repository:** `https://download.liveslak.org/` (rsync: `rsync://liveslak.org/liveslak/`)
* **US Mirror:** `https://us.liveslak.org/` (rsync: `rsync://us.liveslak.org/liveslak/`)
* **UK Mirror:** `https://slackware.uk/liveslak/` (rsync: `rsync://slackware.uk/liveslak/`)
* **Asian Mirror:** `http://repo.ukdw.ac.id/slackware-live/`

Always verify the downloaded ISO file against its provided MD5 checksum prior to writing it to boot media:

```text
darkstar:~$ md5sum -c slackware64-live-current.iso.md5
```

---

## 20.5 Booting and Hardware Compatibility

Slackware Live Edition ISOs are **hybrid ISOs**, meaning they can be burned directly to optical DVDs or copied verbatim to raw USB block devices using `dd` or `cp`:

```text
darkstar:~# dd if=slackware64-live-xfce-current.iso of=/dev/sdX bs=1M status=progress; sync
```

### BIOS Booting (Syslinux)

On legacy BIOS systems, Syslinux handles the boot process (`isolinux` on ISOs, `extlinux` on ext4 USB partitions). Pressing <kbd>Tab</kbd> at the Syslinux boot prompt allows editing kernel parameters directly before pressing <kbd>Enter</kbd> to boot.

### UEFI Booting (GRUB2)

On modern UEFI systems, GRUB2 presents an interactive boot menu. Pressing the <kbd>e</kbd> key on a GRUB menu item opens the command line editor. Press <kbd>F10</kbd> or <kbd>Ctrl+x</kbd> to boot with modified parameters, or <kbd>Esc</kbd> to discard changes.

### UEFI Secure Boot Support

Starting with `liveslak-1.5.0`, 64-bit Slackware Live ISOs include full support for UEFI Secure Boot. Because Slackware does not officially ship a Microsoft-signed bootloader, `liveslak` incorporates a signed 3rd-party `shim` binary (`/EFI/BOOT/bootx64.efi`, extracted from distribution packages like Fedora, Debian, or openSUSE).

`shim` validates GRUB and kernel binaries using an **Alien BOB public SSL certificate**. To boot on a Secure Boot system, you must enroll this certificate into your machine's **MOK (Machine Owner Key)** database:

1. **Automatic First Boot Enrollment:** On first boot, `shim` will fail validation and launch **MokManager** (a blue dialog screen). Select **Enroll key from disk**, navigate to the EFI partition's `/EFI/BOOT/` directory, select `liveslak.der`, confirm enrollment, and reboot.
2. **Pre-enrollment via Linux (`mokutil`):** If running an existing Linux system, pre-import the public key before booting the Live media:
   ```text
   darkstar:~# mokutil --import liveslak.der
   ```

---

## 20.6 Transferring to USB with Persistence (`iso2usb.sh`)

While `dd`-ing an ISO to a USB drive creates a functional bootable drive, it results in an immutable read-only system. The `iso2usb.sh` script transforms a raw USB drive into a fully persistent, multi-partition Slackware Live system.

### USB Disk Partition Layout

Running `iso2usb.sh` wipes and partitions the target USB device into three (or four) partitions:

1. **Partition 1 (1 MB FAT):** Reserved for alternative bootloaders or storing LUKS keyfiles.
2. **Partition 2 (100 MB VFAT):** EFI System Partition (ESP) containing GRUB2, Syslinux, kernels, and `initrd`.
3. **Partition 3 (Linux ext4):** Occupies remaining free space; stores `/liveslak` SquashFS modules, persistent system changes, and user files.
4. **Partition 4 (Optional):** Reserved custom unformatted partition specified via `-y|--layout`.

### `iso2usb.sh` Command Reference

```text
darkstar:~# ./iso2usb.sh -i <path-to-iso> -o /dev/sdX [options]
```

Key command-line parameters include:

* **`-i|--infile <file>`:** Full path to the input Slackware Live ISO file.
* **`-o|--outdev <device>`:** Target USB device node (e.g., `/dev/sdX`—specify the whole drive, not a partition).
* **`-c|--crypt <size|perc>`:** Creates a **LUKS-encrypted `/home`** partition/container (e.g., `-c 2G`, `-c 25%`).
* **`-C|--cryptpersistfile <size|perc>`:** Creates a **LUKS-encrypted persistence container** file instead of a plain directory.
* **`-P|--persistfile`:** Creates an unencrypted sparse container file for persistence (useful on VFAT file systems).
* **`-F|--filesystem <fs>`:** Specifies file system type for Linux partitions (`ext4` [default], `btrfs`, `xfs`, `f2fs`).
* **`-r|--refresh`:** Refreshes system modules on an existing Live USB without wiping user data or reformatting.
* **`-w|--wait <seconds>`:** Increases USB storage detection delay during boot (essential for slow USB media).

### Practical `iso2usb.sh` Examples

* **Create a standard Live USB with encrypted `/home` (750 MB):**
  ```text
  darkstar:~# ./iso2usb.sh -i slackware64-live-current.iso -o /dev/sdX -c 750M -w 10
  ```
* **Create a fully encrypted USB (30% space for LUKS `/home`, 500 MB LUKS persistence):**
  ```text
  darkstar:~# ./iso2usb.sh -i slackware64-live-current.iso -o /dev/sdX -c 30% -C 500M
  ```
* **Refresh system modules on an existing Live USB drive:**
  ```text
  darkstar:~# ./iso2usb.sh -i slackware64-live-current.iso -r -s
  ```

---

## 20.7 Direct ISO Booting and Ventoy Integration (`isocomp.sh`)

Slackware Live supports booting directly from an ISO image stored on a local hard drive or multiboot USB drive (such as **Ventoy**).

### Booting ISO Files via GRUB2

To boot a downloaded ISO directly from a local partition without extracting it, add an entry to `/boot/grub/grub.cfg`:

```text
menuentry "Slackware Live ISO (XFCE)" {
    set iso='/data/ISOS/slackware64-live-xfce-current.iso'
    set bootparms='load_ramdisk=1 prompt_ramdisk=0 rw kbd=us tz=America/New_York lang=en_US'
    search -f $iso --set=root
    loopback loop $iso
    linux (loop)/boot/generic livemedia=scandev:$iso $bootparms
    initrd (loop)/boot/initrd.img
}
```

### Adding Persistence to ISO Booting with `isocomp.sh`

Because ISO files are inherently read-only, booting directly from an ISO normally lacks persistence. The companion script **`isocomp.sh`** overcomes this by generating encrypted LUKS container files (`.icc`) and directory structures alongside the ISO file on disk.

#### Common `isocomp.sh` Operations

* **Create a 2 GB encrypted persistence container for a Ventoy ISO:**
  ```text
  darkstar:~# ./isocomp.sh -p /mnt/Ventoy/livefiles/persistence.icc -P 2G
  ```
* **Create a 4 GB encrypted `/home` container:**
  ```text
  darkstar:~# ./isocomp.sh -l /mnt/Ventoy/livefiles/slhome.icc -L 4G -i /mnt/Ventoy/slackware64-live-current.iso
  ```
* **Create custom module directory structures (`/liveslak/addons/` and `/liveslak/optional/`):**
  ```text
  darkstar:~# ./isocomp.sh -d /mnt/Ventoy/custom_liveslak -i /mnt/Ventoy/slackware64-live-current.iso
  ```

Settings generated by `isocomp.sh` are saved in a `.cfg` file alongside the ISO (e.g., `slackware64-live-current.cfg`) and automatically parsed by `liveslak` during startup.

---

## 20.8 Custom Modules and Package Creation (`makemod`)

The **`makemod`** utility converts any standard Slackware package (`.txz`/`.tgz`) or compiled directory tree into a SquashFS `.sxz` Live module.

### `makemod` Usage Syntax

```text
darkstar:~# makemod <package-or-directory> <output-module.sxz>
```

### Step-by-Step Workflow

1. Convert a custom Slackware package into a Live module:
   ```text
   darkstar:~# makemod htop-3.2.2-x86_64-1.txz 0040-htop-3.2.2-x86_64.sxz
   ```
2. Place the resulting module into the Live environment:
   * **Automatic Loading:** Copy to `/liveslak/addons/` on your persistent USB drive.
   * **On-Demand Loading:** Copy to `/liveslak/optional/` (activated at boot via `load=htop`).

---

## 20.9 Hard Drive Installation (`setup2hd`)

Slackware Live Edition includes **`setup2hd`**, a specialized version of the standard Slackware installer that allows transferring the Live OS directly onto a local hard drive.

### Key Advantages of `setup2hd`

* **Graphical Environment Execution:** `setup2hd` can be launched from an X terminal emulator inside runlevel 4. Users can continue web browsing, listening to music, or working while the installation proceeds in the background.
* **Automatic Partitioning Prompts:** Automatically launches `fdisk` or `gdisk` if no target Linux partitions are configured.
* **Integrated User Creation:** Prompts for non-root user account creation and root password setup during the installation flow.
* **Optional Automated Firewall Setup:** Prompts to configure a basic stateful iptables firewall during setup.

To launch the installer, open a terminal as `root` and run:

```text
darkstar:~# setup2hd
```

`setup2hd` extracts all currently active SquashFS modules directly onto the designated hard drive partitions, converts the Live setup into a standard installation, and runs `lilo`/`elilo` configuration before rebooting.

---

## 20.10 Kernel Upgrades and Maintenance (`upslak.sh`)

Managing and updating a persistent Live USB drive over time is handled by the **`upslak.sh`** administrative tool.

### Primary Functions of `upslak.sh`

* **Upgrade Kernel and Modules:** Replaces the kernel image and initrd on the USB boot partition, automatically generating a matching `kernelmodules` SquashFS addon module in `/liveslak/addons/`.
* **Restore Backed-Up Kernel:** Restores previous kernel binaries (`.prev`) if a new kernel fails to boot.
* **Extend LUKS Container Size:** Expands pre-existing encrypted `/home` or persistence containers without touching user data.
* **Consolidate Persistence into an Addon Module:** Captures accumulated persistent changes and compresses them into a timestamped SquashFS addon module (`0099-slackware__customchanges-YYYYMMDDhhmmss.sxz`), resetting the persistence storage space.

### Practical `upslak.sh` Examples

* **Upgrade kernel on USB device `/dev/sdX` using new TXZ packages:**
  ```text
  darkstar:~# ./upslak.sh -o /dev/sdX -k kernel-generic-5.15.19-x86_64-1.txz -m kernel-modules-5.15.19-x86_64-1.txz
  ```
* **Extend an encrypted home container (`slhome.img`) by 3 GB:**
  ```text
  darkstar:~# ./upslak.sh -s -x /slhome.img -X 3G
  ```
* **Bundle accumulated persistence changes into a permanent addon module:**
  ```text
  darkstar:~# ./upslak.sh -o /dev/sdX -p
  ```

---

## 20.11 Network Booting and PXE Server (`pxeserver`)

Slackware Live Edition can function both as a **PXE network boot client** and as a **standalone PXE boot server**.

### Functioning as a PXE Client

To boot Slackware Live over the network from an NFS export, configure your TFTP/PXE bootloader (`pxelinux.cfg/default`) with the `nfsroot` boot parameter:

```text
label liveslak
    kernel slackware-live/boot/generic
    append initrd=slackware-live/boot/initrd.img rw nfsroot=192.168.1.10:/tftpboot/slackware-live dhcpwait=30 hostname=pxelive
```

### Running a Standalone PXE Server (`pxeserver`)

The `pxeserver` script allows a running Live USB session to transform the host machine into a network boot server for an entire local area network (LAN):

```text
darkstar:~# pxeserver eth0
```

1. **Service Orchestration:** Starts `dnsmasq` (providing DHCP, DNS, and TFTP services) and configures NFS/RPC exports.
2. **RAM Optimization (`toram`):** Recommends booting the host with `toram` so that disk I/O from multiple network clients does not saturate USB flash drive bandwidth.
3. **Automatic Routing & NAT:** Automatically configures IP forwarding and optional IP masquerading (NAT) if the server machine possesses a secondary network interface connected to the Internet.

---

## 20.12 Reference: Essential Boot Parameters

Custom boot parameters can be appended at the Syslinux or GRUB prompt to modify Slackware Live behavior:

### System & Localization Options

* **`0` | `1` | `2` | `3` | `4` | `5` | `S`:** Specifies boot runlevel (default is `4` for graphical login; `3` for console mode).
* **`kbd=us` / `xkb=us`:** Sets console keyboard mapping and X11 keyboard layout/variants.
* **`locale=en_US.utf8` / `tz=America/New_York`:** Sets system locale and timezone.
* **`livepw="secret"` / `rootpw="secret"`:** Sets plain-text passwords for `live` and `root` accounts (`livepw=""` removes password).
* **`hostname=myhost` / `domain=mydomain`:** Configures custom network hostname and domain.

### Module & Storage Control

* **`load=mod1,mod2`:** Forces loading specified SquashFS modules from `/liveslak/optional/`.
* **`noload=mod1,mod2`:** Prevents loading specified SquashFS modules from `/liveslak/addons/`.
* **`toram` / `toram=all`:** Copies all SquashFS modules into physical RAM on boot, allowing safe removal of USB media.
* **`toram=core`:** Loads only minimal rescue Console OS modules into RAM.
* **`nop`:** Disables persistence, booting into a clean virgin state.
* **`nop=wipe`:** Wipes all persistent data from the persistence directory/container upon boot.
* **`luksvol=/slhome.img:/home`:** Specifies LUKS container path and target mount point.

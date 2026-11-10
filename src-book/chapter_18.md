# 18. Keeping Track of Updates

## 18.1 The -stable Branch

After a new version of Slackware is released, the Slackware development team releases updated packages to fix security vulnerabilities and critical bugs as needed. Therefore, it is essential to stay up to date with patches released for your specific release of Slackware, officially referred to as the **-stable** branch. 

There is also a **-current** branch, which serves as the active development tree for the next upcoming stable release. Because **-current** undergoes frequent and potentially disruptive updates, running it requires a willingness to handle system breakage and troubleshoot issues independently. For daily use and production environments, sticking with the **-stable** branch is strongly recommended.

Since **-stable** package updates are released after official installation media are produced, they must be downloaded from the Internet. Numerous organizations and universities worldwide maintain public Slackware mirrors containing the full repository tree, like this example: https://mirrors.slackware.com/slackware/slackware-15.0/  (or specifically the `patches/` directory).

Updates can be accessed via **HTTP/HTTPS**, **FTP**, or synchronized using **rsync**. To locate an official or geographically close mirror, consult the Slackware mirror list at [https://www.slackware.com/getslack/](https://www.slackware.com/getslack/). Choosing a mirror geographically close to your location ensures faster transfer speeds and reduces overall network latency.

**Monitoring Updates via ChangeLog.txt**

The most reliable way to monitor security patches and package revisions is by inspecting the `ChangeLog.txt` file maintained at the root of every updated mirror repository.

You can inspect the `ChangeLog.txt` file directly from your terminal using `wget` piped into `less`:

```bash
darkstar:~$ wget -O - https://mirrors.slackware.com/slackware/slackware-15.0/ChangeLog.txt | less
Sat Nov  7 23:41:05 UTC 2026
patches/packages/ca-certificates-20261107-noarch-1_slack15.0.txz:  Upgraded.
  This update provides the latest CA certificates to check for the
  authenticity of SSL connections.
+--------------------------+
Fri Nov  6 23:52:17 UTC 2026
patches/packages/httpd-2.4.70-i586-1_slack15.0.txz:  Upgraded.
  This update fixes bugs and security issues.
  For more information, see:
    https://downloads.apache.org/httpd/CHANGES_2.4.70
  (* Security fix *)
... more and more lines ..
```

## 18.2 Security Update Mailing List

While the Slackware team occasionally releases updated bugfix-only packages, most system administrators are primarily interested in security advisories for vulnerabilities discovered after a **-stable** release.

To keep users informed, the Slackware development team maintains an official mailing list that delivers advisories whenever updated packages are issued for critical security issues.

**Subscribing to the Security List**

To subscribe to the mailing list:

1. Send an email to `<majordomo@slackware.com>`.
2. In the subject line use subscribe `slackware-security` and place the following single line in the **body** of the message:
   
```text
subscribe slackware-security
```

## 18.3 Slackware's Roadmap

By default, Slackware does not follow a fixed business roadmap or a rigid release schedule, as target release dates in software development are often pure speculation. It is impossible to predict exactly how much time is required to integrate major upstream package updates, resolve complex dependencies, and thoroughly test system stability.

As new packages and components are prepared for an upcoming release, they are continuously built and uploaded into the **-current** development tree. If the **-current** tree is temporarily frozen or unlinked on repository mirrors, it typically indicates that a new stable version of Slackware has just been officially released. A new **-current** tree is initialized shortly after each stable release to begin the next development cycle.


## 18.4 Development version
As noted earlier, the active development version of Slackware is publicly accessible within the **-current** directory across official repository mirrors.

For 64-bit x86_64 architectures, the primary development tree can be browsed at:

* **Slackware 64-bit `-current` Mirror:** [https://mirrors.slackware.com/slackware/slackware64-current/](https://mirrors.slackware.com/slackware/slackware64-current/)

Users and testers who wish to follow ongoing changes, inspect new package additions, or update a testing machine can sync directly against this tree using mirrors, `rsync`, or package management tools configured for the **-current** branch.


## 18.5 Upgrading Slackware Versions

Upgrading from one major release of Slackware to another is considerably more complex than simply updating individual security patches. Each new release introduces widespread changes—and while many are minor, some structural changes can cause severe system breakage if you do not prepare for them properly.

Unlike many Linux distributions that rely on fully automated upgrade scripts, Slackware maintains a **hands-on philosophy**, putting you in full control of the upgrade process (I love it!).


**Step-by-Step Upgrade Guidelines**

Before attempting an operating system upgrade, follow these essential guidelines:

1. **Evaluate Necessity:**
   The most important (and frequently overlooked) step is deciding whether an upgrade is actually necessary. If your current installation is stable, secure, and fully meets your operational requirements, upgrading to a newer release may not be needed.

2. **Read `CHANGES_AND_HINTS.TXT`:**
   If you decide to proceed, carefully read the `CHANGES_AND_HINTS.TXT` file located on your installation media or mirror repository. This document is actively updated during each development cycle and details key architecture changes, deprecated packages, and workarounds.

3. **Consult `UPGRADE.TXT`:**
   Thoroughly read `UPGRADE.TXT` before executing any commands. This file outlines the official, recommended sequence of package upgrades and configuration adjustments required for a successful transition.

4. **Create Full Backups:**
   Always back up critical configuration files and personal data before starting an upgrade. At a minimum, create backups of the **`/etc`** (system configurations) and **`/home`** (user data) directories. Having complete backups ensures you can restore your system or perform a clean installation if the upgrade encounters critical issues.


**Fresh Install vs. In-Place Upgrade**

After reviewing `CHANGES_AND_HINTS.TXT` and `UPGRADE.TXT`, many system administrators find that backing up user data and performing a **fresh installation** of the new Slackware release is cleaner, faster, and far less prone to configuration conflicts than attempting a complex in-place upgrade.

Because every new version of Slackware introduces unique changes, static instructions in external guides quickly become outdated. **Always rely directly on the official documentation included on your Slackware installation media or repository mirror.**


## 18.6 Practical Upgrade Workflow

After evaluating the benefits and risks of upgrading to a new Slackware version, you can proceed with the upgrade process. While the exact procedures may vary slightly between releases, the general workflow follows the official `UPGRADE.TXT` guidelines:

1. **Download the new package tree:** Download all packages for the target Slackware release from an official mirror (or mount the installation DVD/ISO).
2. **Follow the recommended `UPGRADE.TXT` sequence:**
   1. **Switch to single-user mode:** Run `init 1` to prevent active background daemons and user sessions from interfering with library updates.
   2. **Remove obsolete packages:** Remove packages that have been deprecated or renamed in the new release using `removepkg`.
   3. **Upgrade `glibc` shared libraries:** Upgrade core system C libraries first (`glibc-solibs`) so that existing binaries continue to function smoothly during the upgrade process.
   4. **Upgrade package management tools:** Update `pkgtools` (including `installpkg` and `upgradepkg`) to ensure compatibility with any new package features or compression formats.
   5. **Upgrade all remaining packages:** Run `upgradepkg --install-new` to upgrade installed packages and install any new core packages introduced in the release.
   6. **Review and update configuration files:** Check `/etc` for new configuration files generated with `.new` extensions and merge necessary changes into your active configuration.
   7. **Update the bootloader:** Re-run `lilo` (or update your ELILO/GRUB configuration) to ensure the bootloader points to the newly installed kernel.
   8. **Reboot the system:** Restart the machine to load the new kernel and updated system environment.

> **Warning:** Specific upgrade steps can vary depending on the release. Always read the official `UPGRADE.TXT` file included with your target Slackware version before performing an upgrade.



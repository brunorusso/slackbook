# 22. Slackware ARM

Slackware ARM is the official port of Slackware Linux for 32-bit (ARM) and 64-bit (AArch64) architectures. The project was created, developed, and continues to be maintained by **Stuart Winter** (`MoZes@slackware`), Slackware's ARM Platform Architect and Developer. **Brent Earl**, a member of the Slackware Core Team, assists with research, development, testing, and hardware support across various device models.


## 22.1 Project Goals and Philosophy

The Slackware ARM project aligns closely with the core UNIX design principles of Slackware while adapting to the unique characteristics of the ARM ecosystem.

### Personal and Educational Goals

* **Engaging Technical Challenge:** Serves as a hands-on technical project that keeps developers and users intimately connected with UNIX-style operating system internals.
* **Community Collaboration:** Fosters a collaborative environment for like-minded developers and enthusiasts to maintain an architecture-specific port.
* **Educational Outreach:** Functions as an educational tool for learning low-level system design, supported through official documentation and community media channels.




## 22.2 Technical Design Goals

Because the ARM hardware landscape differs significantly from traditional x86 systems, Slackware ARM establishes clear technical objectives:

* **Consistent User Experience:** Delivers an operating system environment and administrative workflow that mirrors the traditional x86/x86_64 Slackware experience as closely as possible.
* **Standard Slackware Installer:** Retains the familiar `setup`-based text interface for installation.
* **Mainline Linux Kernel:** Relies on official mainline kernel sources with minimal downstream patching to ensure long-term stability and upstream compatibility.
* **Selective Package Management:** Includes only additional packages necessary for platform-specific hardware support, SoC initialization, or native operating system compilation.
* **Intentional Package Omissions:** Excludes x86-only software (such as legacy x86 bootloaders or graphics drivers for hardware non-existent on ARM) and packages that cannot be built for the architecture.
* **Standards-Based Booting:** Follows community and industry boot standards (such as U-Boot and UEFI/EDK2) across supported hardware platforms.



## 22.3 Installation Overview

Unlike the standardized x86 architecture where a single installation image boots almost any machine via standard BIOS or UEFI, ARM devices rely on diverse System-on-Chip (SoC) designs, custom firmware implementations, and Device Tree descriptions.

Consequently, while the installation process utilizes the familiar Slackware installer interface, the initial boot setup and storage preparation depend on your specific hardware model.

**Official Documentation & Board Support:**
Before attempting an installation, consult the official Slackware ARM installation guide for device-specific instructions, firmware requirements, and supported hardware models: [https://docs.slackware.com/slackwarearm:inst](https://docs.slackware.com/slackwarearm:inst)

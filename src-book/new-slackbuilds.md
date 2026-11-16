# 21. SlackBuilds.org and Custom Software Building

While official Slackware releases include a comprehensive selection of applications, libraries, desktop environments, and server utilities, users frequently require third-party software not included in the core distribution. On many other Linux distributions, installing third-party software involves adding pre-compiled binary repositories or running automated package helpers.

Slackware takes a community-driven approach. To maintain transparency, system stability, and total administrative control, the Slackware community relies on **SlackBuilds.org (SBo)**—the official community repository of build scripts.

Instead of hosting pre-compiled binary packages, SlackBuilds.org provides audited, standardized shell scripts (`.SlackBuild`) and metadata files that automate the compilation of upstream source code into native Slackware packages (`.txz`).

This chapter covers the inner mechanics of SlackBuilds.org, the structure of build script archives, manual step-by-step compilation workflows, dependency management strategies, automated build helpers like `sbopkg`, and guidelines for authoring custom SlackBuilds.

## 21.1 Introduction to SlackBuilds.org

Founded to provide a safe, organized, and standardized repository for third-party software, **SlackBuilds.org (SBo)** serves as the recognized community repository for Slackware Linux.

Rather than distributing pre-compiled binary files, SlackBuilds.org hosts light, plain-text build projects. Each project contains the instructions necessary to download upstream source code, compile it on your local system, and package the output into a clean, trackable `.txz` file compatible with Slackware's native `pkgtools` (`installpkg`, `removepkg`, `upgradepkg`).

### Core Design Philosophy

The SlackBuilds.org project adheres strictly to Slackware's core philosophy:

* **No Pre-Compiled Binaries:** All software is built from pristine upstream source code directly on the target machine. This ensures binaries are compiled against your system's exact library versions.
* **Full Package Management Integration:** Software built via SBo is registered in `/var/log/packages/`, ensuring clean uninstallation and version tracking.
* **No Unsolicited Modifications:** Build scripts avoid patching upstream source code unless necessary to fix compilation errors or adhere to standard Slackware filesystem hierarchy guidelines (`/usr`, `/usr/lib64`, `/etc`).
* **Explicit Administrative Control:** Dependency resolution is transparent. While scripts document prerequisites, the administrator retains complete control over what gets compiled and installed.


## 21.2 Anatomizing a SlackBuild Package Archive

When you download a package project from SlackBuilds.org, you receive a compressed archive (e.g., `application.tar.gz`). Unpacking this archive reveals a directory containing a standardized set of plain-text files:

| File | Purpose & Description |
| :--- | :--- |
| **`appName.SlackBuild`** | The main executable shell script that automates unpacking, configuring, compiling, staging, and archiving the application into a `.txz` package. |
| **`appName.info`** | Plain-text metadata file containing package variables, upstream download URLs, MD5 checksums, maintainer contact info, and direct dependencies. |
| **`slack-desc`** | Formatted 11-line package description file required by `installpkg` and recorded in `/var/log/packages/`. |
| **`README`** | Critical documentation detailing build prerequisites, optional compile-time flags, group/user requirements, and post-installation setup instructions. |
| *Patch/Extra files* | Optional auxiliary files such as `.patch` bug fixes, custom `.desktop` menu shortcuts, or default configuration templates. |



### 21.2.1 The Metadata File (`appName.info`)

The `.info` file provides machine-readable metadata used by build helpers and system administrators. Key metadata variables include:

* **`PRGNAM`:** The official program name (must match the script directory name).
* **`VERSION`:** The exact version of the upstream source package.
* **`DOWNLOAD` / `DOWNLOAD_x86_64`:** Direct HTTP or FTP URLs pointing to the upstream source code tarball.
* **`MD5SUM` / `MD5SUM_x86_64`:** Cryptographic MD5 checksums used to verify the integrity of the downloaded source code before compilation begins.
* **`REQUIRES`:** A space-separated list of direct prerequisite SlackBuild packages that must be installed on the system before building this script.
* **`MAINTAINER` & `EMAIL`:** Contact details of the community volunteer responsible for testing and updating the script.



### 21.2.2 The Build Script (`appName.SlackBuild`)

The `.SlackBuild` file is an executable Bourne shell script. When executed by the system administrator, it carries out the following automated build steps:

1. **Environment Initialization:** Defines compiler flags (`CFLAGS`, `CXXFLAGS`), architecture detection (`x86_64`), and directory variables (`TMP=/tmp/SBo`, `PKG=/tmp/SBo/package-appName`).
2. **Directory Cleanup:** Prepares a clean build folder in `/tmp/SBo/`.
3. **Source Unpacking:** Extracts the upstream source archive into the temporary directory and enters the source tree.
4. **Permissions Standardization:** Normalizes file ownerships and permissions to safe defaults.
5. **Compilation (`configure` & `make`):** Runs the build tools (such as `./configure`, `cmake`, or `meson`) using standard Slackware paths (`--prefix=/usr`, `--libdir=/usr/lib64`, `--sysconfdir=/etc`).
6. **Staging (`make install`):** Installs the compiled binaries, libraries, man pages, and documentation into the temporary staging directory (`$PKG`).
7. **Optimization & Compression:** Strips debugging symbols from binaries/libraries to reduce file size, compresses man pages with `gzip`, and places documentation files (`README`, `LICENSE`, `NEWS`) in `/usr/doc/appName-version/`.
8. **Package Creation (`makepkg`):** Copies `slack-desc` into `$PKG/install/slack-desc` and executes `makepkg` to generate the final `.txz` package in the target directory (defaults to `/tmp`).



### 21.2.3 The Description File (`slack-desc`)

Slackware's package tools require a formatted 11-line description file named `slack-desc`. Each descriptive line begins with the program name followed by a colon, providing a brief summary of the application's functionality and a link to its homepage.

See a example
```text
# HOW TO EDIT THIS FILE:
# The "handy ruler" below makes it easier to edit a package description.
# Line up the first '|' above the ':' following the base package name, and
# the '|' on the right side marks the last column you can put a character in.
# You must make exactly 11 lines for the formatting to be correct.  It's also
# customary to leave one space after the ':' except on otherwise blank lines.

            |-----handy-ruler------------------------------------------------------|
TriliumNotes: TriliumNotes (organize your thoughts)
TriliumNotes:
TriliumNotes: Trilium is an open-source solution for note-taking and organizing a 
TriliumNotes: personal knowledge base. Use it locally on your desktop, or sync it 
TriliumNotes: with your self-hosted server to keep your notes everywhere you go.
TriliumNotes:
TriliumNotes:
TriliumNotes: Homepage: https://triliumnotes.org/
TriliumNotes:
TriliumNotes:
TriliumNotes:
```

## 21.3 Building Software Manually with SlackBuilds

Building software manually using SlackBuilds.org scripts is straightforward and requires no third-party build tools beyond standard Slackware development package series (`d/`).

### Step-by-Step Manual Build Workflow

1. **Locate and Download the Script Archive:** Search for the desired package on SlackBuilds.org, selecting your Slackware release version (such as `15.0` or above). Download the script archive (`libmd.tar.xz`).
2. **Extract the Script Archive:** Unpack the archive with `tar -xzvf libmd.tar.gz` and enter the project folder `cd libmd/`.
3. **Download Upstream Source Code:** Inspect `libmd.info` to find the exact download URL, then download the source tarball directly into the `libmd/` directory.
4. **Inspect `README` and Prerequisites:** Read the `README` file with `cat README` to check for required build options or dependencies.
5. **Execute the Build Script:** Ensure `libmd.SlackBuild` is executable and run `./foo.SlackBuild` as superuser. Upon successful compilation, the script outputs the location of the generated package in `/tmp/`.
6. **Install the Generated Package:** Install the newly created package using `installpkg /tmp/libmd-1.1.0-x86_64-1_SBo.txz`.

```bash
darkstar:~# tar xzvf libmd.tar.gz 
darkstar:~# cd libmd
darkstar:~# cat libmd.info 
PRGNAM="libmd"
VERSION="1.1.0"
HOMEPAGE="https://www.hadrons.org/software/libmd/"
DOWNLOAD="https://archive.hadrons.org/software/libmd/libmd-1.1.0.tar.xz"
MD5SUM="b2a0650c78d92c7a9632a2a3cdd4f6a6"
DOWNLOAD_x86_64=""
MD5SUM_x86_64=""
REQUIRES=""
MAINTAINER="Matteo Bernardini"
EMAIL="ponce@slackbuilds.org"

darkstar:~# wget https://archive.hadrons.org/software/libmd/libmd-1.1.0.tar.xz
--2026-11-15 21:07:08--  https://archive.hadrons.org/software/libmd/libmd-1.1.0.tar.xz
Resolvendo archive.hadrons.org (archive.hadrons.org)... 84.121.133.206
Conectando-se a archive.hadrons.org (archive.hadrons.org)|84.121.133.206|:443... conectado.
A requisição HTTP foi enviada, aguardando resposta... 200 OK
Tamanho: 271228 (265K) [application/x-xz]
Salvando em: “libmd-1.1.0.tar.xz”

libmd-1.1.0.tar.xz                              100%[====================================================================================================>] 264,87K   288KB/s    em 0,9s    

2026-11-15 21:07:09 (288 KB/s) - “libmd-1.1.0.tar.xz” salvo [271228/271228]

darkstar:~# ./libmd.SlackBuild
libmd-1.1.0/
libmd-1.1.0/get-version
libmd-1.1.0/build-aux/
libmd-1.1.0/build-aux/missing
libmd-1.1.0/build-aux/compile
libmd-1.1.0/build-aux/test-driver
libmd-1.1.0/build-aux/depcomp
libmd-1.1.0/build-aux/ar-lib
libmd-1.1.0/build-aux/ltmain.sh
libmd-1.1.0/build-aux/config.guess
libmd-1.1.0/build-aux/config.sub
libmd-1.1.0/build-aux/install-sh
libmd-1.1.0/README
... some lines ...
... some lines ...
... some lines ...
usr/man/man3/rmd160.3.gz
usr/man/man3/sha1.3.gz
usr/man/man3/sha2.3.gz
usr/man/man7/
usr/man/man7/libmd.7.gz

Slackware package /tmp/libmd-1.1.0-x86_64-1_SBo.tgz created.

darkstar:~# installpkg /tmp/libmd-1.1.0-x86_64-1_SBo.tgz 
```


## 21.4 Managing Dependencies and Custom Build Options

### 21.4.1 Handling Dependency Chains

Slackware deliberately does not resolve dependencies automatically. When a SlackBuild lists packages in its `REQUIRES` metadata, you must compile and install those prerequisites **first**, starting from the deepest dependency up to the main application.

For example, if `foo` requires `libbar`, and `libbar` requires `dependency-baz`:

1. Download, build, and install `dependency-baz`.
2. Download, build, and install `libbar`.
3. Download, build, and install `foo`.

Building out of order will result in missing header or library errors during compilation.


### 21.4.2 Passing Environment Variables and Build Flags

Many SlackBuild scripts accept optional environment variables to customize build features (e.g., enabling GTK3, Python support, or specific audio drivers). These optional parameters are documented in the `README` file.

Pass variables directly on the command line prior to running the script:

```bash
darkstar:~/foo# ENABLE_GTK3=yes PYTHON3=yes ./foo.SlackBuild
```

#### Customizing Target Output and Tag Suffixes
By default, SBo packages are placed in `/tmp` with a build tag suffix of `_SBo`. You can customize these defaults using environment variables:

* **`OUTPUT`:** Sets an alternate output directory (e.g., `OUTPUT=/usr/packages`).
* **`TAG`:** Sets a custom build tag suffix (e.g., `TAG=_custom`).

```bash
darkstar:~/foo# OUTPUT=/usr/packages TAG=_custom ./foo.SlackBuild
```


## 21.5 Automated Build Helpers: `sbopkg`

While manual compilation offers complete transparency, managing multiple third-party packages and complex dependency chains manually can become labor-intensive.

`sbopkg` is the primary community-developed, terminal-based package helper for SlackBuilds.org. It automates synchronizing the SBo repository tree, downloading source tarballs, building queue files, and installing finished packages.


### 21.5.1 Installing and Synchronizing `sbopkg`

Install `sbopkg` using `installpkg`, then synchronize its local index with the remote SlackBuilds.org repository:

```bash
darkstar:~# wget https://github.com/sbopkg/sbopkg/releases/download/0.38.3/sbopkg-0.38.3-noarch-1_wsr.tgz
darkstar:~# installpkg sbopkg-0.38.3-noarch-1_ws.txz
darkstar:~# sbopkg -r
```

> Note: To check the latest version about sbopkg visit: https://www.sbopkg.org/index.php

Running `sbopkg -r` clones or updates the SBo tree into `/var/lib/sbopkg/SBo/15.0/`.


### 21.5.2 Essential `sbopkg` Commands

`sbopkg` can be run interactively via an `ncurses` menu or directly from the command line:

* **Search for a package (`-s`):** `sbopkg -s foo`
* **Inspect package info and README (`-i`):** `sbopkg -i foo`
* **Build and install a package (`-b`):** `sbopkg -b foo`
* **Process a dependency queue file (`-k`):** `sbopkg -k foo.sqf`

> **Note:** Even when using `sbopkg`, always review the `README` files for queued packages to check for required group/user additions or post-install steps.

```bash
darkstar:~#  sbopkg -b awstats

###########################################
       New queue process started on:
       dom 15 nov 2026 21:14:55 -03
###########################################

+++++++++++++++++++++++++++++++++++++++++++
PRE-CHECK LOG
Using the SBo repository for Slackware 15.0
Queue Process:  Download and build

awstats:
  Checking GPG for awstats.tar.gz ... OK
  Processing awstats 8.0-1
  Using original .info file
  Using original SlackBuild file
  No build options selected.

+++++++++++++++++++++++++++++++++++++++++++

Pre-check complete.

Do you wish to proceed based on the search results above? Packages not
found will be skipped during the process.

(P)roceed or (Q)uit?: P
```

The installation process is started. After some seconds, the result:

```text
Slackware package /tmp/sbopkg.3GT9ex/sbopkg-sbooutputdir/awstats-8.0-noarch-1_SBo.tgz created.

Done building package for awstats.
Built package: awstats-8.0-noarch-1_SBo.tgz

+++++++++++++++++++++++++++++++++++++++++++
SUMMARY LOG
Using the SBo repository for Slackware 15.0
Queue Process:  Download and build

awstats:
  MD5SUM check for awstats-8.0.tar.gz ... OK
  Building package awstats-8.0-noarch-1_SBo.tgz ... OK

+++++++++++++++++++++++++++++++++++++++++++

###########################################
          Queue process complete!
###########################################

```


## 21.6 Authoring and Submitting Custom SlackBuilds

For system administrators and package maintainers who wish to submit new scripts to SlackBuilds.org or maintain local custom software, SBo enforces strict packaging guidelines to maintain repository quality.

### 21.6.1 Submission Guidelines Checklist

Submissions to SlackBuilds.org must meet the following technical criteria:

1. **Pristine Upstream Archives:** Build scripts must fetch untouched upstream source tarballs (`.tar.gz`, `.tar.xz`, `.tgz`). Distributing repackaged or modified binaries is prohibited.
2. **Architecture Flexibility:** Scripts must support 32-bit (`i586`/`i686`) and 64-bit (`x86_64`) architectures using standard library suffix detection (`LIBDIRSUFFIX="64"`).
3. **Clean Staging (`PKG`):** Software must be staged inside `$PKG` (`/tmp/SBo/package-PRGNAM`) during `make install` and never directly onto the host root filesystem.
4. **Standard Documentation Path:** Documentation must be installed under `/usr/doc/$PRGNAM-$VERSION/`.
5. **Relative Symbolic Links:** Symlinks inside `$PKG` must be relative links, or generated dynamically in `install/doinst.sh` via `makepkg -l y -c n`.
6. **Valid Cryptographic Hashes:** Every source file listed in `.info` must include an accurate MD5 checksum.



By leveraging SlackBuilds.org and mastering custom build script techniques, Slackware system administrators can expand their software library while maintaining a clean, fully logged, and transparent operating system.

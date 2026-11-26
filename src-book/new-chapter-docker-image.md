# 23. Slackware in Docker

Containerization has revolutionized software development, deployment, and testing. While Slackware is traditionally known for bare-metal servers and workstations, running Slackware inside Docker containers provides a lightweight, reproducible, and isolated environment for testing configurations, running isolated services, and building software packages.

Official and community-maintained container images for Slackware are available via the community registry at `registry.slackware.nl`. These images support both `15.0` (stable) and `-current` (development) releases across `x86_64` and `i586` architectures.

> **Note:** The release tags and supported architectures described in this chapter reflect the repository status as of November 2026 (Slackware 15.0 and `-current`). As future stable versions—such as Slackware 16.0—are released, new image tags will be made available. Always consult `registry.slackware.nl` for the most up-to-date list of available tags.


## 23.1 Image Architecture: Base vs. Builder

Slackware container images are divided into two primary tiers:

1. **Base Images (`slackware:15.0`, `slackware:current`)**: A minimal, stripped-down Slackware installation containing essential system utilities and a configured `slackpkg` package manager. Base images are designed to keep container footprints small for production services and general use.

2. **Builder Images (`slackware-builder:15.0`, `slackware-builder:current`)**: A heavy-duty development environment equipped with the full Slackware toolchain—including `gcc`, `g++`, `make`, `cmake`, `meson`, `ninja`, `llvm`, `rust`, `go`, `python3-build`, and `kernel-headers`. These images allow developers to compile software and execute SlackBuild scripts immediately without downloading build tools at runtime.



## 23.2 Quick Start: Running Slackware Containers


1. Launching an Interactive Session

To pull and start an interactive bash session in a clean Slackware 15.0 container:

```bash
darkstar:~\$ docker run -it --rm registry.slackware.nl/slackware/slackware:15.0 /bin/bash
Unable to find image 'registry.slackware.nl/slackware/slackware:15.0' locally
15.0: Pulling from slackware/slackware
a1eb8b37a61f: Pull complete 
Digest: sha256:9a3eb2d386cb12af046e4384a4fe152138b1c29ffa8156a7666ba6fcb18618ab
Status: Downloaded newer image for registry.slackware.nl/slackware/slackware:15.0
bash-5.1# ps xau
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4284  3456 pts/0    Ss   01:16   0:00 /bin/bash
root           7  0.0  0.0   4228  2400 pts/0    R+   01:16   0:00 ps xau
```


2. Managing Packages inside a Container

Inside a running container, slackpkg can be used to update package lists and install software. To run slackpkg in non-interactive batch mode (essential for container scripts), pass -batch=on:

```text
bash-5.1# slackpkg update

Updating the package lists...
        Downloading...
                        Downloading https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5.asc...
2026-11-26 01:17:50 URL:https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5.asc [232/232] -> "/tmp/slackpkg.TtIqng/CHECKSUMS.md5.asc" [1]
Files //var/lib/slackpkg/CHECKSUMS.md5.asc and /tmp/slackpkg.TtIqng/CHECKSUMS.md5.asc differ

        Downloading...
                        Downloading https://slackware.nl/slackware/slackware64-15.0/ChangeLog.txt...
2026-11-26 01:17:53 URL:https://slackware.nl/slackware/slackware64-15.0/ChangeLog.txt [2454284/2454284] -> "/tmp/slackpkg.TtIqng/ChangeLog.txt" [1]
                List of all files
                        Downloading https://slackware.nl/slackware/slackware64-15.0/patches/MANIFEST.bz2...
2026-11-26 01:18:00 URL:https://slackware.nl/slackware/slackware64-15.0/patches/MANIFEST.bz2 [18874996/18874996] -> "/tmp/slackpkg.TtIqng/patches-MANIFEST.bz2" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/slackware64/MANIFEST.bz2...
2026-11-26 01:18:03 URL:https://slackware.nl/slackware/slackware64-15.0/slackware64/MANIFEST.bz2 [4199768/4199768] -> "/tmp/slackpkg.TtIqng/slackware64-MANIFEST.bz2" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/extra/MANIFEST.bz2...
2026-11-26 01:18:08 URL:https://slackware.nl/slackware/slackware64-15.0/extra/MANIFEST.bz2 [4524146/4524146] -> "/tmp/slackpkg.TtIqng/extra-MANIFEST.bz2" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/pasture/MANIFEST.bz2...
2026-11-26 01:18:10 URL:https://slackware.nl/slackware/slackware64-15.0/pasture/MANIFEST.bz2 [210060/210060] -> "/tmp/slackpkg.TtIqng/pasture-MANIFEST.bz2" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/testing/MANIFEST.bz2...
2026-11-26 01:19:55 URL:https://slackware.nl/slackware/slackware64-15.0/testing/MANIFEST.bz2 [5013528/5013528] -> "/tmp/slackpkg.TtIqng/testing-MANIFEST.bz2" [1]
                Checksums
                        Downloading https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5...
2026-11-26 01:19:59 URL:https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5 [1464132/1464132] -> "/tmp/slackpkg.TtIqng/CHECKSUMS.md5" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5.asc...
2026-11-26 01:20:00 URL:https://slackware.nl/slackware/slackware64-15.0/CHECKSUMS.md5.asc [232/232] -> "/tmp/slackpkg.TtIqng/CHECKSUMS.md5.asc" [1]
                Package List
                        Downloading https://slackware.nl/slackware/slackware64-15.0/FILELIST.TXT...
2026-11-26 01:20:03 URL:https://slackware.nl/slackware/slackware64-15.0/FILELIST.TXT [1915981/1915981] -> "/tmp/slackpkg.TtIqng/FILELIST.TXT" [1]
                Package descriptions
                        Downloading https://slackware.nl/slackware/slackware64-15.0/patches/PACKAGES.TXT...
2026-11-26 01:20:05 URL:https://slackware.nl/slackware/slackware64-15.0/patches/PACKAGES.TXT [131257/131257] -> "/tmp/slackpkg.TtIqng/patches-PACKAGES.TXT" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/slackware64/PACKAGES.TXT...
2026-11-26 01:20:09 URL:https://slackware.nl/slackware/slackware64-15.0/slackware64/PACKAGES.TXT [864745/864745] -> "/tmp/slackpkg.TtIqng/slackware64-PACKAGES.TXT" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/extra/PACKAGES.TXT...
2026-11-26 01:20:10 URL:https://slackware.nl/slackware/slackware64-15.0/extra/PACKAGES.TXT [40815/40815] -> "/tmp/slackpkg.TtIqng/extra-PACKAGES.TXT" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/pasture/PACKAGES.TXT...
2026-11-26 01:20:11 URL:https://slackware.nl/slackware/slackware64-15.0/pasture/PACKAGES.TXT [2163/2163] -> "/tmp/slackpkg.TtIqng/pasture-PACKAGES.TXT" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/testing/PACKAGES.TXT...
2026-11-26 01:20:13 URL:https://slackware.nl/slackware/slackware64-15.0/testing/PACKAGES.TXT [22923/22923] -> "/tmp/slackpkg.TtIqng/testing-PACKAGES.TXT" [1]
        Formatting lists to slackpkg style...
                Package List: using CHECKSUMS.md5 as source
                Package descriptions

```

Now, we are install httpd and mariadb

```text
bash-5.1# slackpkg install httpd mariadb

Looking for httpd mariadb in package list. Please wait... DONE

httpd-2.4.71-x86_64-1_slack15.0.txz
mariadb-10.5.29-x86_64-1_slack15.0.txz

Total package(s): 2

Do you wish to install selected packages (Y/n)? y

Package: httpd-2.4.71-x86_64-1_slack15.0.txz
                        Downloading https://slackware.nl/slackware/slackware64-15.0/./patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz...
2026-11-26 01:22:40 URL:https://slackware.nl/slackware/slackware64-15.0/patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz [4258688/4258688] -> "//var/cache/packages/./patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/./patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz.asc...
2026-11-26 01:22:40 URL:https://slackware.nl/slackware/slackware64-15.0/patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz.asc [232/232] -> "//var/cache/packages/./patches/packages/httpd-2.4.71-x86_64-1_slack15.0.txz.asc" [1]

Package: mariadb-10.5.29-x86_64-1_slack15.0.txz
                        Downloading https://slackware.nl/slackware/slackware64-15.0/./patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz...
2026-11-26 01:22:45 URL:https://slackware.nl/slackware/slackware64-15.0/patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz [30109476/30109476] -> "//var/cache/packages/./patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz" [1]
                        Downloading https://slackware.nl/slackware/slackware64-15.0/./patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz.asc...
2026-11-26 01:22:46 URL:https://slackware.nl/slackware/slackware64-15.0/patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz.asc [195/195] -> "//var/cache/packages/./patches/packages/mariadb-10.5.29-x86_64-1_slack15.0.txz.asc" [1]
        Package httpd-2.4.71-x86_64-1_slack15.0.txz is already in cache - not downloading
        Installing httpd-2.4.71-x86_64-1_slack15.0...
Verifying package httpd-2.4.71-x86_64-1_slack15.0.txz.
Installing package httpd-2.4.71-x86_64-1_slack15.0.txz:
PACKAGE DESCRIPTION:
# httpd (The Apache HTTP Server)
#
# Apache is an HTTP server designed as a plug-in replacement for the
# NCSA HTTP server. It fixes numerous bugs in the NCSA server and
# includes many frequently requested new features, and has an API which
# allows it to be extended to meet users' needs more easily.
#
# Apache is the most popular web server in the known universe; over
# half of the servers on the Internet are running Apache or one of
# its variants.
#
Executing install script for httpd-2.4.71-x86_64-1_slack15.0.txz.
Package httpd-2.4.71-x86_64-1_slack15.0.txz installed.
        Package mariadb-10.5.29-x86_64-1_slack15.0.txz is already in cache - not downloading
        Installing mariadb-10.5.29-x86_64-1_slack15.0...
Verifying package mariadb-10.5.29-x86_64-1_slack15.0.txz.
Installing package mariadb-10.5.29-x86_64-1_slack15.0.txz:
PACKAGE DESCRIPTION:
# mariadb (Drop-in replacement for the MySQL Database Server)
#
# MariaDB is a backward compatible, drop-in replacement branch of the
# MySQL(R) Database Server. It includes all major open source storage
# engines, including the Aria storage engine.
#
# Homepage: http://mariadb.org/
#
Executing install script for mariadb-10.5.29-x86_64-1_slack15.0.txz.
Package mariadb-10.5.29-x86_64-1_slack15.0.txz installed.

```


## 23.3 Building Packages with `slackware-builder`

Compiling software directly on a host machine can contaminate the host system with temporary header files or build dependencies. Using the `slackware-builder` image ensures clean, isolated build environments.

**Workflow: Executing a SlackBuild in Docker**

Suppose you have a local directory (`~/builds/htop`) containing `htop.SlackBuild`, `htop.info`, and the source tarball. You can mount your local directory into the container using a Docker volume (`-v`), execute the build, and output the compiled `.txz` package back to your host filesystem:

```bash
darkstar:~\$ docker run --rm \
  -v ~/builds/htop:/build \
  -w /build \
  registry.slackware.nl/slackware/slackware-builder:current \
  bash -c "sh htop.SlackBuild && cp /tmp/htop-*.txz /build/"
```

When the command completes:
1. The package is built inside the isolated container using the pre-installed compiler toolchain.
2. The finished `.txz` package is saved in your local `~/builds/htop` directory on the host.
3. The container self-destructs (`--rm`), leaving your host system untouched.



## 23.4 Automated Custom Builder Images (`build-builder-image.sh`)

For administrators maintaining custom build environments or private container registries, Eric Hameleers [Alien BOB](https://blog.slackware.nl/) created the `build-builder-image.sh` automation script.


**How Image Verification Works**

To prevent unnecessary rebuilds, the build script uses a smart base digest check:
1. It inspects the remote base image's unique SHA256 digest (`slackware.builder.base-digest`).
2. It checks if a local builder image already exists with a matching digest label.
3. If the base image has been updated on the registry, the script automatically triggers a rebuild of the builder image; otherwise, it skips the build process.

**Command-Line Usage**

The build script supports arguments for targeting specific releases and architectures:

```bash
# Build the builder image for Slackware 15.0 (x86_64)
darkstar:~# ./build-builder-image.sh --version current --arch x86_64

# Force a rebuild even if the base image digest has not changed
darkstar:~# ./build-builder-image.sh --version current --arch x86_64 --force
```

**Script Flags Reference**

| Flag | Description | Example |
| :--- | :--- | :--- |
| **`-v, --version <ver>`** | Specifies the target Slackware version (`15.0` or `current`). Default is `current`. | `./build-builder-image.sh -v 15.0` |
| **`-a, --arch <arch>`** | Specifies target architecture (`x86_64` or `i586`). Default is `x86_64`. | `./build-builder-image.sh -a x86_64` |
| **`-f, --force`** | Forces image creation even if the base image digest remains unchanged. | `./build-builder-image.sh --force` |


## 23.5 Best Practices for Slackware Dockerfiles

When writing custom `Dockerfile` scripts based on Slackware, follow these guidelines:

1. **Chain Commands in a Single `RUN` Block:** Combine package installation and cache cleanup in a single layer to minimize final image size.

```dockerfile
FROM registry.slackware.nl/slackware/slackware:current

RUN slackpkg -batch=on update && \
    slackpkg -batch=on install python3 libffi && \
    slackpkg -batch=on clean && \
    rm -rf /var/cache/slackpkg/* /tmp/*
```

2. **Set Non-Interactive Environment Variables:** Disable interactive prompts during script execution.
3. **Use Specific Image Tags:** Avoid using `:latest` in production Dockerfiles; pin your images to specific release tags like `:15.0`.
```


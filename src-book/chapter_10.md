# 10. Filesystem Permissions

## 10.1 Permissions Overview

As we have discussed, Slackware Linux is a multi-user operating system. Because of this, its filesystems are multi-user as well. This means that every file or directory has a set of permissions that grant or deny privileges to different users. There are three basic permissions (read, write, execute) and three permission sets for every file or directory.

Let's examine an example file using `ls -l`:


```bash
darkstar:~$ ls -l /bin/ls 
-rwxr-xr-x 1 root root 163384 Oct 24 20:46 /bin/ls
```
Recall from Chapter 4 that ls -l displays permissions along with the user and group that own the file. In this example:

- The leading - indicates a regular file.
- The permission string is rwxr-xr-x.
- The user owner is root and the group owner is also root.

While displayed together, the 9-character permission string is divided into three separate triplets:


| Set | Listing | Meaning |
| --- | --- | --- |
| Owner | rwx | The owner "root" may read, write, and execute |
| Group | r-x | The group "root" may read and execute |
| Others | r-x | Everyone else may read and execute |

Permissions behave slightly differently depending on whether they apply to a file or a directory:

- Read (`r`): On a file, allows reading its contents. On a directory, allows listing its contained files (e.g., using `ls`).
- Write (`w`): On a file, allows modifying or truncating its contents. On a directory, allows creating, deleting, or renaming files within it.
- Execute (`x`): On a file, allows running it as a program or script. On a directory, allows entering the directory (e.g., using `cd`) and accessing its subdirectories or file metadata.

Let's inspect the permissions on a user's home directory using `ls -ld`:

```bash
darkstar:~$ ls -ld /home/brusso
drwx--x--- 114 brusso users 4096 Oct 28 11:57 /home/brusso/
```

Here, the leading d indicates a directory. The directory is owned by the user `brusso` and the group `users`:

- Owner (`brusso`): Granted full access (`rwx`).
- Group (`users`): Granted read and execute permissions (`r-x`).
- Others: Prohibited from accessing, listing, or entering the directory (`---`).



## 10.2 chmod, chown, and chgrp

Now that we understand what permissions are and how they are structured, how do we change them? And how do we assign user and group ownership? This section covers the core command-line tools used to manage filesystem security and access rights.

The primary tool for modifying file ownership is `chown` (change owner). Traditionally used to change user ownership, `chown` can also modify group ownership simultaneously.

Let's look at an example:

```bash
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 brusso users 0 nov  2 18:51 a
-rw-r--r-- 1 brusso users 0 nov  2 18:51 b
darkstar:~# chown root /tmp/foo/a
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 root   users 0 nov  2 18:51 a
-rw-r--r-- 1 brusso users 0 nov  2 18:51 b
```

By separating a username and group name with a colon `(:)`, chown can change both user and group ownership in a single step:



```bash
darkstar:~# chown root:root /tmp/foo/b
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 root users 0 Nov  2 18:51 a
-rw-r--r-- 1 root root  0 Nov  2 18:51 b
```

If you specify a colon followed by a group name without a username, `chown` changes only the group ownership while leaving the user owner unchanged:

```bash
darkstar:~# chown :wheel /tmp/foo/a
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 root wheel 0 Nov  2 18:51 a
-rw-r--r-- 1 root root  0 Nov  2 18:51 b
```

To change the ownership of a directory and all of its contents (files and subdirectories) recursively, use the `-R` flag:

```bash
darkstar:~# chown -R root:root /tmp/foo
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 root root 0 nov  2 18:51 a
-rw-r--r-- 1 root root 0 nov  2 18:51 b
```

The `chgrp` (change group) utility is a dedicated tool used exclusively to change group ownership:

```bash
darkstar:~# chgrp wheel /tmp/foo/a
darkstar:~# ls -l /tmp/foo
total 0
-rw-r--r-- 1 root wheel 0 nov  2 18:51 a
-rw-r--r-- 1 root root  0 nov  2 18:51 b
```
While `chown` can already change group ownership, `chgrp` exists for POSIX compliance and compatibility with other UNIX variants whose legacy `chown` tools did not support group modifications.


**Changing Permissions (chmod)**

The command used to modify file and directory access permissions is `chmod` (change mode). Only the file's owner or the `root` superuser can change its permissions.

`chmod` supports two methods for defining permissions: Octal (Numeric) Mode and Symbolic (Alphabetic) Mode.


**1. Octal (Numeric) Mode**

In octal mode, permissions are represented by a 3-digit number. Each digit corresponds to one of the permission sets in order: **Owner**, **Group**, and **Other**s.

Each basic permission has a specific numeric value based on powers of 2:

| Permission | Octal Value | Bit Position |
|------------|-------------|--------------|
|Read (r) | 4 | 2^2 |
|Write (w) 2 | 2^1 |
|Execute (x) | 1 | 2^0 |

By adding these values together, you can specify any permission combination from `0` (no permissions) to `7` (full read, write, and execute permissions):

| Value | Permissions | String | Meaning |
| 0 | None | --- | No access |
| 1 | Execute only | --x | Execute |
| 2 | Write only | -w- | Write
| 3 | Write + Execute | -wx | Write & Execute (2 + 1) |
| 4 | Read only | r-- | Read |
| 5 | Read + Execute | r-x | Read & Execute (4 + 1) |
| 6 | Read + Write | rw- | Read & Write (4 + 2) |
| 7 | Read + Write + Execute | rwx | Read, Write & Execute (4 + 2 + 1) |



For example, to set permissions to `rwxr-x---` (User: `7`, Group: `5`, Others: `0`):

```bash
darkstar:~# ls -l /tmp/foo/a
-rw-r--r-- 1 root root 0 Nov  2 18:51 a
darkstar:~# chmod 750 /tmp/foo/a
darkstar:~# ls -l /tmp/foo/a
-rwxr-x--- 1 root root 0 Nov  2 18:51 a
```

**2. Symbolic (Alphabetic) Mode**

Symbolic mode uses letter codes combined with mathematical operators (`+`, `-`, `=`) to modify specific permission bits without affecting others.


*Target Categories (Who):*

- **u** — User (Owner)
- **g** — Group
- **o** — Others (World)
- **a** — All (u, g, and o)


*Operators:*

- **+** — Add permissions
- **-** — Remove permissions
- **=** — Set exact permissions (overwriting existing ones)

*Permission Types:*

- **r** — Read
- **w** — Write
- **x** — Execute

Multiple symbolic actions can be combined by separating them with commas:

```bash
darkstar:/tmp/foo# ls -l
total 0
-rw-r--r-- 1 brusso users 0 Nov  2 18:51 a
-rw-r--r-- 1 brusso users 0 Nov  2 18:51 b
-rw-r--r-- 1 brusso users 0 Nov  2 18:51 c
-rw-r--r-- 1 brusso users 0 Nov  2 18:51 d

darkstar:/tmp/foo# chmod u+x a
darkstar:/tmp/foo# chmod g+w b
darkstar:/tmp/foo# chmod u+x,g+x,o-r c
darkstar:/tmp/foo# chmod u=rwx,g=rx,o= d

darkstar:/tmp/foo# ls -l
-rwxr--r-- 1 brusso users 0 Nov  2 18:51 a*
-rw-rw-r-- 1 brusso users 0 Nov  2 18:51 b
-rwxr-x--- 1 brusso users 0 Nov  2 18:51 c*
-rwxr-x--- 1 brusso users 0 Nov  2 18:51 d*
```

Both Octal and Symbolic modes are widely used. Octal mode is ideal when setting absolute permissions across all three sets at once, while Symbolic mode is perfect for selectively adding or removing a specific privilege.


## 10.3 SUID, SGID, and the "Sticky" Bit

We're not quite done with permissions just yet. There are three other "special" permissions in addition to those mentioned above: **SUID**, **SGID**, and the **sticky bit**. When a file or directory has one or more of these permissions set, it behaves in special ways. The SUID and SGID permissions change the way an application is executed, while the sticky bit restricts file deletion. These permissions are applied with `chmod` just like standard read, write, and execute permissions, but with a twist.

> **When Are Special Permissions Used?**
> 
> Before diving into how these special bits are configured, it helps to understand the practical scenarios where each permission is necessary:
> 
> * **SUID (Set User ID):** Used when a regular user needs to run an executable that requires temporary elevated privileges (usually `root`) to perform a system task. A classic example is changing one's password using `/usr/bin/passwd`, which must modify system files like `/etc/shadow` that are strictly owned by `root`.
> * **SGID (Set Group ID):** Used on binary executables to run a process with the group owner's permissions, or set on shared directories so that any newly created file automatically inherits the parent directory's group ownership instead of the creator's default group.
> * **Sticky Bit:** Set on shared directories where all users have full write access (such as `/tmp`). It restricts file deletion so that users can only remove or rename their own files, preventing them from accidentally or maliciously deleting files owned by others.

**SUID and SGID in Action**

SUID and SGID stand for "Set User ID" and "Set Group ID", respectively. When an application with one of these bits is set, the process executes with the privileges of the file's owner or group owner, regardless of which user actually launched the program.

Let's look at a common SUID application, `/usr/bin/passwd`, and the system files it interacts with:

```bash
darkstar:~# ls -l /etc/passwd /etc/shadow /usr/bin/passwd
-rw-r--r-- 1 root root     2573 out 21 20:46 /etc/passwd
-rw-r----- 1 root shadow   1408 out 21 20:46 /etc/shadow
-rws--x--x 1 root root   136960 set  2 05:17 /usr/bin/passwd
```

Notice the permissions on `/usr/bin/passwd`. Instead of an <kbd>x</kbd> in the user's execute slot, there is an <kbd>s</kbd>. This indicates that `passwd` is a SUID executable: when executed by a standard user, the process runs with `root` privileges. This elevated privilege is required because neither `/etc/passwd` nor `/etc/shadow` is writable by unprivileged users.


The sticky bit restricts the ability to delete or rename files and is applied to directories. In a directory with the sticky bit set, non-root users can only delete or rename files that they personally own.

Let's inspect a common system directory that utilizes the sticky bit:

```bash
darkstar:~# ls -ld /tmp 
drwxrwxrwt 1458 root root 1269760 nov  2 19:17 /tmp
```
As a shared directory for temporary file storage, `/tmp` must be readable, writable, and executable by all users. Setting the sticky bit—indicated by the <kbd>t</kbd> in the world execution slot—prevents users from deleting each other's temporary files.


Special Permissions Syntax Reference

| Permission Type | Octal Value | Letter Symbol | Affected Slot | Primary Function | 
| SUID | 4 | s | User (u) | Executes process as file owner | 
| SGID | 2 | s | Group (g) | Executes process as group owner / inherits directory group | 
| Sticky Bit | 1 | t | Others (o) | Restricts file deletion to file owner| 


**Octal Mode (4 Digits)**

When applying special permissions with octal numbers, pass a leading fourth digit to `chmod`:

```bash
darkstar:~# chmod 4711 /usr/bin/passwd
darkstar:~# chmod 1777 /tmp
```

> Note: Whenever the leading fourth octet is omitted, `chmod` defaults its value to 0.


**Symbolic Mode**

You can also assign special bits using symbolic notation (s and t):

```bash
darkstar:~# chmod u+s,go+x /usr/bin/passwd
darkstar:~# chmod ug+rwx,o+rwt /tmp
```

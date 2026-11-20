# 9. Users and Groups

## 9.1 What Are Users and Groups?

Slackware Linux inherits a robust multi-user architecture from its UNIX design principles. In a multi-user environment, multiple users can operate the system simultaneously, each isolated by distinct security permissions. This boundary prevents unauthorized access to or modification of other users' files and enables system administrators to define precise access controls across the entire system.

Furthermore, user accounts in Slackware are not limited to human operators. The operating system includes numerous pre-defined system users and groups (such as `daemon`, `nobody`, `bin`, and `ssdm`). Rather than facilitating interactive logins, these specialized accounts serve to segment system daemons, restrict service privileges, and enforce the principle of least privilege—a topic explored in detail in the next chapter on filesystem permissions.


>**Note on Local vs. Centralized Authentication:**
> While Slackware Linux can be configured to integrate with centralized authentication directories (such as LDAP, NIS, or Kerberos), the commands and examples in this chapter focus exclusively on local user administration, where account information is stored directly in `/etc/passwd`, `/etc/shadow`, and `/etc/group`.


## 9.2 Managing Users and Groups

Slackware provides both interactive helper scripts for quick administration and powerful low-level command-line utilities for automation and batch operations.

### 9.2.1 Interactive Account Creation (`adduser`)

The simplest and most user-friendly way to create a new user account in Slackware is using the interactive `adduser` shell script. `adduser` guides you through each configuration step—setting up the username, UID, initial group, supplementary groups, home directory, login shell, and initial password.


```text
darkstar:~# adduser 

Login name for new user []: alan

User ID ('UID') [ defaults to next available ]: 

Initial group [ users ]: 
Additional UNIX groups:

Users can belong to additional UNIX groups on the system.
root@maria:/home/brusso# adduser 

Login name for new user []: alan

User ID ('UID') [ defaults to next available ]: 

Initial group [ users ]: users
Additional UNIX groups:

Users can belong to additional UNIX groups on the system.
root@maria:/home/brusso# adduser 

Login name for new user []: alan

User ID ('UID') [ defaults to next available ]: 

Initial group [ users ]: users
Additional UNIX groups:

Users can belong to additional UNIX groups on the system.
For local users using graphical desktop login managers such
as XDM/KDM, users may need to be members of additional groups
to access the full functionality of removable media devices.

* Security implications *
Please be aware that by adding users to additional groups may
potentially give access to the removable media of other users.

If you are creating a new user for remote shell access only,
users do not need to belong to any additional groups as standard,
so you may press ENTER at the next prompt.

Press ENTER to continue without adding any additional groups
Or press the UP arrow key to add/select/edit additional groups
:  cdrom floppy plugdev

Home directory [ /home/alan ] 

Press the UP and DOWN arrow keys to cycle through the available shells
Shell [ /bin/bash ] 

Expiry date (YYYY-MM-DD) []: 

New account will be created as follows:

---------------------------------------
Login name.......:  alan
UID..............:  [ Next available ]
Initial group....:  users
Additional groups:  cdrom,floppy,plugdev
Home directory...:  /home/alan
Shell............:  /bin/bash
Expiry date......:  [ Never ]

This is it... if you want to bail out, hit Control-C.  Otherwise, press
ENTER to go ahead and make the account.


Creating new account...


Changing finger information for alan.
Name []: Alan Hicks
Office []: SlackwareBook
Work phone []:
Home phone []:


Finger information has been changed.
New password:
Retype new password:
passwd: password updated successfully

Account setup complete.

```

### 9.2.2 Supplementary Groups for Desktop Functionality

Group membership in Slackware controls access to hardware devices and system services. Every user has a primary group (by default, `users`), but accounts can belong to multiple secondary groups to inherit additional system permissions:

- audio: Grants access to sound cards and audio hardware.
- video: Grants access to GPU acceleration and display devices.
- cdrom / floppy / plugdev: Enables mounting and managing removable storage devices (USB drives, optical discs) without requiring root privileges.

During the `adduser` prompt, pressing the Up Arrow key automatically inserts Slackware's recommended default groups for interactive desktop users.


### 9.2.3 Non-Interactive User Creation (useradd)

While `adduser` is ideal for interactive use, `useradd` is the low-level utility used for non-interactive account creation, shell scripting, and batch operations. In fact, `adduser` itself is a wrapper script built on top of useradd.

Unlike `adduser`, `useradd` requires explicit command-line flags to set non-default attributes:

```text
darkstar:~# useradd -d /home/alan -s /bin/bash -g users -G cdrom,floppy,plugdev alan

```

In this example:
* -d /home/alan: Sets a custom path for the home directory.
* -s /bin/bash: Assigns /bin/bash as the default login shell.
* -g users: Sets the primary group to users.
* -G audio,cdrom,...: Specifies a comma-separated list of secondary groups.


>Note: useradd creates the user account but does not set a password. You must run passwd username immediately afterward to enable password authentication for the new account.



### 9.2.4 Managing Groups (groupadd)

Creating new security groups is handled by `groupadd`. Like `useradd`, it operates non-interactively:

```text
darkstar:~# groupadd slackers
```

This creates a new system group named `slackers` and automatically assigns it the next available GID (Group ID) in `/etc/group`.


### 9.2.5 Deleting Accounts and Groups (userdel and groupdel)

Removing accounts and groups is straightforward using `userdel` and `groupdel`:

```text
darkstar:~# userdel -r alan
darkstar:~# groupdel slackers
```

* `userdel alan`: Removes the user account entry from /etc/passwd and /etc/shadow, but leaves the user's home directory (/home/alan) intact on disk.
* `userdel -r alan`: Removes both the user account and recursively deletes their home directory and mail spool.
* `groupdel slackers`: Removes the specified group entry from /etc/group.



## 9.3 Other User and Group Tools

In addition to account creation and deletion tools, Slackware includes several command-line utilities for modifying existing user attributes, managing passwords, and updating user environment settings.


### 9.3.1 Managing Passwords and Account Locks (`passwd`)

The most fundamental credential utility is `passwd`. Regular users can execute `passwd` without arguments to update their own login password. The system administrator (`root`) can change the password for any user by specifying the target username:

```bash
darkstar:~# passwd alan
```

**Locking and Unlocking Accounts**

The root user can temporarily disable logins for a specific account using the -l (lock) flag:

```text
darkstar:~# passwd -l alan
```

This operation locks the account by prepending an exclamation mark (!) to the encrypted password string in `/etc/shadow`, preventing password-based authentication without deleting user files or home directories. To restore access, execute `passwd` with the `-u` (unlock) flag:

```text
darkstar:~# passwd -u alan
```


### 9.3.2 Modifying Existing User Accounts (usermod)

The `usermod` utility modifies existing user account settings in `/etc/passwd` and `/etc/shadow`. It is the primary command for altering group memberships, home directory locations, and default login shells.



**Appending vs. Overwriting Secondary Groups (-a -G)**

When managing secondary group memberships with `usermod`, understanding the distinction between appending and overwriting groups is critical:


> Correct: Appends "lp" to existing secondary groups

```text
darkstar:~# usermod -a -G lp alan 
```

> CAUTION: Overwrites ALL secondary groups with ONLY "lp"

```text
darkstar:~# usermod -G lp alan
```

* `usermod -a -G lp alan`: The `-a` (append) option ensures that `alan` is added to the `lp` group while preserving all current secondary group memberships (such as `audio`, `video`, `plugdev`).
* `usermod -G lp alan`: Omitting the `-a` flag replaces all of `alan's` secondary group memberships with only `lp`, revoking access to all previously assigned groups.

**Common usermod Operations:**
* `-d /new/home -m`: Updates the home directory path and moves existing files to the new location.
* `-s /bin/zsh`: Changes the user's default login shell.
* `-l newname`: Renames the user account login name.
* `-e YYYY-MM-DD`: Sets an explicit expiration date for the account.




### 9.3.3 Changing Default Shells (chsh)

The `chsh` (change shell) utility allows users to modify their default login shell without needing administrative intervention:

```text
darkstar:~\$ chsh -s /bin/zsh
```

Regular users can only select valid system shells listed in `/etc/shells`. The `root` user can change any user's shell by passing the target username to `chsh`.


### 9.3.4 Updating User Information (chfn)

The `chfn` (change finger) utility updates user identity information stored in the GECOS field of `/etc/passwd` (such as full name, office room, and phone numbers):

```text
darkstar:~\$ chfn
```

This metadata can be queried locally or retrieved over networks using utilities like finger.


## 9.4 Managing Users and Groups Manually

Like most configuration aspects in Slackware Linux, user and group definitions are stored as plain-text files on the local filesystem. While higher-level tools like `adduser` and `usermod` automate account management, you can create, modify, or inspect user accounts directly by editing these configuration files and manually setting up home directories.



### 9.4.1 Structure of `/etc/passwd`

The primary account registry is `/etc/passwd`. This file contains one line per user account, with seven distinct fields separated by colons (`:`):

```text
darkstar:~\$ cat /etc/passwd | grep alan
alan:x:1002:100:Alan Hicks,Slackware Book:/home/alan:/bin/zsh
```


From left to right, the fields represent:
1. **Username (alan)**: The unique login name for the account.
2. **Password Placeholder (x)**: Historical password field. The literal `x` indicates that the encrypted password string is safely stored in `/etc/shadow`.
3. **User ID / UID (1000)**: The numerical identifier assigned to the user by the kernel.
4. **Group ID / GID (100)**: The numerical identifier of the user's primary group (by default, GID `100` corresponds to `users`).
5. **GECOS / Comment Field (Alan Hicks,,,)**: Optional metadata, such as full name, office location, and contact numbers (managed via `chfn`).
6. **Home Directory (/home/alan)**: The absolute path to the user's initial working directory upon login.
7. **Default Shell (/bin/bash)**: The path to the command interpreter executed when the user logs in.


### 9.4.2 Shadow Password Security (/etc/shadow)

Because `/etc/passwd` must remain world-readable (so system programs can map UIDs to usernames), storing password hashes inside it presents a severe security risk. Slackware uses shadow password protection, moving encrypted hashes to `/etc/shadow`, which is readable only by root (permissions `0600`).

A typical entry in `/etc/shadow` looks like this:

```text
darkstar:~\# cat /etc/shadow | grep alan
alan:$6$h2sjEdiuwzO.R13H$cZfZjZO9imd4uqfJKal/2cdbLZu9e0EgDWoR96QuKdUTQ.dY7FJhy0:20775:0:99999:7:::
```

The fields in /etc/shadow specify:

1. **Username**: Matches the corresponding account in /etc/passwd.
2. **Encrypted Password**: The cryptographic password hash (typically SHA-512 in modern Slackware). An ! or * in this field locks the account.
3. **Last Change Date**: The date the password was last modified, expressed as the number of days elapsed since the Unix Epoch (January 1, 1970).
4. **Minimum Password Age**: Minimum number of days required before the password can be changed again.
5. **Maximum Password Age**: Maximum number of days the password remains valid before forcing a password change.
6. **Warning Period**: Number of days prior to password expiration that the user is warned to change credentials.
7. **Inactivity Period**: Days after password expiration during which the account remains accessible before being automatically disabled.
8. **Account Expiration Date**: Absolute date (in days since Epoch) when the account expires.
9. **Reserved Field**: Reserved for future use.



### 9.4.3 Group Definitions (/etc/group)

Group relationships are maintained in `/etc/group`. Each line defines a system group using four colon-separated fields:

```text
darkstar:~\# cat /etc/group | grep alan
floppy:x:11:alan
cdrom:x:19:alan
plugdev:x:83:alan
```

- **Group Name (wheel)**: The unique string identifier for the group.
- **Group Password Placeholder (x)**: Placeholder for optional group passwords (stored in `/etc/gshadow`).
- **Group ID / GID (10)**: The unique numerical GID.
- **Member List (root,alan)**: A comma-separated list of secondary users assigned to this group.


### 9.4.4 Safe Manual Editing with vipw and vigr

Directly opening `/etc/passwd` or `/etc/shadow` with a standard text editor like `vi` or `nano` is dangerous, as concurrent writes can corrupt the system database.

Slackware provides dedicated locking utilities for manual editing:

- **vipw**: Safely opens `/etc/passwd` with mandatory file locking.
- **vipw -s**: Safely opens `/etc/shadow` with file locking.
- **vigr**: Safely opens `/etc/group` with file locking.
- **vigr -s**: Safely opens `/etc/gshadow` with file locking.

These tools respect your `EDITOR` or `VISUAL` environment variables and prevent race conditions by locking the files during editing.



### 9.4.5 Complete Manual Account Setup Workflow

Creating a user manually requires more than adding text entries to configuration files. To fully set up a functional user account manually, follow these steps:

1. **Lock and Edit Account Files**: Run `vipw` to add the user entry to `/etc/passwd`, then run `vipw -s` to initialize the shadow entry.
2. **Assign Group Memberships**: Run `vigr` to add the username to appropriate secondary groups in `/etc/group`.
3. **Create the Home Directory**: Create the user's home directory and populate it with default profile templates from `/etc/skel/`:

```text
darkstar:~# mkdir -p /home/alan
darkstar:~# cp -r /etc/skel/.[a-z]* /home/alan/
```

* **Set Correct Ownership and Permissions**: Assign ownership of the home directory and its contents to the new user and primary group:

```text
darkstar:~# chown -R alan:users /home/alan
darkstar:~# chmod 701 /home/alan
```

* **Set Initial Password**: Initialize the account password using the `passwd` utility:

```text
darkstar:~# passwd alan
```

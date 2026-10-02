# 9. Users and Groups

## 9.1 What Are Users and Groups?

Slackware Linux inherits a strong multi-user tradition from its UNIX inspiration. This means that multiple people may use the system at once, but it also means that each of these people may have different permissions. This allows users to prevent others from modifying their files, or lets system administrators explicitly define what users can and cannot do on the system. Moreover, users need not be actual people at all. In fact, Slackware includes several dozen pre-defined user and group accounts that are not typically used by regular users. Rather these accounts allow the system administrator to segment the system for security reasons. We'll see how that's done in the next chapter on filesystem permissions.

## 9.2 Managing Users and Groups

The easiest way to add new users in Slackware is through the use of our very fine `adduser` shell script. `adduser` will prompt you to enter the details of the new user you wish to creature and step you through the process quickly and easily. It will even create a password for the new user.

```text

darkstar:~# adduser Login name for new user []: david User ID ('UID') [ defaults to next available ]: Initial group [ users ]: Additional UNIX groups: Users can belong to additional UNIX groups on the system. For local users using graphical desktop login managers such as XDM/KDM, users may need to be members of additional groups to access the full functionality of removable media devices. * Security implications * Please be aware that by adding users to additional groups may potentially give access to the removable media of other users. If you are creating a new user for remote shell access only, users do not need to belong to any additional groups as standard, so you may press ENTER at the next prompt. Press ENTER to continue without adding any additional groups Or press the UP arrow to add/select/edit additional groups : audio cdrom floppy plugdev video Home directory [ /home/david ] Shell [ /bin/bash ] Expiry date (YYYY-MM-DD) []: New account will be created as follows: --------------------------------------- Login name.......: david UID..............: [ Next available ] Initial group....: users Additional groups: audio,cdrom,floppy,plugdev,video Home directory...: /home/david Shell............: /bin/bash Expiry date......: [ Never ] This is it... if you want to bail out, hit Control-C. Otherwise, press ENTER to go ahead and make the account. Creating new account... Changing the user information for david Enter the new value, or press ENTER for the default Full Name []: Room Number []: Work Phone []: Home Phone []: Other []: Changing password for david Enter the new password (minimum of 5, maximum of 127 characters) Please use a combination of upper and lower case letters and numbers. New password: Re-enter new password: Password changed. Account setup complete.

```

The addition of optional groups needs a little explaining. Every user in Slackware has a single group that it is always a member of. By default, this is the "users" group. However, users can belong to more than one group at a time and will inherit all the permissions of every group they belong to. Typical desktop users will need to add several group memberships in order to do things like play sound or access removeable media like cdroms or USB flash drives. You can simply press the up arrow key at this section and a list of default groups for desktop users will magically appear. You can of course, add to or remove groups from this listing.

Now that we've demonstrated how to use the interactive `adduser` program, lets look at some powerful non-interactive tools that you may wish to use. The first is `useradd` (8). `useradd` is a little less friendly, but much faster for creating users in batches. This makes it ideal for use in shell scripts. In fact, `adduser` is just such a shell script and uses `useradd` for most of the heavy lifting. `useradd` has many options and we can't explain them all here, so refer to its man page for the complete details. Now, let's make a new user.

```text

darkstar:~# useradd -d /data/home/alan -s /bin/bash -g users -G audio,cdrom,floppy,plugdev,video alan

```

Here I have added the user "alan". I specified the user's home directory as `/data/home/alan` and used `bash` as my shell. Also, I specified my default group as "users" and added myself to a number of useful groups for dekstop use. You'll note that `useradd` does not do any prompting like `adduser` . Unless you want to accept the defaults for everything, you'll need to tell `useradd` what to do.

Now that we know how to add users, we should learn how to add groups. As you might have guessed, the command for doing this is `groupadd` (8). `groupadd` works in the same way as `useradd` , but with far fewer options. The following command adds the group "slackers" to the system.

```text

darkstar:~# groupadd slackers

```

Deleting users and groups is easy as well. Simply run the `userdel` (8) and `groupdel` (8) commands. By default, `userdel` will leave the user's home directory on the system. You can remove this with the `-r` argument.

## 9.3 Other User and Group Tools

Several other tools exist for managing users and groups. Perhaps the most important one is `passwd` (1). This command changes a user account's password. Normal users may change their own passwords only, but root can change anyone's password. Also, root can lock a user account with the `-l` argument. This doesn't actually shutout the account, but instead changes the user's encrypted password to a value that can't be matched.

The easiest way for modifying a user's information is the `usermod` (8) utility which is capable of modifying everything from group membership to home directories. A full listing of its features won't be given here, so check the man page. `usermod` is perhaps the best tool to use for modifying a user's group members. The `-s` and `-G` arguments accomplish this.

```text

darkstar:~# usermod -a -G wheel alan darkstar:~# usermod -G wheel alan

```

It important to note the differences in the two commands above. The first command adds the user "alan" to the "wheel" group without modifying any other groups "alan" belongs to. The second command also makes "alan" a member of the "wheel" group, but also removes the user's membership from any other groups, something you will very rarely want to do!

Another useful tool is `chsh` (1) which changes a user's default shell. Like `passwd` , normal users can only change their own shell, but the root user can change anyone's.

The last tool we're going to discuss is `chfn` (1). This is used to enter identifying information on the user such as his phone number and real name. This information is stored in the `passwd` (5) file and retrieved using `finger` (1).

## 9.4 Managing Users and Groups Manually

Like most things in Slackware Linux, users and groups are stored in plain-text files. This means that you can edit all the details of a user, or even create a new user or group simply by editing these files and doing a few other tasks like creating the user's home directory. Of course, after you see how this is done you'll appreciate just how simple the included tools make this task.

Our first stop is the `/etc/passwd` file. Here, all the information about a user is stored, except for (oddly enough) the user's password. The reason for this is rather simple. `/etc/passwd` must be readable by all users on the system, so you wouldn't want passwords stored there, even if they are encrypted. Let's take a quick look at my entry in this file.

```text

alan:x:1000:100:,,,:/home/alan:/bin/bash

```

Each line in this file contains a number of fields seperated by a colon. They are, from left to right: username, password, UID, GUID, a comment field, home directory, and shell. You'll notice that the password field for every entry is an <kbd>x</kbd> . That is because Slackware uses shadow passwords, so the actual encrypted password is stored in `/etc/shadow` . Let's take a look there.

```text

alan:$1$HlR?M3fkL@oeJmsdLfhsLFM*4dflPh8:14197:0:99999:7:::

```

The `shadow` file contains more than just the encrypted password as you'll notice. The fields here, again from left to right, are: username, encrypted password, last day the password was changed, days before the password may be changed again, how many days before the password expires, days that the account will be disabled after expiring, when the account was disabled, and a reserved field. You may notice on some accounts that the various "days" fields often include very large numbers. The reason for this is that Slackware counts time from the "Epoch" which is January 1, 1970 for historical reasons.

To create a new user account, you'll just need to open these files using `vipw` (8). This will open `/etc/passwd` in the editor defined by your VISUAL variable or your EDITOR variable if VISUAL isn't defined. If neither is present, it will fall back to `vi` by default. If you pass the `-s` argument, it will open `/etc/shadow` instead. It's important to use `vipw` instead of using any other editor, because `vipw` will lock the file and prevent other programs from editing it right underneath your feet.

That isn't all you'll need to do however; you must also create the user's home directory and change the user's password using `passwd` .

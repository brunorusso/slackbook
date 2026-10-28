# 5. The Bourne Again Shell

## 5.1 What Is A Shell?

What exactly is a shell? At its core, a shell is a command-line user environment. In essence, it is an application that starts when a user logs in, providing a framework to execute commands and launch programs—much like a graphical user interface (GUI) does.

Slackware includes several shells in a full installation. However, this book focuses primarily on `bash` (the Bourne Again Shell). Advanced users might consider using the powerful `zsh`, while those familiar with older UNIX systems may appreciate `ksh`. The truly masochistic might choose `csh`, but new users should stick to the most popular option: `bash`.

> **In other words:** The shell acts as an interactive bridge between the user and the Linux kernel.

An important point to remember is that a shell is not merely a command interpreter. With a shell, it is also possible to automate tasks by writing executable scripts (called **shell scripts**), customize your command-line environment, and much more.



## 5.2 Environment Variables

All shells make system administration easier by keeping track of settings using **environment variables**. An environment variable acts like a global configuration key—a simple name used to store information that the shell and other programs can reference at any time.

For example, the `PS1` variable tells `bash` how to format your command prompt, while `LS_OPTIONS` enables color output for `ls`. Other variables control application behavior directly, such as `LESSOPEN`, which tells `less` to run the `lesspipe.sh` preprocessor.

Setting your own environment variables is straightforward. `bash` includes built-in commands for managing them:

* **`set`** / **`export`**: Defines a new variable or promotes it so sub-shells can access it.
* **`unset`**: Removes a variable from the environment.

To access or read the value stored inside a variable, simply place a dollar sign (`$`) in front of its name (e.g., `$PS1` or `$PATH`). 

> **Tip:** Don't panic if you accidentally `unset` an important variable! You can easily restore all default environment variables by logging out of your terminal session and logging back.


Let's practice by creating a variable and displaying its contents:

```bash
darkstar:~$ set FOO=bar 
darkstar:~$ echo $FOO bar
```

The primary difference between setting a local variable and using `export` is that `export` makes the variable available to any sub-shells (a sub-shell is simply a child process running inside the parent shell). You can easily see this behavior when modifying the `PS1` variable, which controls the bash prompt:


```bash
darkstar:~$ set PS1='FOO ' 
darkstar:~$ export PS1='FOO ' FOO
```

While bash uses many environment variables, one of the most important you will encounter is `PATH`. The `PATH` variable contains a colon-separated list of directories that the shell searches through whenever you enter a command.

For example, the `top` binary is located at `/usr/bin/top`. You could execute it by typing its full absolute path (`/usr/bin/top`), but if `/usr/bin` is listed in your `PATH`, bash locates and runs it automatically.

You will most likely notice this mechanism when attempting to run system administration tools as a normal user. For instance, commands like `ifconfig` reside in `/sbin`, which is usually omitted from a regular user's `PATH`:


```bash
darkstar:~$ ifconfig 
bash: ifconfig: command not found 
darkstar:~$ echo $PATH 
/usr/local/bin:/usr/bin:/bin:/usr/games:/usr/libexec/kf6:/usr/libexec/kf5:/usr/lib64/qt6/bin:/usr/lib64/qt5/bin
```

Above, you see a typical PATH for a mortal user. You can change it on your own the same as any other environment variable. If you login as root however, you'll see that root has a different PATH.

As shown above, this is a typical `PATH` for a normal user. You can modify your `PATH` just like any other environment variable. However, if you switch to the `root` user, you will notice that `root` has a different `PATH` that includes system binary directories like `/sbin` and `/usr/sbin`

```bash
darkstar:~$ su - 
Password: 
darkstar:~# echo $PATH 
/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/games:/usr/libexec/kf6:/usr/libexec/kf5:/usr/lib64/qt6/bin:/usr/lib64/qt5/bin
```

## 5.3 Tab Completion

Still think there's too much work involved in typing out long filenames or wildcards? There is an even faster feature for daily productivity: **tab completion**.

Tab completion enables you to type just enough of a filename, directory, or command to uniquely identify it, and then press the <kbd>TAB</kbd> key—`bash` will automatically fill in the rest for you. 

If the text you typed isn't enough to uniquely identify a single match, `bash` will complete as much as it can [1]. Pressing the <kbd>TAB</kbd> key a second time will display a list of all possible matches:

```bash
darkstar:~\$ cd /usr/loc<TAB>
darkstar:~\$ cd /usr/local/

darkstar:~\$ cd /usr/l<TAB><TAB>
lib/  lib64/  libexec/  local/
```


--## 5.4 Wildcards

Wildcards are special characters that tell the shell to match certain criteria. If you have experience with DOS, you'll recognize * as a wildcard that matches anything. `bash` makes use of this wildcard and several others to enable you to easily define exactly what you want to do.

This first and most common of these is, of course, *. The asterisk matches any character or combination of characters, including none. Thus `b*` would match any files named b, ba, bab, babc, bcdb, and so forth. Slightly less common is the ?. This wildcard matches one instance of any character, so `b?` would match ba and bb, but not b or bab.

```text

darkstar:~$ touch b ba bab 
darkstar:~$ ls * 
b ba bab 
darkstar:~$ ls b? 
ba

```

No, the fun doesn't stop there! In addition to these two we also have the bracket pair "[ ]" which allows us to fine tune exactly what we want to match. Whenever `bash` see the bracket pair, it substitutes the contents of the bracket. Any combination of letters or numbers may be specified in the bracket as long as they are comma seperated. Additionally, ranges of numbers and letters may be specified as well. This is probably best shown by example.

```text

darkstar:~$ ls a[1-4,9] 
a1 a2 a3 a4 a9

```

Since Linux is case-sensitive, capital and lower-case letters are treated differently. All capital letters come before all lower-case letters in "alphabetical" order, so when using ranges of capital and lower-case letters, make sure to get them right.

```text

darkstar:~$ ls 1[W-b] 
1W 1X 1Y 1Z 1a 1b 
darkstar:~$ ls 1[w-B] 
/bin/ls: cannot access 1[b-W]: No such file or directory

```

In the second example, 1[b-W] isn't a valid range, so the shell treats it as a filename, and since that file doesn't exist, `ls` tells you so.


--## 5.5 Input and Output Redirection

One of the defining features of Linux and other UNIX-like operating systems is the number of small, relatively simple applications and the ability to stack them together to create complex systems. This is achieved by redirecting the output of one program to another, or by drawing input from a file or second program.

To get started, we're going to show you how to redirect the output of a program to a file. This is easily done with the '>' character. When `bash` sees the '>' character, it redirects all of the standard output (also known as stdout) to whatever file name follows.

```text

darkstar:~$ echo foo 
foo 
darkstar:~$ echo foo > /tmp/bar 
darkstar:~$ cat /tmp/bar 
foo

```

In this example, we show you what `echo` would do if its stdout was not redirected to a file, then we re-direct it to the `/tmp/bar` file. If `/tmp/bar` does not exist, it is created and the output from `echo` is placed within it. If `/tmp/bar` did exist, then its contents are over-written. This might not be the best idea if you want to keep those contents in place. Thankfully, `bash` supports '>>' which will append the output to the file.

```text

darkstar:~$ echo foo 
foo 
darkstar:~$ echo foo > /tmp/bar 
darkstar:~$ cat /tmp/bar 
foo 
darkstar:~$ echo foo2 >> /tmp/bar 
darkstar:~$ cat /tmp/bar 
foo 
foo2

```

You can also re-direct the standard error (or stderr) to a file. This is slightly different in that you must use '2>' instead of just '>'. (Since `bash` can re-direct input, stdout, and stderr, each must be uniquely identifiable. 0 is input, 1 is stdout, and 2 is stderr. Unless one of these is specified, `bash` will make its best guess as to what you actually meant, and assumed anytime you use '>' you only want to redirect stdout. 1> would have worked just as well.)

```text

darkstar:~$ rm bar 
rm: cannot remove `bar': No such file or directory 
darkstar:~$ rm bar 2> /tmp/foo 
darkstar:~$ cat /tmp/foo 
rm: cannot remove `bar': No such file or directory

```

You may also redirect the standard input (known as stdin) with the '<' character, though it's not used very often.

```text

darkstar:~$ fromdos < dosfile

```

Finally, you can actually redirect the output of one program as input to another. This is perhaps the most useful feature of `bash` and other shells, and is accomplished using the '|' character. (This character is referred to as 'pipe'. If you here some one talk of piping one program to another, this is exactly what they mean.)

```text

darkstar:~$ ps auxw | grep getty
root      2632  0.0  0.0   1656   532 tty2     Ss+  Feb21   0:00 /sbin/agetty 38400 tty2 linux
root      3199  0.0  0.0   1656   528 tty3     Ss+  Feb15   0:00 /sbin/agetty 38400 tty3 linux
root      3200  0.0  0.0   1656   532 tty4     Ss+  Feb15   0:00 /sbin/agetty 38400 tty4 linux
root      3201  0.0  0.0   1656   532 tty5     Ss+  Feb15   0:00 /sbin/agetty 38400 tty5 linux
root      3202  0.0  0.0   1660   536 tty6     Ss+  Feb15   0:00 /sbin/agetty 38400 tty6 linux

```

--## 5.6 Task Management

`bash` has yet another cool feature to offer, the ability to suspend and resume tasks. This allows you to temporarily halt a running process, perform some other task, then resume it or optionally make it run in the background. Upon pressing <kbd>CTRL-Z</kbd> , `bash` will suspend the running process and return you to a prompt. You can return to that process later. Additionally, you can suspend multiple processes in this way indefinitely. The `jobs` built-in command will display a list of suspended tasks.

```text

darkstar:~$ jobs 
[1]- Stopped vi TODO 
[2]+ Stopped vi chapter_05.xml

```

In order to return to a suspended task, run the `fg` built-in to bring the the most recently suspended task back into the foreground. If you have mutiple suspended tasks, you can specify a number as well to bring one of them to the foreground.

```text

darkstar:~$ fg # "vi TODO" 
darkstar:~$ fg 1 # "vi chapter_05.xml"

```

You can also background a task with (surprize) `bg` . This will allow the process to continue running without maintaining control of your shell. You can bring it back to the foreground with `fg` in the same way as suspended tasks.


## 5.7 Terminals

Slackware Linux and other UNIX-like operating systems allow users to interact with them in many ways, but the most common—and arguably the most useful—is the terminal. In the past, terminals were physical keyboards and monitors connected to a mainframe or server via serial cables. Today, however, most terminals are virtual; they exist purely in software, eliminating the need for expensive dedicated hardware.

The most basic virtual terminals in Slackware are managed by `agetty`. By default, Slackware runs six virtual console instances (`tty1` through `tty6`), allowing local users to log in and run commands simultaneously. You can switch between these text-based consoles using the <kbd>Alt</kbd>+<kbd>F1</kbd> through <kbd>F6</kbd> key combinations (or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F1</kbd>–<kbd>F6</kbd> if you are currently inside a graphical session). This multi-console capability is particularly useful on headless servers or for running separate tasks under different user accounts.

On desktop and laptop workstations where a graphical interface (`X`) is running, users typically rely on graphical terminal emulators. Slackware includes several options, such as KDE's `konsole`, XFCE's `Terminal`, and the classic `xterm`. These can usually be launched from your desktop environment's menu (often listed under a "System" or "Utilities" submenu). Opening any of these applications creates a new terminal window that automatically starts your default shell (`bash`).



--## 5.8 Customization

By now you should be pretty familiar with `bash` and you may have even noticed some odd behavior. For example, when you login at the console, you're presented with a prompt that looks a bit like this.

```text

alan@darkstar:~$

```

However, sometimes you'll see a much less helpful prompt like this one.

```text

bash-3.1$

```

The cause here is a special environment variable that controls the `bash` prompt. Some shells are considered "login" shells and others are "interactive" shells, and both types read different configuration files when started. Login shells read `/etc/profile` and `~/.bash_profile` when executed. Interactive shells read `~/.bashrc` instead. This has some advantages for power users, but is a common annoyance for many new users who want the same environment anytime they execute `bash` and don't care about the difference between login and interactive shells. If this applies to you, simply edit your own ~/.bashrc file and include the following lines. (For more information on the different configuration files used, read the INVOCATION section of the `bash` man page.)

```text

#~/.bashrc 
. /etc/profile 
. ~/.bash_profile

```

When using the above, all your login and interactive shells will have the same environment settings and behave identically. Now, anytime we wish to customize a shell setting, we only have to edit `~/.bash_profile` for user-specific changes and `/etc/profile` for global settings. Let's start by configuring the prompt.

`bash` prompts come in all shapes, colors, and sizes, and every user has their own preferances. Personally, I prefer short and simple prompts that take up a minimum of space, but I've seen and used mutli-line prompts many times. One personal friend of mine even included ASCII-art in his bash prompt. To change your prompt you need only to change your PS1 variable. By default, Slackware attempts to configure your PS1 variable thusly:

```text

darkstar:~$ echo $PS1 
\u@\h:\w\$

```

Yes, this tiny piece of funny-looking figures controls your `bash` prompt. Basicaly, every character in the PS1 variable is included in the prompt, unless it is a escaped by a <kbd>\</kbd> , which tells `bash` to interpret it. There are many different escape sequences and we can't discuss them all, but I'll explain these. The first "\u" translates to the username of the current user. "\h" is the hostname of the machine the terminal is attached to. "\w" is the current working directory, and "\$" displays either a <kbd>#</kbd> or a <kbd>$</kbd> sign, depending on whether or not the current user is root. A complete listing of all prompt escape sequences is listed in the `bash` man page under the PROMPTING section.

Since we've gone through all this trouble to discuss the default prompt, I thought I'd take some time to show you a couple example prompts and the PS1 variable values needed to use them.

```text

Wed Jan 14 12:08 AM 
alan@raven:~$ echo $PS1 
\d \@\n\u@\h:\w$ 
HOST: raven - JOBS: 0 - TTY: 3 
alan@~/Desktop/sb_3.0:$ echo $PS1 
HOST: \H - JOBS: \j - TTY: \l\n\u@\w:\$

```

For even more information on configuring your bash prompt, including information on setting up colored prompts, refer to `/usr/doc/Linux-HOWTOs/Bash-Prompt-HOWTO` . After reading that for a short while, you'll get an idea of just how powerful your `bash` prompts can be. I once even had a prompt that gave me up to date weather information such as temperature and barometric pressure!


## 5.9 Another words about Shell

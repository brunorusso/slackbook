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


## 5.4 Wildcards

Wildcards are special characters that allow you to match files and directories based on patterns. If you have experience with DOS/CMD, you will recognize `*` as a wildcard that matches anything. `bash` makes extensive use of wildcards to simplify file management.

The first and most common wildcard is the asterisk (`*`). It matches any sequence of characters, including an empty string. For example, `b*` matches any filename starting with the letter "b" (such as `b`, `ba`, `bab`, or `bcdb`).

Slightly less common is the question mark (`?`). It matches exactly one instance of any single character. Thus, `b?` matches `ba` and `bb`, but will not match `b` or `bab`.


```bash
darkstar:~$ touch b ba bab 
darkstar:~$ ls * 
b ba bab 
darkstar:~$ ls b? 
ba
```

The fun doesn't stop there! bash also supports square brackets ([ ]), which allow you to specify exact sets or ranges of characters to match at a single position. Unlike shell brace expansion, characters inside brackets are not separated by commas.

You can list individual characters inside the brackets (e.g., [ab]) or specify ranges of letters and numbers using a hyphen (e.g., [a-z] or [0-9]):


```bash
darkstar:~$ touch a1 a2 a3 a4 a5 a6 a7 a8 a9 10
darkstar:~$ ls a[1-4,9] 
a1 a2 a3 a4 a9
```

Because Linux and ASCII collation are case-sensitive, uppercase and lowercase letters are treated as distinct characters. In standard ASCII ordering, all uppercase letters (A–Z) come before lowercase letters (a–z). Therefore, when specifying ranges that span both uppercase and lowercase letters, you must list the character with the lower ASCII value first.

For example, `[W-b]` is a valid range (matching W, X, Y, Z, a, and b), whereas `[w-B]` is invalid because w comes after B in ASCII order:


```bash
darkstar:~$ ls 1[W-b] 
1W 1X 1Y 1Z 1a 1b 
darkstar:~$ ls 1[w-B] 
/bin/ls: cannot access 1[b-W]: No such file or directory
```

In the second example, because `[w-B]` is an invalid range (since w has a higher ASCII value than B), bash fails to expand the wildcard pattern and treats `1[w-B]` as a literal filename. Since no file with that exact name exists, ls returns an error.



## 5.5 Input and Output Redirection

One of the defining features of Linux and UNIX-like operating systems is the availability of many small, specialized applications and the ability to chain them together to build complex systems. This modularity is achieved by redirecting the output of one program to a file or another program, or by drawing input from an external file or stream.

By default, every command in `bash` interacts with three standard data channels known as **file descriptors**:
* **`0` (stdin)** — Standard Input (keyboard input by default)
* **`1` (stdout)** — Standard Output (terminal display by default)
* **`2` (stderr)** — Standard Error (error messages displayed on screen)


**Redirecting Standard Output (`>` and `>>`)**

```bash
darkstar:~$ echo foo 
foo 
darkstar:~$ echo foo > /tmp/bar 
darkstar:~$ cat /tmp/bar 
foo
```

If you want to preserve existing content and append new lines to the end of the file instead, use the `>>` operator:


```bash
darkstar:~$ echo foo2 >> /tmp/bar 
darkstar:~$ cat /tmp/bar 
foo 
foo2
```

**Redirecting Standard Error (2>)**

Error messages are sent to standard error (stderr) rather than standard output (stdout). To redirect error messages to a file, specify file descriptor `2` before the redirection symbol (`2>`):


```bash
darkstar:~$ rm bar 
rm: cannot remove 'bar': No such file or directory 

darkstar:~$ rm bar 2> /tmp/err.log 
darkstar:~$ cat /tmp/err.log 
rm: cannot remove 'bar': No such file or directory
```

> Note: Since stdout is descriptor 1, 1> is functionally identical to >. You can also redirect both stdout and stderr into the same file using &> (or 2>&1).


**Redirecting Standard Input (<)**

You can instruct a program to read its input directly from a file instead of waiting for keyboard input using the `<` operator:

```bash
darkstar:~$ fromdos < dosfile.txt
```

**Pipelines (|)**

Perhaps the most powerful feature of `bash` is the pipe operator (`|`). A pipeline connects the standard output of one command directly into the standard input of another, enabling you to combine utilities seamlessly:


```bash
darkstar:~$ ps auxw | grep getty
root      1500  0.0  0.0   5616  3288 tty1     Ss+  out27   0:00 /sbin/agetty --noclear 38400 tty1 linux
root      1501  0.0  0.0   5616  3308 tty2     Ss+  out27   0:00 /sbin/agetty 38400 tty2 linux
root      1502  0.0  0.0   5616  3308 tty3     Ss+  out27   0:00 /sbin/agetty 38400 tty3 linux
root      1503  0.0  0.0   5616  3380 tty4     Ss+  out27   0:00 /sbin/agetty 38400 tty4 linux
root      1504  0.0  0.0   5616  3312 tty5     Ss+  out27   0:00 /sbin/agetty 38400 tty5 linux
root      1505  0.0  0.0   5616  3464 tty6     Ss+  out27   0:00 /sbin/agetty 38400 tty6 linux
```

In this example, `ps aux` lists all running processes on the system, and the pipe passes that text output directly to `grep getty`, which filters and displays only the lines matching "getty".


## 5.6 Task Management

`bash` provides robust task management features, allowing you to suspend, resume, and manage multiple running programs from a single terminal session. This enables you to temporarily pause a process, return to the shell prompt to perform other work, and resume the paused task later—either in the foreground or in the background.


Suspending Tasks (<kbd>Ctrl</kbd>+<kbd>Z</kbd> and `jobs`)

Pressing <kbd>Ctrl</kbd>+<kbd>Z</kbd> sends a signal to the active process, pausing it and returning you to the shell prompt. You can suspend multiple applications indefinitely.

To view all currently suspended or backgrounded tasks, use the `jobs` built-in command:


```bash
darkstar:~$ jobs 
[1]- Stopped vi TODO 
[2]+ Stopped vi chapter_05.xml
```

In the output above:
- The number in brackets (`[1]`, `[2]`) represents the Job ID.
- The plus sign (`+`) indicates the current (most recently suspended) job.
- The minus sign (`-`) indicates the previous job.


**Foregrounding Tasks (fg)**

To resume a suspended process in the foreground, use the `fg` command. Running `fg` without any arguments resumes the current job (marked with +). To bring a specific job back, pass its Job ID (e.g., `fg 1` or `fg %1`):

```bash
darkstar:~$ fg 
# Resumes job [2] ("vi chapter_05.xml")

darkstar:~$ fg 1 
# Resumes job [1] ("vi TODO")

```

**Backgrounding Tasks (`bg` and `&`)**

If you want a suspended command to continue executing in the background without taking over your terminal prompt (useful for long-running scripts, downloads, or compilations), use the `bg` command:

```bash
darkstar:~\$ bg 1
[1]+ vi TODO &
```

> Tip: You can also launch a command directly in the background from the start by appending an ampersand (`&`) to the end of the command line (e.g., `command &`).



## 5.7 Terminals

Slackware Linux and other UNIX-like operating systems allow users to interact with them in many ways, but the most common—and arguably the most useful—is the terminal. In the past, terminals were physical keyboards and monitors connected to a mainframe or server via serial cables. Today, however, most terminals are virtual; they exist purely in software, eliminating the need for expensive dedicated hardware.

The most basic virtual terminals in Slackware are managed by `agetty`. By default, Slackware runs six virtual console instances (`tty1` through `tty6`), allowing local users to log in and run commands simultaneously. You can switch between these text-based consoles using the <kbd>Alt</kbd>+<kbd>F1</kbd> through <kbd>F6</kbd> key combinations (or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F1</kbd>–<kbd>F6</kbd> if you are currently inside a graphical session). This multi-console capability is particularly useful on headless servers or for running separate tasks under different user accounts.

On desktop and laptop workstations where a graphical interface (`X`) is running, users typically rely on graphical terminal emulators. Slackware includes several options, such as KDE's `konsole`, XFCE's `Terminal`, and the classic `xterm`. These can usually be launched from your desktop environment's menu (often listed under a "System" or "Utilities" submenu). Opening any of these applications creates a new terminal window that automatically starts your default shell (`bash`).



## 5.8 Customization


By now, you should be fairly familiar with `bash`, and you may have even noticed some seemingly odd behavior. For example, when you log in at a text console, you are presented with a prompt that looks like this:

```bash
brusso@darkstar:~$
```

However, inside certain terminal windows, you might see a much less informative prompt:

```bash
bash-3.1$
```

This variation occurs because different types of shell sessions read different configuration files upon startup:

- **Login Shells**: Executed when you log into the system (e.g., at the console prompt or via SSH). A login shell reads `/etc/profile` first for global settings, followed by the user's `~/.bash_profile`.
- **Interactive Non-Login Shells**: Launched when you open a terminal window inside a graphical desktop environment. An interactive shell reads `~/.bashrc` instead.



This distinction allows power users to fine-tune environment behavior, but it can confuse new users who want a consistent environment everywhere. To unify your settings, you can edit your `~/.bashrc` file to automatically source your login profile:


```bash
#~/.bashrc 
. /etc/profile 
. ~/.bash_profile
```

With this configuration in place, both login and interactive shells will share identical settings. From then on, you only need to edit `~/.bash_profile` for personal shell customizations and `/etc/profile` for system-wide changes.



**Configuring the Prompt (PS1)**

The appearance of your `bash` prompt is controlled by the `PS1` environment variable. By default, Slackware defines `PS1` as follows:

```bash
darkstar:~$ echo $PS1 
\u@\h:\w\$
```

Every literal character in `PS1` is displayed as-is, while characters preceded by a backslash (`\`) are interpreted as special escape sequences:

- **\u** — The current username
- **\h** — The hostname up to the first dot
- **\H** — The full hostname
- **\w** — The current working directory (with $HOME abbreviated as ~)
- **\$** — Displays # if the current user is root, or $ for a standard user
- **\d** — The current date (e.g., "Wed Jan 14")
- **\@** — The current time in 12-hour AM/PM format
- **\n** — Inserts a newline
- **\j** — The number of background jobs currently managed by the shell
- **\l** — The basename of the shell's terminal device (e.g., 1 for tty1 or pts/0)

Here are two examples of custom multi-line prompts and the `PS1` values used to create them:


```bash
brusso@darkstar:~$ echo $PS1 
\u@\h:\w\$
```

For comprehensive guidance on creating advanced prompt layouts—including adding ANSI color codes—refer to the documentation in `/usr/doc/Linux-HOWTOs/Bash-Prompt-HOWTO`.

## 5.9 Another words about Shell

The shell is far more than a simple command-line interface—it is an indispensable Swiss Army knife for system administration. Throughout this chapter, we have seen how features like environment variables, wildcards, I/O redirection, pipelines, and job control transform routine terminal operations into powerful, streamlined workflows.

Beyond executing standalone commands, the shell enables you to automate complex tasks, build customized system maintenance scripts, and manage your Slackware environment with total control. Mastering `bash` is one of the most rewarding investments you can make in your Linux journey. We strongly encourage you to keep exploring, writing your own shell scripts, and discovering new ways to elevate your productivity.


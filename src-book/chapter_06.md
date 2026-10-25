# 6. Process Control and Scheduling

Slackware systems often run hundreds or thousands of programs, each of which is referred to as a process. Managing these processes is an important part of system administration. So how exactly do we handle all of these separate processes?

## 6.1 ps

The first step in managing processes is figuring out what processes are currently running. The most popular and powerful tool for this is `ps` (1). Without any arguments, `ps` won't tell you much information. By default, it only tells you what processes are running in your currently active shell. If we want more information, we'll need to look deeper.

```text

darkstar:~$ ps 
  PID TTY           TIME CMD 
12220 pts/4     00:00:00 bash 
12236 pts/4     00:00:00 ps

```

Here you can see what processes you are running in your currently active shell or terminal and only some information is included. The PID is the "Process ID"; every process is assigned a unique number. The TTY tells you what terminal device the process is attached to. Naturally, CMD is the command that was run. You might be a little confused by TIME though, since it seems to move so slowly. This isn't the amount of real time the process has been running, but rather the amount of CPU time the process has consumed. An idle process uses virtually no CPU time, so this value may not increase quickly.

Viewing only our own processes isn't very much fun, so let's take a look at all the processes on the system with the `-e` argument.

```text

darkstar:~$ ps -e 
PID TTY         TIME     CMD 
  1 ?           00:00:00 init 
  2 ?           00:00:00 kthreadd 
  3 ?           00:00:00 migration/0 
  4 ?           00:00:00 ksoftirqd/0 
  7 ?           00:00:11 events/0 
  9 ?           00:00:01 work_on_cpu/0 
 11 ?           00:00:00 khelper 
102 ?           00:00:02 kblockd/0 
105 ?           00:01:19 kacpid 
106 ?           00:00:01 kacpi_notify 
... many more lines omitted ...

```

**Note**

The above example uses the standard `ps` syntax, but much more information can be discovered if we use BSD syntax. In order to do so, we must use the `aux` argument.

This is distinct from the `-aux` argument, but in most cases the two arguments are equivilant. This is a decades-old relic. For more information, see the man page for `ps` .

```text

darkstar:~$ ps aux 
USER    PID     %CPU    %MEM    VSZ     RSS TTY STAT START TIME COMMAND 
root      1     0.0     0.0     3928    632 ?   Ss   Apr05 0:00 init [3] 
root      2     0.0     0.0     0       0 ?     S    Apr05 0:00 [kthreadd] 
root      3     0.0     0.0     0       0 ?     S    Apr05 0:00 [migration/0] 
root      4     0.0     0.0     0       0 ?     S    Apr05 0:00 [ksoftirqd/0] 
root      7     0.0     0.0     0       0 ?     S    Apr05 0:11 [events/0] 
root      9     0.0     0.0     0       0 ?     S    Apr05 0:01 [work_on_cpu/0] 
root     11     0.0     0.0     0       0 ?     S    Apr05 0:00 [khelper] 
... many more lines omitted ....

```

As you can see, BSD syntax offers much more information, including what user controls the process and what percentage of RAM and CPU the process is consuming when `ps` is run.

To accomplish bits of this, on a per process basis, `ps` allows one or more process IDs (PIDs) to be provided in the command line, and has the '-o' flag to show a particular attribute of the PID.

```text

darkstar:~$ ps -o cmd -o etime $$ 
CMD         ELAPSED 
/bin/bash   12:22

```

What this is displaying, is the PID's command name (cmd), and its elapsed time (etime). The PID in this example, is a shell variable for the PID of the current shell. So you can see, in this example, the shell process has existed for 12 minutes, 22 seconds.

Using the `pgrep` (1) command, this can get more automatable.

```text

darkstar:~$ ps -o cmd -o rss -o vsz $(pgrep httpd) 
CMD                          RSS   VSZ 
/usr/sbin/httpd -k restart 33456 84816 
/usr/sbin/httpd -k restart 33460 84716 
/usr/sbin/httpd -k restart 33588 84472 
/usr/sbin/httpd -k restart 30424 81608 
/usr/sbin/httpd -k restart 33104 84900 
/usr/sbin/httpd -k restart 33268 85112 
/usr/sbin/httpd -k restart 30640 82724 
/usr/sbin/httpd -k restart 15168 67396 
/usr/sbin/httpd -k restart 33180 84416 
/usr/sbin/httpd -k restart 33396 84592 
/usr/sbin/httpd -k restart 32804 84232

```

In this example, a subshell execution, using `pgrep` , is returning the PIDs of any process, whose command name includes 'httpd'. Then `ps` displaying the command name, resident memory size, and virtual memory size.

Finally, `ps` can also create a process tree. This shows you which processes have children processes. Ending the parent of a child process also ends the child. We do this with the `-ejH` argument.

```text

darkstar:~$ ps -ejH 
... many lines omitted ... 
 3660  3660 3660 tty1 00:00:00 bash 
29947 29947 3660 tty1 00:00:00  startx 
29963 29947 3660 tty1 00:00:00   xinit 
29964 29964 29964 tty7 00:27:11   X 
29972 29972 3660 tty1 00:00:00    sh 
29977 29972 3660 tty1 00:00:05     xscreensaver 
29988 29972 3660 tty1 00:00:04     xfce4-session 
29997 29972 3660 tty1 00:00:16      xfwm4 
29999 29972 3660 tty1 00:00:02      Thunar 
... many more lines omitted ...

```

As you can see, `ps` (1) is an incredibly powerful tool for determining not only what processes are currently active on your system, but also for learning lots of important information about them.

As is the case with many of the applications, there is often several tools for the job. Similar to the `ps -ejH` output, but more terse, is `pstree` (1). It displays the process tree, a bit more visually.

```text

darkstar:~$ pstree 
<<<<<<< Updated upstream
init-+-atd 
|-crond 
|-dbus-daemon 
|-httpd---10*[httpd] 
|-inetd 
|-klogd 
|-mysqld_safe---mysqld---8*[{mysqld}] 
|-screen-+-4*[bash] 
|        |-bash---pstree 
|        |-2*[bash---ssh] 
|        `-bash---irssi 
|-2*[sendmail] 
|-ssh-agent 
|-sshd---sshd---sshd---bash---screen 
`-syslogd

=======
init─┬─ModemManager───3*[{ModemManager}]
     ├─NetworkManager─┬─dhcpcd─┬─dhcpcd───2*[dhcpcd]
     │                │        └─dhcpcd
     │                └─3*[{NetworkManager}]
     ├─acpid
     ├─4*[agetty]
     ├─akonadi_contact───2*[{akonadi_contact}]
     ├─akonadi_control─┬─akonadi_archive───4*[{akonadi_archive}]
     │                 ├─akonadi_contact───2*[{akonadi_contact}]
     │                 ├─akonadi_followu───3*[{akonadi_followu}]
     │                 ├─akonadi_indexin───2*[{akonadi_indexin}]
     │                 ├─akonadi_maildir───2*[{akonadi_maildir}]
     │                 ├─akonadi_maildis───3*[{akonadi_maildis}]
     │                 ├─akonadi_mailfil───4*[{akonadi_mailfil}]
     │                 ├─akonadi_mailmer───3*[{akonadi_mailmer}]
     │                 ├─akonadi_migrati───3*[{akonadi_migrati}]
     │                 ├─akonadi_newmail───3*[{akonadi_newmail}]
     │                 ├─akonadi_sendlat───3*[{akonadi_sendlat}]
     │                 ├─akonadi_unified───3*[{akonadi_unified}]
     │                 ├─akonadiserver─┬─mysqld───14*[{mysqld}]
     │                 │               └─26*[{akonadiserver}]
     │                 └─2*[{akonadi_control}]
... many more lines omitted ...
>>>>>>> Stashed changes
```

## 6.2 kill and killall

Managing processes isn't only about knowing which ones are running, but also about communicating with them to change their behavior. The most common way of managing a program is to terminate it. Thus, the tool for the job is named `kill`. Despite the name, `kill` doesn't actually terminate processes, but sends signals to them. The most common signal is SIGTERM, which tells the process to finish up what it is doing and terminate. There are a variety of other signals that can be sent, but the three most common are SIGTERM, SIGHUP, and SIGKILL.

What a process does when it receives a signal varies. Most programs will terminate (or attempt to terminate) whenever they receive any signal, but there are a few important differences. For starters, the SIGTERM signal informs the process that it should terminate itself at its earliest convenience. This gives the process time to finish up any important activities, such as writing information to disk, before it closes. In contrast, the SIGKILL signal tells the process to terminate itself immediately, no questions asked. This is most useful for killing processes that are not responding and is sometimes called the "silver bullet". Some processes (particularly daemons) capture the SIGHUP signal and reload their configuration files whenever they receive it.

In order to signal a process, we first need to know it's PID. You can get this easily with `ps` as we discused. In order to send different signals to a running process, you simply pass the signal name or number and `-s` as an argument. The `-l` argument lists all the signals you can choose and their number. You can also send signals by their name with `-s` .

```text
darkstar:~$ kill -l 
 1) SIGHUP   2) SIGINT   3) SIGQUIT  4) SIGILL 
 5) SIGTRAP  6) SIGABRT  7) SIGBUS   8) SIGFPE 
 9) SIGKILL 10) SIGUSR1 11) SIGSEGV 12) SIGUSR2 
13) SIGPIPE 14) SIGALRM 15) SIGTERM 16) SIGSTKFLT 
... many more lines omitted ... 
darkstar:~$ kill 1234 # SIGTERM 
darkstar:~$ kill -s 9 1234 # SIGKILL 
darkstar:~$ kill -s 1 1234 # SIGHUP 
darkstar:~$ kill -s HUP 1234 # SIGHUP
```

Sometimes you may wish to terminate all running processes with a certain name. You can kill processes by name using `killall`. Just pass the same arguments to `killall` that you would pass to kill:

```text
darkstar:~$ killall bash # SIGTERM 
darkstar:~$ killall -s 9 bash # SIGKILL 
darkstar:~$ killall -s 1 bash # SIGHUP 
darkstar:~$ killall -s HUP bash # SIGHUP
```

## 6.3 top


So far, we've learned how to look at active processes for a single moment in time, but what if we want to monitor them continuously over an extended period? `top` allows us to do just that. It displays an ordered, real-time list of active processes on your system along with vital resource consumption metrics, updating periodically (every three seconds by default).

![image](img/top.png)

The man page has helpful details on how to interact with `top`, such as changing its delay interval, altering the order in which processes are displayed, and even terminating processes right from within `top` itself.


## 6.4 htop

<<<<<<< Updated upstream

## 6.5 cron
=======
The `htop` like top allow you to look active processes in real-time and allows you to scroll vertically and horizontally, and interact using a pointing device (mouse).  You can observe all processes running on the system, along with their command line arguments, as well as view them in a tree format, select multiple processes and act on them all at once.

At the top of the screen, `htop` features visual meters displaying real-time CPU, memory, and swap utilization. At the bottom, a footer bar displays available actions mapped to Function keys (<kbd>F1</kbd> through <kbd>F10</kbd>). This allows you to search, filter, send signals (killing), or adjust process priorities (renicing) directly without needing to enter PIDs manually.

![image](img/htop.png)


The man page has helpful details on how to interact with `htop`.


## 6.5 btop

Another popular resource monitor is `btop`, which displays real-time statistics and resource usage for the processor, memory, storage disks, network interfaces, and running processes. In other words, `btop` serves as a comprehensive, feature-rich TUI (Text User Interface) dashboard for system performance.

If you prefer an intuitive, visually responsive interface to monitor your system, `btop` is an excellent choice. It features full mouse support, allowing you to click on elements, scroll through lists, and select individual PIDs to view detailed process trees or filter resource usage effortlessly.

![image](img/btop.png)

The man page has helpful details on how to interact with `btop`.


## 6.6 cron
>>>>>>> Stashed changes

So far, we've learned many different ways of viewing active processes on our system and methods for signaling them, but what if we want to run a process periodically on an automated schedule? Fortunately, Slackware includes just the tool for the job: `crond`. `cron` runs processes for every user on a schedule specified by that user. This makes it extremely useful for tasks that need to run periodically without requiring a dedicated daemon, such as automated backup scripts. Every user gets their own entry in the `cron` database, allowing non-root users to schedule their own background tasks as well.

In order to manage scheduled tasks, you will need to use the `crontab` utility. The man page lists a variety of options, but the most common method is using the `-e` argument. This locks the user's entry in the `cron` database (preventing concurrent modifications) and opens it in the text editor specified by the `VISUAL` or `EDITOR` environment variable. On Slackware systems, this defaults to the `vi` editor. You may wish to review the chapter on `vi` before proceeding.

The `cron` database entries may seem a bit archaic at first glance, but they are remarkably flexible. Each uncommented line is processed by `crond`, and the specified command is executed whenever all time conditions match.

```text
darkstar:~$ crontab -e 
#Keep current with slackware 
30 02 * * * /usr/local/bin/rsync-slackware64.sh 1>/dev/null 2>&1

```

As mentioned before, the syntax for `cron` entries can be a little difficult to understand at first, so let's break down each part individually. From left to right, the five time fields are: **Minute**, **Hour**, **Day of Month**, **Month**, and **Day of Week**, followed by the **Command** to execute.

An asterisk (`*`) acts as a wildcard, matching every possible value for that field (e.g., every minute, every hour, or every day).

In the previous example (`30 02 * * * /usr/local/bin/rsync-slackware64.sh 1>/dev/null 2>&1`):
* **Minute (`30`)**: At minute 30
* **Hour (`02`)**: At 2:00 AM
* **Day of Month (`*`)**: Every day of the month
* **Month (`*`)**: Every month
* **Day of Week (`*`)**: Every day of the week

Therefore, the command `/usr/local/bin/rsync-slackware64.sh 1>/dev/null 2>&1` runs **every day at 2:30 a.m.**


`crond` will also email the local user with any standard output or error generated by a executed command. For this reason, many tasks have their output redirected to `/dev/null`, a special character device file that immediately discards any data written to it.

To make it easier to remember the syntax rules and output redirection, you can paste the following commented template at the top of your own `crontab` file:

```text
# MIN HOUR DAY MONTH WEEKDAY COMMAND
# Redirect output to /dev/null: 1>/dev/null 2>&1
```

By default, Slackware includes a number of pre-configured entries and comments in `root`'s `crontab`. These entries make it easier to set up periodic system maintenance by utilizing dedicated directories in `/etc` corresponding to execution frequencies. Any executable script placed within these directories will automatically run on that schedule.

The directory names are self-explanatory:
* `/etc/cron.hourly` — Executed once every hour
* `/etc/cron.daily` — Executed once every day
* `/etc/cron.weekly` — Executed once every week
* `/etc/cron.monthly` — Executed once every month

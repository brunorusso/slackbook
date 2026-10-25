# 6. Process Control

Slackware systems often run hundreds or thousands of programs, each of which is referred to as a process in a Linux environment. Managing these processes is an important part of system administration.

So how exactly do we handle all of these separate processes? To help us with this task, there are several utilities we can use. In this chapter, we will explore some of the most common ones.


## 6.1 ps

The first step in managing processes is figuring out what processes are currently running. The most popular and powerful tool for this is `ps`. Without any arguments, `ps` won't tell you much information. By default, it only tells you what processes are running in your currently active shell. If we want more information, we'll need to look deeper.


```text

darkstar:~$ ps 
  PID TTY           TIME CMD 
12220 pts/4     00:00:00 bash 
12236 pts/4     00:00:00 ps

```

Here you can see what processes you are running in your currently active shell or terminal and only some information is included. The PID is the "Process ID"; every process is assigned a unique number. The TTY tells you what terminal device the process is attached to. Naturally, CMD is the command that was run. You might be a little confused by TIME though, since it seems to move so slowly. This isn't the amount of real time the process has been running, but rather the amount of CPU time the process has consumed. An idle process uses virtually no CPU time, so this value may not increase quickly.

Here, you can see what processes you are running in your currently active shell or terminal, with only basic information included. The PID is the "Process ID" — every process is assigned a unique number. The TTY tells you what terminal device the process is attached to. Naturally, CMD is the command that was run. You might be a little confused by TIME, though, since it seems to move so slowly. This isn't the amount of real time the process has been running, but rather the amount of CPU time the process has consumed. An idle process uses virtually no CPU time, so this value may not increase quickly.


Viewing only our own processes isn't very much fun, so let's take a look at all the processes on the system with the `-e` argument.

```text

darkstar:~$ ps -e 
PID TTY         TIME     CMD 
  1 ?        00:00:00 init 
  2 ?        00:00:00 kthreadd 
  3 ?        00:00:00 pool_workqueue_release
  4 ?        00:00:00 kworker/R-rcu_gp
  5 ?        00:00:00 kworker/R-sync_wq
  6 ?        00:00:00 kworker/R-kvfree_rcu_reclaim
  7 ?        00:00:00 kworker/R-slub_flushwq
  8 ?        00:00:00 kworker/R-netns
 10 ?        00:00:00 kworker/0:0H-kblockd
 11 ?        00:00:00 kworker/0:1-events
 12 ?        00:00:01 kworker/u64:0-gfx
 13 ?        00:00:00 kworker/R-mm_percpu_wq
 14 ?        00:00:00 ksoftirqd/0
 15 ?        00:00:01 rcu_preempt
 16 ?        00:00:00 rcu_exp_par_gp_kthread_worker/0
 17 ?        00:00:00 rcu_exp_gp_kthread_worker
 18 ?        00:00:00 migration/0
 19 ?        00:00:00 kprobe-optimizer
... many more lines omitted ...

```

**Note**

The above example uses the standard `ps` syntax, but much more information can be discovered if we use BSD syntax. In order to do so, we must use the `aux` argument.

This is distinct from the `-aux` argument, but in most cases the two arguments are equivalent. This is a decades-old relic. For more information, see the man page for `ps`.

```text

darkstar:~$ ps aux 
USER    PID     %CPU    %MEM    VSZ     RSS TTY STAT START TIME COMMAND 
root      1     0.0     0.0     3928    632 ?   Ss   15:45 0:00 init [4] 
root      2     0.0     0.0        0      0 ?   S    15:45 0:00 [kthreadd]
root      3     0.0     0.0        0      0 ?   S    15:45 0:00 [pool_workqueue_release]
root      4     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-rcu_gp]
root      5     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-sync_wq]
root      6     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-kvfree_rcu_reclaim]
root      7     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-slub_flushwq]
root      8     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-netns]
root     10     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/0:0H-kblockd]
root     11     0.0     0.0        0      0 ?   I    15:45 0:00 [kworker/0:1-events]
root     12     0.1     0.0        0      0 ?   I    15:45 0:01 [kworker/u64:0-gfx]
root     13     0.0     0.0        0      0 ?   I<   15:45 0:00 [kworker/R-mm_percpu_wq]
root     14     0.0     0.0        0      0 ?   S    15:45 0:00 [ksoftirqd/0]
root     15     0.1     0.0        0      0 ?   I    15:45 0:01 [rcu_preempt]
... many more lines omitted ....

```

As you can see, the `aux` argument offers much more information, including which user controls the process and what percentage of CPU and RAM the process is consuming when `ps` is run.

To accomplish this on a per-process basis, `ps` allows one or more process IDs (PIDs) to be provided on the command line and features the `-o` flag to display specific attributes of a PID.


```text
darkstar:~$ ps -o cmd -o etime
CMD                             ELAPSED
/bin/bash                         09:21
fish                              09:21
ps -o cmd -o etime                00:00
```

What this is displaying, is the PID's command name (cmd), and its elapsed time (etime). The PID in this example, is a shell variable for the PID of the current shell. So you can see, in this example, the shell process has existed for 9 minutes, 21 seconds.

By combining `ps` with the `pgrep` command, this process can be easily automated:

```text
darkstar:~$  ps -o cmd -o rss -o vsz $(pgrep chrome)
CMD                           RSS    VSZ
/opt/google/chrome/chrome   516976 51688644
/opt/google/chrome/chrome_c  4396 50355400
/opt/google/chrome/chrome_c  3812 50346164
/opt/google/chrome/chrome - 65816 50774672
/opt/google/chrome/chrome - 66164 50774660
/opt/google/chrome/chrome - 19420 50774688
/opt/google/chrome/chrome - 196028 51243208
/opt/google/chrome/chrome - 153324 50886676
/opt/google/chrome/chrome - 57752 50858720
/opt/google/chrome/chrome - 158208 1518473728
/opt/google/chrome/chrome - 353032 1524425320
/opt/google/chrome/chrome - 512404 1518545988
/opt/google/chrome/chrome - 289524 1518470868
/opt/google/chrome/chrome - 94932 50848384
/opt/google/chrome/chrome - 122228 1518466812
/opt/google/chrome/chrome - 165912 1518475280
/opt/google/chrome/chrome - 198144 1518534900
/opt/google/chrome/chrome - 53908 67618392
/opt/google/chrome/chrome - 418120 1518642108
/opt/google/chrome/chrome - 112568 1518360188
/opt/google/chrome/chrome - 126632 1520336712
/opt/google/chrome/chrome - 136956 1518380384
/opt/google/chrome/chrome - 77984 1518350972


```
In this example, command substitution using $(pgrep chrome) returns the PIDs of all running processes whose command names match 'chrome'. ps then displays each process's command name (cmd), resident set size (rss), and virtual memory size (vsz).


Finally, `ps` can also create a process tree. This shows you which processes have children processes. Ending the parent of a child process also ends the child. We do this with the `-ejH` argument.



```text

darkstar:~$ ps -ejH 
... many lines omitted ... 
3091  3091  3091 ?        00:00:00   login
3111  3111  3111 tty2     00:00:00     bash
3130  3130  3111 tty2     00:00:00       sddm.bin
3135  3135  3135 tty7     00:00:00         Xorg
3175  3130  3111 tty2     00:00:00         sddm-helper
3176  3130  3111 tty2     00:00:01           sddm-greeter-qt
3182  3130  3111 tty2     00:00:00   dbus-launch
3183  3183  3183 ?        00:00:00   dbus-daemon
3239  3239  3239 ?        00:00:00   sddm.bin
3244  3244  3244 tty8     00:00:55     Xorg
3327  3239  3239 ?        00:00:00     sddm-helper
3343  3239  3239 ?        00:00:00       dbus-run-sessio
3365  3239  3239 ?        00:00:01         dbus-daemon
3366  3239  3239 ?        00:00:00         startplasma-x11
3373  3239  3239 ?        00:00:00           plasma_session
3423  3239  3239 ?        00:00:01             kded6
... many more lines omitted ...

```

As you can see, `ps` is an incredibly powerful tool for determining not only what processes are currently active on your system, but also for learning lots of important information about them.

As is the case with many of the applications, there is often several tools for the job. Similar to the `ps -ejH` output, but more terse, is `pstree`. It displays the process tree, a bit more visually.

```text
darkstar:~$ pstree 
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

```

## 6.2 kill and killall

Managing processes isn't only about knowing which ones are running, but also about communicating with them to change their behavior. The most common way of managing a program is to terminate it. Thus, the tool for the job is named `kill` (1). Despite the name, `kill` doesn't actually terminate processes, but sends signals to them. The most common signal is a SIGTERM, which tells the process to finish up what it is doing and terminate. There are a variety of other signals that can be sent, but the three most common are SIGTERM, SIGHUP, and SIGKILL.

What a process does when it receives a signal varies. Most programs will terminate (or attempt to terminate) whenever they receive any signal, but there are a few important differences. For starters, the SIGTERM signal informs the process that it should terminate itself at its earliest convenience. This gives the process time to finish up any important activities, such as writing information to the disk, before it closes. In contrast, the SIGKILL signal tells the process to terminate itself immediately, no questions asked. This is most useful for killing processes that are not responding and is sometimes called the "silver bullet". Some processes (particularly daemons) capture the SIGHUP signal and reload their configuration files whenever they receive it.

In order to signal a process, we first need to know it's PID. You can get this easily with `ps` as we discused. In order to send different signals to a running process, you simply pass the signal number and `-s` as an argument. The `-l` argument lists all the signals you can choose and their number. You can also send signals by their name with `-s` .

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

Sometimes you may wish to terminate all running processes with a certain name. You can kill processes by name with `killall` (1). Just pass the same arguments to `killall` that you would pass to `kill` .

```text

darkstar:~$ killall bash # SIGTERM 
darkstar:~$ killall -s 9 bash # SIGKILL 
darkstar:~$ killall -s 1 bash # SIGHUP 
darkstar:~$ killall -s HUP bash # SIGHUP

```

## 6.3 top

So far we've learned how to look at the active processes for a moment in time, but what if we want to monitor them for an extended period? `top` (1) allows us to do just that. It displays an ordered list of the processes on your system, along with vital information about them, and updates periodically. By default, processes are ordered by their CPU percentage and updates occur every three seconds.

```text

darkstar:~$ top 
top - 16:44:15 up 26 days,  5:53,  5 users,  load average: 0.08, 0.03, 0.03
Tasks: 122 total,   1 running, 119 sleeping,   0 stopped,   2 zombie
Cpu(s):  3.4%us,  0.7%sy,  0.0%ni, 95.5%id,  0.1%wa,  0.0%hi,  0.2%si, 0.0%st
Mem:   3058360k total,  2853780k used,   204580k free,   154956k buffers
Swap:        0k total,        0k used,        0k free,  2082652k cached

  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND            
    1 root      20   0  3928  632  544 S    0  0.0   0:00.99 init               
    2 root      15  -5     0    0    0 S    0  0.0   0:00.00 kthreadd           
    3 root      RT  -5     0    0    0 S    0  0.0   0:00.82 migration/0        
    4 root      15  -5     0    0    0 S    0  0.0   0:00.01 ksoftirqd/0        
    7 root      15  -5     0    0    0 S    0  0.0   0:11.22 events/0           
    9 root      15  -5     0    0    0 S    0  0.0   0:01.19 work_on_cpu/0      
   11 root      15  -5     0    0    0 S    0  0.0   0:00.01 khelper            
  102 root      15  -5     0    0    0 S    0  0.0   0:02.04 kblockd/0          
  105 root      15  -5     0    0    0 S    0  0.0   1:20.08 kacpid             
  106 root      15  -5     0    0    0 S    0  0.0   0:01.92 kacpi_notify       
  175 root      15  -5     0    0    0 S    0  0.0   0:00.00 ata/0              
  177 root      15  -5     0    0    0 S    0  0.0   0:00.00 ata_aux            
  178 root      15  -5     0    0    0 S    0  0.0   0:00.00 ksuspend_usbd      
  184 root      15  -5     0    0    0 S    0  0.0   0:00.02 khubd              
  187 root      15  -5     0    0    0 S    0  0.0   0:00.00 kseriod            
  242 root      20   0     0    0    0 S    0  0.0   0:03.37 pdflush            
  243 root      15  -5     0    0    0 S    0  0.0   0:02.65 kswapd0

```

The man page has helpful details on how to interact with `top` such as changing its delay interval, the order processes are displayed, and even how to terminate processes right from within `top` itself.


## 6.4 htop

## 6.5 btop


## 6.6 cron

Ok, so we've learned many different ways of viewing the active processes on our system and means of signalling them, but what if we want to run a process periodically? Fortunately, Slackware includes just the thing, `crond` (8). cron runs processes for every user on the schedule that user demands. This makes it very useful for processes that need to be run periodically, but don't require full daemonization, such as backup scripts. Every user gets their own entry in the cron database, so non-root users can periodically run processes too.

In order to run programs from cron, you'll need to use the `crontab` (1). The man page lists a variety of ways to do this, but the most common method is to pass the `-e` argument. This will lock the user's entry in the cron database (to prevent it from being overwritten by another program), then open that entry with whatever text editor is specified by the VISUAL environment variable. On Slackware systems, this is typically the `vi` editor. You may need to refer to the chapter on `vi` before continuing.

The cron database entries may seem a little archaic at first, but they are highly flexible. Each uncommented line is processed by `crond` and the command specified is run if all the time conditions match.

```text

darkstar:~$ crontab -e 
#Keep current with slackware 
30 02 * * * /usr/local/bin/rsync-slackware64.sh 1>/dev/null 2>&1

```

As mentioned before, the syntax for cron entries is a little difficult to understand at first, so let's look at each part individually. From left to right, the different sections are: Minute, Hour, Day, Month, Week Day, and Command. Any asterisk <kbd>*</kbd> entry matches every minute, hour, day, and so on. So from the example above, the command is "/usr/local/bin/rsync-slackware64.sh 1>/dev/null 2>&1", and it runs every weekday or every week of every month at 2:30 a.m.

`crond` will also e-mail the local user with any output the command generates. For this reason, many tasks have their output redirected to `/dev/null` , a special device file that immediately discards everything it receives. In order to make it easier for you to remember these rules, you might wish to paste the following commented text at the top of your own cron entries.

```text

#Redirect everything to /dev/null with: 
#1>/dev/null 2>&1 
# 
#MIN HOUR DAY MONTH WEEKDAY COMMAND

```

By default, Slackware includes a number of entries and comments in root's crontab. These entries make it easier to setup periodic system tasks by creating a number of directories in `/etc` corresponding to how often the tasks should run. Any script placed within these directories will be run hourly, daily, weekly, or monthly. The names should be self-explanatory: `/etc/cron.hourly` , `/etc/cron.daily` , `/etc/cron.weekly` , and `/etc/cron.monthly` .

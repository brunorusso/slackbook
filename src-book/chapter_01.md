# 1. Introduction to Slackware

## 1.1 Why Use Slackware?

Slackware has a long tradition of excellence. Started in 1992 and first released in 1993, Slackware is the oldest surviving commercial Linux distribution. Slackware's focus on making a clean, simple Linux distribution that is as UNIX-like as possible makes it a natural choice for those people who really want to learn about Linux and other UNIX-like operating systems. In a 2012 interview, Slackware founder and benevolent dictator for life, Patrick Volkerding, put it thusly.

"I try not to let things get juggled around simply for the sake of making them different. People who come back to Slackware after a time tend to be pleasantly surprised that they don't need to relearn how to do everything. This has given us quite a loyal following, for which I am grateful."

Respect for the original code (Upstream): In the vast majority of cases, Slackware does not modify or patch source code simply to apply distribution-specific customizations. Instead, the developers’ role is to compile, package, and thoroughly test the software as provided by its original authors. This ensures predictable behavior, stability, and complete alignment with official upstream documentation.

Slackware's simplicity makes it ideal for those users who want to create their own custom systems. Of course, Slackware is great in its own right as a desktop, workstation, or server as well.


## 1.2 Differences Compared to Other Linux Distributions

There are a great number of differences between Slackware and other mainstream distributions such as Red Hat, Debian, and Ubuntu and others. Perhaps the greatest difference is the lack of "hand-holding" that Slackware will do for the administrator. Many of those other distributions ship with custom graphical configuration tools for all manner of services. In many cases, these configuration tools are the preferred method of setting up applications on these systems and will overwrite any changes you make to the configuration files via other means. These tools often make it easy (or at least possible) for a rookie with no in-depth understanding of his system to setup basic services; however, they also make it difficult to do anything too out of the ordinary. 

In contrast, Slackware expects you, the system administrator, to do these tasks on your own. Slackware provides no general purpose setup tools beyond those included with the source code published by upstream developers. Furthermore, while many other distributions extensively patch software to integrate custom features or distro-specific defaults, Slackware generally avoids modifying upstream code. The distribution focuses purely on compiling, packaging, and testing software in its unadulterated state. This means there is often a somewhat steeper learning curve associated with Slackware, even for those users familiar with other Linux distributions, but also makes it much easier to do whatever you want with your operating system.

Also, you may hear users of other distributions say that Slackware has no package management system. This is completely and obviously false. Slackware has always had package management. What it does not have is automatic dependency resolution - Slackware's package tools trade dependency management for simplicity, ease-of-use, and reliability.


## 1.3 Licensing

Each piece of Slackware (this is true of all Linux distributions) is developed by different people (or teams of people), and each group has their own ideas about what it means to be "free". Because of this, there are dozens of different licenses granting you different permissions regarding their use or distribution. Fortunately, dealing with free and open-source software licenses isn't as difficult as it may first appear. Most components are licensed under either the GNU General Public License (GPL) or permissive BSD-style licenses (including MIT and ISC). Sometimes you'll encounter software with a different license, but in almost all cases, they are remarkably similar to either the GPL or the BSD model.

Because Slackware ships unmodified upstream software, it offers complete license transparency: the original copyrights, permissions, and terms provided by upstream authors remain intact, without added layers of distribution-specific patches or proprietary helper tools.

Probably the most popular license in use within the Free Software community is the GNU General Public License. The GPL was created by the Free Software Foundation , which actively works to create and distribute software that guarantees the freedoms which they believe are basic rights. In fact, this is the very group that coined the term "Free Software." The GPL imposes no restrictions on the use of software. In fact, you don't even have to accept the terms of the license in order to use the software, but you are not allowed to redistribute the software or any changes to it without abiding by the terms of the license agreement. A large number of software projects shipped with Slackware, from the Linux kernel itself to the Samba project, are released under the terms of the GPL.

Another very common category includes permissive licenses like the BSD license, which is arguably "more free" than the GPL because it imposes virtually no restrictions on derivative works. The BSD license simply requires that the copyright notice remain intact along with a simple disclaimer. Many of the utilities and management scripts specific to Slackware are licensed under a BSD-style license or placed in the public domain, keeping the base system lightweight, unencumbered, and easy to inspect.

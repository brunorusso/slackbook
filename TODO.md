# General
 - [X] Create a README file
 - [X] Check if all content was migrated do markdown
 - [X] Improve script to build
 - [ ] Improve script to build pdf output
 - [X] Check licence
 - [ ] Check old authors
 - [X] Clean eps files and migrate png files to img directory 

 # New version
 - [ ] Update chapter 2. Installation to new slackware version, maybe 16.0
 - [ ] Update chapter 3. Booting add information about nvme
 - [ ] Check if chapter 4 need improve
 - [ ] Check if chapter 5 need improve
 - [ ] Check if chapter 6 need improve
 - [ ] Update chapter 7 X windows has any updates like wayland
 - [ ] Check if chapter 8 need improve
 - [ ] Check if chapter 9 need improve
 - [ ] Check if chapter 10 need improve
 - [ ] Check if chapter 11 need improve
 - [ ] Check if chapter 12 need improve
 - [ ] Check if chapter 13 need improve. Is it necessary?
 - [ ] Update chapter 14. Network
 - [ ] Update chapter 15. Wireless Network
 - [ ] Check if chapter 16 need improve
 - [ ] Check if chapter 17 need improve. Necessary add information about how use slackbuilds.org
 - [ ] Check if chapter 18 need improve
 - [ ] Check if chapter 19 need improve
 - [ ] New chapter about: slacklive; slackware docker image; kde/xfce; bluetooth ???


# Instructions

For any chapter was change, it is necessary check/update:

- Information about versions
- upgrade images
 

------------------------------------------------------------
# This sesion is old ToDo
* Make damn certain our Docbook markup is both _CORRECT_ and
  _CONSISTANT_. There's many places where the <screen> sections
  are very different. They should all be of this form.

<screen>
  <prompt>darkstar:~$ <prompt><userinput>_EVERYTHING_ the user types</userinput>
  Anything the screen prints that the user doesn't type.
</screen>

  I've found several cases where the <command> tag was used inside of a
  <screen> section. This is wrong and must be avoided. When the book
  goes to the publisher, all of those <command> tags will be formatted
  one way for printing and the <userinput> tags could be formatted
  another. Also, wrapping only applications in <command> tags could
  make the reader wonder just how much they are supposed to type.

* Aim to update references to kernel versions and Slackware versions to those 
  used in the most recent release of Slackware. I've seen kernel 2.6.29.4 and 
  Slackware 12.0.0 for instance.
  - 2012-08-22 Most of the Slackware versions should be fixed now.  -Alan

* more extensive CLI apps like v2.0

* no idea where the hell udev is covered in here, but we need to do a bit of
  talk about it.  Nothing too advanced, and we definitely DO NOT want to 
  imply that users should have to do much with udev.  All of the asshattery
  out there with trying to automount shit with udev is, well, asshattery.
  * need to mention that /etc/udev/rules.d/<somefile> overrides an identically
    named file in /lib/udev/rules.d/
  * need to mention persistent rules that are system-generated, especially
    in reference to how the admin might be misled into thinking that they are
    causing breakage...
  * need to point out that the persistent rules themselves are (according
    to upstream) a bad idea - not sure I completely agree, but there is a 
    lot of potential for breakage, it seems...

* Need to mention iptables somewhere - perhaps consolidate some bits from
  my iptables/netfilter presentations?  --rworkman

Chapter 2. Installation

* Should we include some partitioning examples using gdisk since this
  tool is increasingly required with today's modern systems? Perhaps add
  it as an appendix and mention it within the partitioning section?

Chapter 14. Networking

* We should probably include a "screenshot" of netconfig somewhere.

Chapter 18. Keeping Track of Updates

* Once 14.0 is released and there's a security update for it, we need
  to change the contents of the <screen> section to show what an actual
  -stable Changelog entry.

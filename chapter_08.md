# 8. Printing

## 8.1 Choosing A Printer

Linux hasn't always had a great history with printers. For many years, printing was a black art to many Linux users, and very few printers worked reliably. Today, most printers will work well with Linux, but some still do not. If you're purchasing a new printer, be aware that many of the cheap inkjet models aren't as well supported in Linux as more expensive laser printers. If you're unsure about a printer, you can check online to see if others have had success with it.

All these warnings are perhaps a bit overkill though, as the large majority of printers work with Linux after only a brief and simple setup. The progress in this direction is largely due to the efforts of the Common UNIX Printing System, (CUPS). CUPS is a printing system used by Slackware and most other Linux distributions today. It primarily uses a graphical setup procedure accessed via a web browser. In order to setup a printer with CUPS, you'll need to open a web browser such as firefox, konqueror, or links and go to http://localhost:631 .

![image](img/cups-01.png)

You might find that a quick click-through of CUPS configures your printer nearly automatically. Or, you may find that further configuration is required. To learn more about how printing works or how to get a stubborn printer configured, read on.

## 8.2 Getting the driver

There are, essentially, three types of printer drivers:

1. Postscript printers use the unversal-ish language of Postscript to communicate with computers. A driver for postscript printers is usually not needed, since a postscript-compatible subsystem called `Ghostscript` is already installed.

2. Gutenprint are drivers engineered by GNU Linux developers. It provides support for roughly 700 printers.

3. Manufacturers may provide Linux drivers for their printers. Find out by going to the manufacturer's driver and support website and searching for your model.

Since `gutenprint` is already installed on Slackware, from this set of three categories, we have two methods of installing drivers:

1. For the manufacturer's drivers, installation is usually the same as any other software on your system; use `installpkg` or `rpm2tgz` to install the driver package. Be sure to read the documentation bundled with the drivers.

2. For Postscript printers, there is no "installation" as such; simply download the appropriate `PPD` file and keep it in a sensible location on your hard drive.

Once you've located and installed or downloaded the necessary components, you're ready to run `CUPS` .

## 8.3 Setting Up a Printer in CUPS

From this point onward, setting up a printer is just a series of following the step-by-step instructions with CUPS, but understanding how the printing configuration actually works might help clarify what CUPS does is doing.

The file `/etc/cups/printers.conf` consists of definitions which detail the printing devices your computer will be able to access, with one marked as the default device. If you wish to edit this file manually (and you probably don't), you must stop the `cupsd` `CUPS` daemon.

A typical entry would look something like this:

```text

  <Printer r1060>
  Info Ricoh 1060
  Location Downstairs
  MakeModel Ricoh Aficio 1060 - CUPS+Gutenprint v5.2.6
  DeviceURI lpd://192.168.4.8
  State Idle
  StateTime 1316011347
  Type 12308
  Filter application/vnd.cups-raw 0 -
  Filter application/vnd.cups-raster 100 rastertogutenprint.5.2
  # standard-ish stuff below here
  Accepting Yes
  Shared No
  JobSheets none none
  QuotaPeriod 0
  PageLimit 0
  KLimit 0
  OpPolicy default
  ErrorPolicy stop-printer
  </Printer>

```

In this example, we have given the printer the name `r1060` , a human-readable identifier `Ricoh 1060` .

The `MakeModel` attribute is gained from `lpinfo` , which lists all available printer drivers on your system. So, if you know that you have a Ricoh 1060 that you want to print to, then you would issue this command as root:

```text

darkstar:~# lpinfo -m | grep 1060

```

This lists the drivers that you have installed, grepping for the string 1060:

```text

gutenprint.5.2://brother-hl-1060/expert Brother HL-1060 - CUPS+Gutenprint v5.2.6 
gutenprint.5.2://ricoh-afc_1060/expert Ricoh Aficio 1060 - CUPS+Gutenprint v5.2.6

```

The `MakeModel` is the last half of the appropriate result; in this case `Ricoh Aficio 1060 - CUPS+Gutenprint v5.2.6`

The final vital entry is the device URI, or where on the network (or physical location, such as the USB port), the printer can be found. In this example, we use `DeviceURI lpd://192.168.4.8` because we are using the `lpd` (line printer daemon) protocol to send data to the printer.

Now you understand what is being configured, and you can use the more common (and easier) method of doing this from the configuration tool that runs inside of a web browser.

In the CUPS interface, choose the Administration tab, and choose to Add Printer . You should be asked to enter administrative authorization here; enter `root` as the admin and your `root password` .

You will be presented with a list of printer interfaces and protocols that you can use for a printer. In many cases, you will want to add the printer via the `LPD/LPR` protocol (unless you've managed to find a printer that requires some other protocol).

Note that if the printer is plugged directly into your computer, and is on, you should see it listed as a Local Printer.

Assuming the printer is networked, the next screen will ask for the location of the printer. Using lpd:// as the protocol, enter the IP address of the printer. To find the IP address of the printer, you will probably need to look at the printer's settings, or you may be able to determine it from your router.

Whether your printer is connected via USB or network, the following screen will ask for human-readable details about the printer; this is for your reference only, so enter a name for the printer that makes sense to you and your users (the model number usually), a description (something that is distinctive about the printer if you have more than one of the same printers), and the location (describing where it is in the building).

On the next screen, point CUPS to the printer driver. If the printer is a postscript printer (as most laserprinters are) then you may need only the `PPD` for that printer. If your printer is not postscript or has special features that require additional drivers, then define the make (manufacturer) and you will then be presented with a list of available drivers. Select the appropriate driver.

The printer is now installed and will be the default printer for all of your applications.

## 8.4 Printing from the Command Line

Now that you have successfully installed and configured your printer, you may also use `lpr` to print from the command line.

`lpr` sends documents to a printer but before using it, you might want to define a default printer by using `lpadmin` as root:

```text

# lpadmin -d r1060

```

**Note**
In this example, `r1060` is the human readable name given to the printer in either `/etc/cups/printers.conf` or in the `CUPS` configuration.

If you do not have root privileges on the workstation you are using, you can also set the `PRINTER` environment variable:

```text

$ PRINTER=r1060 
$ export PRINTER

```

Once the printer has been set, then you may print:

```text

$ lpr foo.txt

```

### 8.4.1 Formatting for Print

`lpr` , like so many other UNIX applications, does one thig: sends files to a printer. It doesn't much care if the file looks good or even fits on a page. When printing large text files that have not been formatted for print, use `pr` (1).

`pr` is a simple text formatter that takes any text document and makes sure that it contains line breaks and page breaks, with an optional header and footer, page numbering, and much more. It has many options, but the defaults are usually good enough. `pr` outputs the results of the formatting to standard out, meaning it simply takes the text document, formats it, and displays the results in the terminal. This, of course, means that it can be redirected to `lpr` :

```text

darkstar:~$ pr foo.txt | lpr

```

This will format `foo.txt` and send the formatted output to the default printer.

As usual, see the `pr` man page for a list of the customizations you can make to the default formatting.

I have successfully installed the topspin 3.2pl2 in Opensuse, and work well under the client license. But my favorite Linux-OS is ubuntu dis, the lastest ubuntu LTS is 14.04 with the kernal-3.13.40. So I try to install topspin in Ubuntu 14.04, first I can install the whole sofeware in my system, but when I type the `topspin` in termina,
```
    % topspin
    TopSpin 3.2 pl 3 - Copyright (C) 2013 Bruker BioSpin GmbH
    Installation directory: "/opt/topspin3.2"
    Waiting for FLEXlm license
    valid until 2029-04-24
    mod cprserver: process seems to be dead

    premature cprserver termination
    Program is exiting ...

    Hit ENTER to continue ...
```
So I think the Bruker will release new topspin, I download the lastest release 3.2pl6, and install. Now the bug is:

0007099: system call msgrcv() from 32-bit application shows error:  msgrcv: No message of desired type

I google and yahoo the simaly problem, don't found how to fix. the bruker gay said this problem due to the kernal, because it will run well under kernal-3.10. I also send email to ask the bruker support if they have the solution. unfortunately， they said they have nothing to do, only report the bug to Linux Kernal developer.

The Good Think is Ubuntu 14.11 coming, and update the kernal to 3.16. I update the ubuntu release to 14.11, try.

Yes, this kernal fix the two problems.:), thanks Linux kernal developer, now i can using topspin under ubuntu.

Att: If you using the ubuntu 64bit, you have to install 32bit depanded package, when you install or run "topspin", it cannot found the "libxxxx" file or dir., now you can install libxxx:i386.

Att: If you don't have the license of topspin, you can request the demo license from bruker site (maybe you first register), it can using 3 monthes.

###update install topspin in Ubuntu 15.10 64bit
1. install the 32-bit support
```
sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386
```
2. sudo sh linux-topspin.sh
libX11.so.6 No such file or directory
```
sudo apt-get install libX11-dev:i386
```
libXft.so.2 No such file or directory
```
sudo apt-get install libXft-dev:i386
```
you can do:
```
sudo apt-get install libXft-dev:i386 libX11-dev:i386
```
3. now you can install successfully
4. installation finished, ```topspin```, the error popup:
libmawt.so: libXext.so.6: No such file or directory
```
sudo apt-get install libXext-dev:i386
```
libXtst.so.6: No such file or directory
```
sudo apt-get install libXtst-dev:i386
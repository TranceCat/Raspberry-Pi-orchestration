0 Raspberry Pi orchestration

In this Instructable I would like to share my personal work-flow for working with headless Raspberry Pi.
 If you are interested in automating the setup and deployment process for one Pi or many this is the post for you.
All the code is available on github:  ​Raspberry Pi orchestration
Please give feedback as this is my first post and first python project. 
Many thanks to ​HackBergen club and ​Verkstedet hackerspace in Bergen, Norway for help, space and hardware to test my project. 
Thanks to ​Instructables for sending Raspery Pi 2 in quantity which allowed  to create big network for testing.

1 Short history

​cover picture link to preserve copyright on it [http://www.element14.com/community/servlet/JiveServlet/showImage/38-14865-192066/Raspberry%2BPi%2B%2BB%2B%2B(2).jpg]

I love RPi as a fast way to solve personal problems. Make a media center, maybe a internet radio, NAS or whatever.

I never tried running any desktop on RPi or connected keyboard to it. But to use it this way is not always easy. The fastest way I found was to use Google Coder project. It was so fast. Burn the image to SD card and connect ethernet cable or WiFi dongle and you are good to go. But as all raspbian solutions it needs 4 Gb sd card. I try to re use old cards or make projects as small as possible.

What I did for myself is a Frankenstein of different projects to make it possible to find all the raspberry pi's on the network, install any distro of your choice to sd card or USB flashdrive and them provision it as you need. And if you have apps to deploy you can do it too.

2 What you need

Raspberry pi, any model will do, this script can be changed to run on all of them. But it is much simpler if you don't use A or A+ because they don't have Ethernet port.
Internet. and fast one if you don't want to wait long/ For first runs all the files will be downloaded from external sources.
Any computer running OS X, Linux or Windows. All steps can be reproduced on any of the platforms, some modifications to the code needed.
Know basic python.
This tutorial is not for the people who only starting with Raspberry Pi.

Try

- https://www.raspberrypi.org/

- https://googlecreativelab.github.io/coder/

- http://www.instructables.com/tag/type-id/category-...

for guides for first start.

3 Sturcture

This os a big project for me, so I'll have to dived it into parts.

here is the first draft of what I wanted to achieve:

rpi_detector
dicovery module, use any way to detect ip by partial mac address
use the ip to create ansible inventory
optional
test for standard login methods # integrated in rpi_ssh
ssh with password
ssh with key
rpi_inventory
use detector to get _list_ of Rpis
rpi_ssh - generate ansible inventory based on a template
use templates for role definition
rpi_ssh
test for default ssh login methods
ssh with password
if true continue to switch to key, else ssh with key
ssh with key : if policy mandates switch to key, else exit

switch to key
use pre-defined root key
generate root key # if used for key deployment use this strategy - generate keys based on the _list_ for root
generate keys for defined users
generate authorised_keys files
copy to defined folders
rpi_create # will be used to deploy OS on raspberry pi with netinstaller
use template to generate
installer-config.txt
post-install.txt
copy needed files (authorized-keys, hosts, rules etc.)
update/change boot-loader
if local repository is used verify accessibility, update and verify needed packages
restart all affected machines to start creation process
- use base image if available
rpi_provission
if used as stand alone app:
rpi_detector
rpi_inventory
else
run update, upgrade playbook
run role provision playbooks
rpi_deploy
playbook for environment verification
playbook for deployment
playbook for deployment verification
rpi_monitor
monitor demon for controlling cluster status
failure detection and re-install
Next steps will describe how I managed and sometimes failed in thees steps.

I use OS X as a development platform, but tried to test all modules on Windows and Linux. I down't have full solutions for those platforms right now, hope to get them in the future.

4 OS

To do anything with Raspberry Pi you need to install minimal software.

OS for Raspberry Pi come in different flavors, you can find some on official website or search for "raspberry pi os".

I use alternative way to get very small and custom os installed raspbian net installer.

Pros:

very minimal install, in minimal server configuration uses ~380 Mb.
customizable. You can define packages needed.
Simple install, copy files to FAT partition on SD card and plug it to RPi
Can install to USB flashdrive or other media if needed
It is possible, after first run, re-install OS without taking out SD card or touching RPi via ssh.
Cons:

Needs internet to get files from repository, if you deploy many machines it will consume lots of traffic. For this case it is recommended to have local clone of repository with necessary packages and use Ansible to add additional ones on per-machine basis.
Takes time. If used over Internet speed of install will depend on downlink.
You can run this once and create preferable base installation, create an image of it and use that next time.

Yes, it is possible to use base image to deploy os over network.(Will add if there is interest)

To define installer parameters and install additional packages use installer-config.txt. Put it on /boot partition of SD card you plug to your RPi.

If you want to use Ansible next add python to your custom installer-config.txt. It would be a good thing to change root password, just in case.

5 Detector

By now you should have a raspberry pi running, with os of your choice and connected to your network.

There are options how to find Raspberry Pi on the network.

nmap - great multi platform tool for network discovery and security auditing. You can scan your network for all connected devices and get ip addresses for RPi. Downside is that you need to install it on OS X and Windows and not all Linux distros have it pre-installed. I use it all the time for different applications and if you like it – use this option for the discovery part.
login to your router if possible and look up the ip that was assigned to RPi. Not very scriptable process.
if RPi has avahi-daemon running than use Apple zeroconfig, Bonjour in Windows, or avahi-browse in Linux to get ip addresses.
Pi Finder.app - Simple Apple script app for discovery.
many more
I needed small and fast solution that needs no additional apps, libs for python – "arp". Arp is networking tool available on almost all platforms, definitely on OS X, Windows and Linux. It produces basically same output and readily available through python.

You can see I found 4 RPi's on my network.

There is a caveat with this code. By default arp table is empty and you have to fill it. My monitor server fills it for it constantly in contact with all machines.

Possible solutions:

- use nmap instead, or use it as a solution to fill the arp table .

- add ping loop for the subnet scan

I use arp because nmap needs additional library in python to function properly and parsing nmap output as is not as simple as arp for me.

From her you can pipe it to next stage.

6 Inventory

So we got ip addresses.

We can use them to connect to RPi's using ssh and configure them as we want.

For automating this process there are special tools: Puppet, Chef, SaltStack etc.

I use Ansible because:

Server only. Doesn't need client software installed
Python based
Very simple YAML configuration files
Main concept is to ru scripts with tasks you want to perform(Playbooks) against list of machines you have (Inventory). Read more in documentation.

This step explains how to make inventory file from list of IPs we got before.

7 Ansible Playbooks

This part is just an example of what is possible with ansible playbooks.

I will use my testing project to deploy raspberry pi temperature monitor with web interface. It uses :

python script to:

get temperature from ds18b20 1-wire sensors, store it in sqlite database;

view a web ui with temperature plot

apache server to serve web page and run cgi script to generate temperature plot.

File structure of my project

- project folder/

- inventory

- main.yml # is the main file that I run to do all tasks, it includes update/upgrade features, provisioning and deploymnent tasks. As it is simple project there no roles and decision making.

- files/ # is a folder to store all files you need to copy to raspberry pi, for example public ssh keys

- playbooks/ # is a folder for ansible playbooks, if you want to have separate set of tasks for different scenarios like update/upgrade as you don't want to run it every time.

- vars/ # stores files with different variables you might need like paths and permissions, user lists etc.

- templates/ # stores jinja2 template files to generate different things on the machines. I use it to create apache configuration, but it's not necessary for simple setup


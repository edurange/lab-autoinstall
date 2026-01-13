These are install configurations for subiquity ("ubiquity for servers"), Canonical's official tool for automating Ubuntu server installation. subiquity is based on cloud-init, a tool for standardizing Linux deployment.

subiquity/cloud-data config files can be supplied to the installer in a number of ways. Here, I've created an ISO disk image that is mounted alongside the installation media. If you wanted to use this on a physical machine, you'd put the autoinstall ISO on a thumb drive or SD card, and the server installer on a DVD or other USB drive, and start the computer with both attached. The Ubuntu installer looks for a volume with a certain name, and if it finds it, loads config data from there. In a VM, we do something similar.

# Lo-fi instructions in VirtualBox:

Create a virtual machine per the usual EDURange specifications, but be sure to use Ubuntu Server, not the desktop version (desktop packages will be installed, but the desktop installer itself is not compatible with subiquity/cloud-init):
- Select "New" in VirtualBox
- The server image can be found at https://ubuntu.com/download/server - but note that the autoinstall profiles are version specific; at this time I have a config confirmed working on Ubuntu 24.04.3 LTS, which should be generally expected to be compatible with all 24.04 releases
- Select the "ISO Image" in the "New Virtual Machine" window and navigate to the server installer ISO
- "Proceed with Unattended Installation" may become checked automatically when VirtualBox sees an installer flavor it recognizes; make sure it is unchecked before proceeding
- In the subsequent "Specify virtual hardware" and "Specify virtual hard disk" sections, select 4096MB (4GB) "Base Memory" (RAM) and 2 CPUs, then 50GB for "Disk Size"
- Click "Finish", but do not start the VM after VirtualBox finishes creating it; we haven't attached the autoinstall configuration yet
 
Adjust the settings of the virtual machine to add a bridged network adapter and attach the autoinstall media:
- Images are attached to releases in this repo, such as https://github.com/edurange/lab-autoinstall/releases/download/v0.1-alpha/autoinstall-24.04.iso - you can generate your own image, but I'm not prepared to give a full explanation of what's required here
- Select the VM in the main window, and then click "Settings" in the toolbar or right-click context menu
- Select the "Network" section
- The view should default to the first tab in the "Network" section, "Adapter 1"; under "Attached to" change the drop-down menu to "Bridged Adapter"
- Select the "Storage" section
- In the "Devices" list, select "Controller: SATA"
- In the "Attributes" panel on the right side of the window, change "Port Count" to 3
- Back on the "Controller: SATA" row, there are two icons on the right with green pluses - select the left one of the pair, which should have the tooltip "Add optical drive"
- The autoinstall file isn't really an optical drive, but we can treat it as read-only, which I think is about what that means here; select it
- Click "OK" to apply the configuration changes

Start the VM:
- Obviously, at some point you've got to start it
- It takes a bit of booting for cloud-init to kick in
- Once cloud-init is running, it will ask you to confirm the installation once with a yes or no - after that, it's touchless
- The desktop environment isn't on the server installation media, so pulling that down takes a while; the installer may be relatively inactive for several minutes at a time while doing things like resolving package dependencies or downloading from the package repository
- At times the installer may only output messages such as "subiquity/Network/_send_update" repeatedly while waiting for a background process to complete - this is not evidence of a failure or infinite loop, it is just the network service reporting state changes while something slow happens, so do not interrupt the installer
- To inspect the progress of the installer you can use Ctrl+Alt+F2 to switch to a different virtual console (you may need to enter this key combination in the soft keyboard)
- While in the installer shell in the virtual console, take caution to do only read-only operations; do not use `apt`, as contention for locks can cause the installer to fail without warning
- You can safely view logfiles, or get diagnostic information with `ps`, `iostat`, `top`, or `ip`; try `sudo tail -f /var/log/installer/curtin-install.log`
- Treat yourself to a cup of coffee - you've earned it, tiger

Minimal system configuration:
- The installer sets up one sudoer user account called 'sysadmin' with a password that must be changed immediately upon login - we should discuss how we want to handle this in practice, but for now you can guess it
- The system is configured by default with an extra MOTD that instructs the first user to create a normal user account, add it to the sudo group, and switch to that
- sshd should be enabled, so you can SSH in right away
- To start the desktop environment, use `systemctl start gdm3` (**G**NOME **D**esktop **M**anager **3**)
- If you indeed used VirtualBox, you might want to `sudo apt install virtualbox-guest-utils virtualbox-guest-x11` or select "Devices" > "Insert Guest Additions CD image..." from the menu of the VirtualBox window

# Table of Contents
- [Quadruped ROS Gazebo project](#Quadruped-Robot-Project)
- [Setup](##Setup)
- [Run](##Run)
- [Controllers](##Controllers)
- [Keyboard Teleoperation](##Keyboard-Teleoperation)
- [WSL setup](#WSL-setup)
- [License](#License)
- [Acknowledgements](#Acknowledgements)

# Quadruped-Robot-Project
Repository for EE5109 mini-project: Quadruped Robot Project. This repository contains all the files and code needed to simulate the notspot quadrupedal robot using Gazebo and ROS. The software runs on ROS noetic and Ubuntu 20.04. 
![image](https://github.com/user-attachments/assets/7ea9f32b-9309-42cf-9fc3-ef04f5e1460e)

##### note: the repository contains a Dockerfile, but if you have a Windows machine and no dedicated GPU, I recommend using wsl. See instructions below.

## Setup
To clone the repository, run:
```
git clone https://github.com/EE5109-Control-Locomotion-Navigation/Quadruped-Robot-Project.git
```
Once cloned, build and source:
```
cd src && catkin_init_workspace
cd .. && catkin_make
source devel/setup.bash
roscd notspot_controller/scripts && chmod +x robot_controller_gazebo.py
cp -r RoboticsUtilities ~/.local/lib/python3.8/site-packages
roscd notspot_joystick/scripts && chmod +x ramped_joystick.py
```
## Run
```
source devel/setup.bash
roslaunch notspot run_robot_gazebo.launch
```
## Controllers
As described in the original repository (https://github.com/lnotspotl/notspot_sim_py/tree/main), the project comes with four different controllers. These are:
### Rest Controller
![image](https://github.com/user-attachments/assets/b328e85e-0f40-4158-a5a8-aa70b514d996)
### Stand Controller
![image](https://github.com/user-attachments/assets/76c86229-46df-4345-9c26-a670f6827691)
### Trot Gait Controller
![image](https://github.com/user-attachments/assets/99cbe836-1e72-481b-bb4e-8c4420c66e9e)
### Crawl Gait Controller
![image](https://github.com/user-attachments/assets/1c80eb69-8b6b-40ea-8785-6d1bcfc8b96c)

The user can switch between these at runtime.

## Keyboard-Teleoperation
This repository comes with a rudimentary keyboard controller, based on teleop_twist_keyboard. To teleoperate the robot, open a second terminal and run the following from the project workspace:
```
source devel/setup.bash
roslaunch notspot_joystick teleop_keyboard.launch
```
You should see the following:
![image](https://github.com/user-attachments/assets/c6aa2a2c-101a-411b-b3ab-29409e1a17f0)

# WSL-setup
Unless you have a dedicated GPU, you will have to rely on the internal graphics card for 3D acceleration. Docker and virtual machines do not have good support for 3D acceleration. Based on this, I have found the best way to run simulations is through WSL. WSL allows you to run a Linux environment directly on Windows, making it possible to install and use ROS Noetic, which is officially supported on Ubuntu 20.04. The following are instructions on how to set it up:

### **Steps to Run ROS Noetic on WSL**

#### **1. Install WSL 2**
WSL 2 is recommended for better performance and compatibility.

1. Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
   - This installs WSL 2 and the default Ubuntu distribution.

2. If WSL is already installed, ensure it's set to version 2:
   ```powershell
   wsl --set-default-version 2
   ```

3. Restart your computer if prompted.

---

#### **2. Install Ubuntu 20.04 on WSL**
ROS Noetic requires Ubuntu 20.04. If you don't have it installed:

1. Open the Microsoft Store and search for **Ubuntu 20.04**.
2. Install the distribution.
3. Launch Ubuntu 20.04 from the Start menu and complete the initial setup (create a username and password).

---
![image](https://github.com/user-attachments/assets/2aa4ccf5-f2a7-405a-bb33-1d2ed705b76e)


#### **3. Set Up ROS Noetic in WSL**

Follow the official ROS Noetic installation instructions for Ubuntu 20.04.

1. **Update and Upgrade Packages**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Set Up ROS Noetic**:
   - Add the ROS Noetic repository:
     ```bash
     sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
     ```
   - Add the ROS key:
     ```bash
     sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
     ```
   - Update the package list:
     ```bash
     sudo apt update
     ```

3. **Install ROS Noetic**:
   - Install the full desktop version:
     ```bash
     sudo apt install ros-noetic-desktop-full
     ```
   - Or install the base version:
     ```bash
     sudo apt install ros-noetic-ros-base
     ```

4. **Initialize rosdep**:
   ```bash
   sudo rosdep init
   rosdep update
   ```

5. **Set Up Environment Variables**:
   Add the following to your `.bashrc` file:
   ```bash
   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

---

#### **4. Install Additional Dependencies**

Some ROS packages may require additional dependencies. Install them as needed:
```bash
sudo apt install python3-rosinstall python3-rosinstall-generator python3-wstool build-essential python3-rosdep python3-pip
```

---

#### **5. Test ROS Noetic in WSL**

1. Start a ROS Master:
   ```bash
   roscore
   ```
   - This should start the ROS master without errors.

2. Run a simple ROS node:
   - In one terminal, start the `turtlesim` node:
     ```bash
     rosrun turtlesim turtlesim_node
     ```
   - In another terminal, control the turtle:
     ```bash
     rosrun turtlesim turtle_teleop_key
     ```

---
![image](https://github.com/user-attachments/assets/20089601-60b7-413e-a81d-64f5c5bea450)

#### **6. Setting up Gallium Driver**
For reasons above my paygrade, 3D acceleration does not work out-of-the-box with WSL. Fortunately, there is a magic workaround: setting the `GALLIUM_DRIVER=llvmpipe` environment variable. The following instructions enable show you how to do this


### Steps to Set Environment Variables in WSL

1. **Edit the Profile Script:**

   You can add environment variables to your shell's profile script. This script runs every time you start a new shell session. For common shells like `bash`, this would typically be `~/.bashrc` or `~/.profile`.

   - Open the `.bashrc` or `.profile` file in your home directory with a text editor. For example, using `nano`:

     ```bash
     nano ~/.bashrc
     ```

2. **Add the Environment Variable:**

   Scroll to the end of the file and add the following line to set `GALLIUM_DRIVER` to `llvmpipe`:

   ```bash
   export GALLIUM_DRIVER=llvmpipe
   ```

3. **Save and Exit:**

   - Save the changes and exit the text editor. In `nano`, you can do this by pressing `CTRL + O` to save and `CTRL + X` to exit.

4. **Reload the Profile Script:**

   To apply the changes immediately without restarting your terminal, reload the `.bashrc` or `.profile` by running:

   ```bash
   source ~/.bashrc
   ```

5. **Verify the Setting:**

   After reloading, you can verify that the `GALLIUM_DRIVER` is set correctly by echoing the variable:

   ```bash
   echo $GALLIUM_DRIVER
   ```

   It should output `llvmpipe`.

   With this update, and with shadows disabled, you should be able to get 15-20fps in Gazebo. Further optimizations will get this even higher (e.g. changing the physics engine, reducing the mesh complexity etc)

   ![image](https://github.com/user-attachments/assets/50556fe3-feab-4979-a99e-9ba8bbe4e13d)


### **7. GUI Support in WSL**

By default, WSL does not support GUI applications. To run ROS tools like `rviz` or `gazebo`, you need to set up a **X server** on Windows.

#### **Steps to Enable GUI Support**:
1. Install an X server on Windows:
   - [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (recommended) or [Xming](https://sourceforge.net/projects/xming/).

2. Launch the X server:
   - Open VcXsrv and ensure "Disable access control" is checked.

3. Set the `DISPLAY` environment variable in WSL:
   ```bash
   export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
   ```
   - Add this line to your `.bashrc` to make it persistent:
     ```bash
     echo "export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0" >> ~/.bashrc
     ```

4. Test GUI support:
   - Run a GUI application like `xeyes`:
     ```bash
     sudo apt install x11-apps
     xeyes
     ```
   - If the X server is configured correctly, you should see the `xeyes` window on your Windows desktop.
   - To test the performance, run `glxgears`. The gears should turn smoothly, and the frame rate should be at least 100fps, hopefully higher
  
   ![image](https://github.com/user-attachments/assets/a85e5757-68b1-4eb8-99d2-2aa954325624)


---

### **8. Running ROS GUI Tools**

With GUI support enabled, you can now run ROS tools like `rviz` and `gazebo`:
```bash
rosrun rviz rviz
```

---

# Accessing WSL folders through Windows Explorer
In Windows 10, Windows Subsystem for Linux (WSL) is an environment that allows you to run a Linux instance directly within Windows. The files for the Linux distributions you install are stored in the Windows file system. Here's how you can access these WSL folders:

1. **Access via File Explorer:**
   - Open the Windows File Explorer.
   - In the address bar, type `\\wsl$` and press Enter.
   - You will see a list of installed Linux distributions. Click on the specific distribution to access its file system.

2. **Access via Direct Path:**
   - WSL stores its files in a specific location within your user profile folder. The default path is:
     ```
     C:\Users\<YourUsername>\AppData\Local\Packages
     ```
   - Locate the folder corresponding to your Linux distribution. It usually starts with the distribution name, such as `CanonicalGroupLimited.UbuntuonWindows_` for Ubuntu.
   - Navigate to:
     ```
     <DistributionFolder>\LocalState\rootfs
     ```
   - Here, you will find the root file system of your WSL distribution.

3. **Using WSL Command Line:**
   - You can also navigate to your Windows files from within the WSL terminal using the `/mnt` directory. For instance, your C: drive is accessible at `/mnt/c`. You can explore files using regular Linux commands like `ls`, `cd`, etc.
  
4. **Accessing WSL Home Folder:**
   - If you need to access your Linux home directory directly from File Explorer, you can create a symbolic link:
     - Open a WSL terminal.
     - Enter the following command:
       ```bash
       ln -s ~/ /mnt/c/Users/<YourWindowsUsername>/wsl_home
       ```
     - Now, you can navigate to `C:\Users\<YourWindowsUsername>\wsl_home` to access your Linux home directory.

**Note:** Direct access to WSL files from the Windows file system is possible, but modifying your Linux files from Windows can lead to permissions issues or data corruption. As a general rule, it's safer to interact with your Linux files using Linux tools via a WSL terminal.
## License

This project is licensed under the MIT License - see the [License](./LICENSE.TXT) file for details.

# Acknowledgements
This project is based on the **spotMicro** https://github.com/mike4192/spotMicro/tree/master and **notspot** project https://github.com/lnotspotl/notspot_sim_py projects. As per the spotMicro links and references, here are some useful resources:

- Spot Micro AI community: https://gitlab.com/custom_robots/spotmicroai
- Research paper used for inverse kinematics: Sen, Muhammed Arif & Bakircioglu, Veli & Kalyoncu, Mete. (2017).  Inverse Kinematic Analysis Of A Quadruped Robot. International Journal of Scientific & Technology Research. 6.
- Stanford robotics for inspiration for gait code: https://github.com/stanfordroboticsclub/StanfordQuadruped
- Spot micro URDF model copied and modified from Florian Wilk's repo
- https://gitlab.com/custom_robots/spotmicroai/simulation/-/tree/master/Basic%20simulation%20by%20user%20Florian%20Wilk

List of submodules utilized:
- ros-i2cpwmboard by bradanlane for PCA9685 support
- https://gitlab.com/bradanlane/ros-i2cpwmboard
- spot_micro_kinematics_python by me :) for python spot micro kinematic calculations:
- https://github.com/mike4192/spot_micro_kinematics_python
- spot_micro_kinematics_cpp by me :) for c++ spot micro kinematic calculations:
- https://github.com/mike4192/spot_micro_kinematics_cpp

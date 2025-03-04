FROM osrf/ros:noetic-desktop-full

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Example of installing programs
RUN apt-get update \
    && apt-get install -y \
    nano \
    vim \
    iputils-ping \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    python3-rosdep \
    python3-pip \
    ros-noetic-rospy \
    ros-noetic-joy \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*


# Example of copying a file
#COPY quadrupted_robot_tutorial/ /home/ros/ros_ws/


# Create a non-root user
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config


# Set up sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir PyQt5
# Set up entrypoint and default command
CMD ["bash"]
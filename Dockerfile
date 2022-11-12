FROM rockylinux:8
RUN dnf install -y which python3 python3-devel gcc gcc-c++ epel-release zlib-devel
RUN dnf config-manager --set-enabled powertools
RUN dnf localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
RUN dnf install -y OpenEXR-devel
RUN pip3 install OpenEXR
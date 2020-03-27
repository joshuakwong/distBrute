#!/bin/sh

# install configure golang
inst_golang () {
    echo "* downloading golang *"
    wget https://dl.google.com/go/go1.14.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.14.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    rm -rf go1.14.linux-amd64.tar.gz
}

inst_gobuster () {
    echo "* downloading gobuster *"
    go get github.com/OJ/gobuster
}

inst_aws () {
    echo "* installing awscli *"
    sudo apt install unzip
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip >/dev/null
    sudo ./aws/install >/dev/null
    mkdir ~/.aws
    cp ~/dispatch_files/cred ~/.aws/cred
    cp ~/dispatch_files/config ~/.aws/config
    rm -rf aws
    rm -rf awscliv2.zip
}

run_dispatch () {
    echo "* preparing dispatch.py *"
    # prepare for dispatch.py
    sudo apt -y update
    sudo apt -y install python3-pip
    pip3 install -r requirements.txt
    ./dispatch.py example.com --dir --dns
}



echo "--- dispatcher ---"
inst_golang
inst_gobuster
inst_aws
run_dispatch
echo "* dispatch.py completed *"


#!/usr/bin/env python3
import sys
import time
import signal
import validators
import json
import argparse
import scp
import paramiko
import boto3


ec2 = boto3.resource("ec2")
ec2Cli = boto3.client("ec2")
ec2instList = []


def main():
    signal.signal(signal.SIGINT, signal_handler)
    args = get_args()
    masterId = deploy_ec2()
    start_dispatcher(masterId)

    while True:
        time.sleep(3)
    termAllInst()


def start_dispatcher(instId):
    # cant exec command/send files without sleeping, maybe machine still in pending state
    time.sleep(4)
    send_files(instId, [
        "./dispatch.sh",
        "./dispatch.py",
        "./requirements.txt",
        "./dispatch_files"
        ])
    run_commands(instId, ["~/dispatch.sh"])


# ref https://stackoverflow.com/a/42688515
def run_commands(instId, cmd_list):
    key = paramiko.RSAKey.from_private_key_file("/Users/jk/.ssh/box.pem")
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        sshClient.connect(hostname = ec2.Instance(instId).public_ip_address, username = "ubuntu", pkey = key)
        for cmd in cmd_list:
            #cmd += " 2>&1"
            stdin, stdout, stderr = sshClient.exec_command(cmd)
            print(stdout.read())
        print("completed")

    except Exception as e:
        print("failure in run_command()")
        print(e)
        while True:
            time.sleep(10)
    sshClient.close()


def send_files(instId, file_list):
    key = paramiko.RSAKey.from_private_key_file("/Users/jk/.ssh/box.pem")
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for tries in range(0, 6):
        try:
            sshClient.connect(hostname = ec2.Instance(instId).public_ip_address, username = "ubuntu", pkey = key)
            for f in file_list:
                print("send_files: {} transfering...  ".format(f), end = "")
                with scp.SCPClient(sshClient.get_transport()) as scpClient:
                    scpClient.put(f, "~/", recursive = True)
                print("SUCCESS!")
            break
        except Exception as e:
            print("failure in send_files()")
            print(e)
            if tries == 5:
                while True:
                    time.sleep(10)
            else:
                tries += 1
                print("retrying in {} seconds...".format(str(tries*2)))
                time.sleep(tries*2)
                print("retry order: {}...".format(tries))
                continue

    sshClient.close()


def make_list(InstId):
    lst = []
    lst.append(InstId)
    return lst


def signal_handler(sig, frame):
    print("termainating all instances")
    termAllInst()
    sys.exit(0)


def inst_status(instId):
    status = ec2Cli.describe_instance_status(InstanceIds = make_list(instId))
    print(status)
    print("-------------")


def get_args():
    print("distBrute - A gobuster bruteforcer wrapper")
    parser = argparse.ArgumentParser(description="A Subdomain and Subdirectory bruteforcer on steorids")
    parser.add_argument("target", help="your target domain name, e.g. \"google.com\"")
    parser.add_argument("--dns", help="subdomain bruteforcing", action="store_true")
    parser.add_argument("--dir", help="subdir bruteforcing", action="store_true")
    parser.add_argument("--dnsw", dest="dnsw", help="subdomain bf wordlist")
    parser.add_argument("--dirw", dest="dirw", help="subdir bf wordlist")

    args = parser.parse_args()
    if not validators.domain(args.target):
        print("Error: <target> is not valid domain name")
        parser.print_help()
        sys.exit()

    arg = {"target": args.target,
            "dns": args.dns,
            "dir": args.dir,
            "dnsw": args.dnsw,
            "dirw": args.dirw
            }
    return arg


def deploy_ec2():
    newInstList = ec2.create_instances(
            ImageId = "ami-03ba3948f6c37a4b0", # using ubuntu 18.04 ami
            MinCount = 1,
            MaxCount = 1,
            InstanceType = "t2.micro",
            SecurityGroups=[
                'default',
                ],
            KeyName = "box",
            IamInstanceProfile={
                'Name': 'admin'
                }
            )

    newInstId = newInstList[0].id

    print("Successfully deployed instance")
    print("Wait until instance in running state...")
    newInst = ec2.Instance(newInstId)
    newInst.wait_until_running()
    print("attempt to print public ip: "+str(newInst.public_ip_address))
    ec2instList.append(newInstId)

    return newInstId


def termAllInst():
    ec2.instances.filter(InstanceIds = ec2instList).terminate()


if __name__ == "__main__":
    main()


# run command with ssm
#resp = ssm.send_command(
#        InstanceIds = make_list(newId),
#        DocumentName="AWS-RunShellScript",
#        Comment = "asdfasdfasdfasdfasdfasdf",
#        Parameters = {
#            "commands": [
#                "ping hitbag.gq -c 1"
#                ]
#            }
#        )
#command_id = resp['Command']['CommandId']
#output = ssm.get_command_invocation(
#        CommandId = command_id,
#        InstanceId = newId
#        )

#while output["Status"] == "InProgress":
#    print("waiting...")
#    time.sleep(0.1)
#    output = ssm.get_command_invocation(
#            CommandId = command_id,
#            InstanceId = newId
#            )

#json.dumps(output, indent=2)
#print("--------------------")
#print(output)



#!/usr/bin/env python3
import sys
import boto3



ec2 = boto3.resource("ec2")
ec2instList = []


def start_slave():
    pass


def main():
    instId = deploy_ec2()
    if instId is None:
        print("dispatch.py failed, cannot deploy")
    else:
        termAllInst()
        print("dispatch.py ran successfully, instId is {}", str(instId))
    pass


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


def get_args():
    print("distBrute - A gobuster bruteforcer wrapper (dispatcher module)")
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


if __name__ == "__main__":
    main()


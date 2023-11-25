import argparse
from paramiko import SSHClient
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Checks if hosts are reachable."
    )
    parser.add_argument("list", 
                        help = "File containing a list of IPs.")
    parser.add_argument("-J", "--jump",
                        dest = "jump_host")
    args = parser.parse_args()

    if args.jump_host:
        client = SSHClient()
        client.look_for_keys(True)
        client.connect(args.jump_host)
    with open(args.list , "r") as hosts_file:
        hosts = hosts_file.readlines()
        for host in hosts:
            if args.jump_host:
                stdin, stdout, stderr = client.exec_command("ping -c1 -w1 " + host + " >/dev/null; echo $?")
                if stdout.read() == "0":
                    continue
            else:
                if subprocess.call(["ping", "-c1", "-w1", host]) == 0:
                    continue
            print(host + " is unreachable.")
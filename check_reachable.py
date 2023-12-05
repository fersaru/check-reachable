import argparse
import subprocess

class bash_colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def get_args():
    parser = argparse.ArgumentParser(
        description = "Checks if hosts are reachable."
    )
    parser.add_argument("list", 
                        help = "File containing a list of IPs.")
    parser.add_argument("-J", "--jump",
                        dest = "jump_host")
    args = parser.parse_args()
    return args.list, args.jump_host

def read_hosts(hosts_file_path):
    hosts = []
    with open(hosts_file_path, "r") as hosts_file:
        hosts = hosts_file.read().splitlines()
    return hosts

if __name__ == "__main__":
    hosts_file, jump_host = get_args()
    hosts = read_hosts(hosts_file)

    for host in hosts:
        command = []
        if jump_host:
            command += ["ssh", "%s" % jump_host]
            
        command += ["ping", "-c1", "-w1", "%s" % host]
        if subprocess.run(command, stdout=subprocess.DEVNULL ).returncode == 0:
            print(bash_colors.OKGREEN + host + " is reachable." + bash_colors.ENDC)
            continue

        # this line is reached if any of above doesn't return 0
        print(bash_colors.FAIL + host + " is unreachable." + bash_colors.ENDC)
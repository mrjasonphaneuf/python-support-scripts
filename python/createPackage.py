#!/usr/bin/env python3
"""
System Utility: Build a package from source and deploy it to a given directory
                location on a set of servers.
Author:         Jason Phaneuf
Created:        July 2026
GitHub:         ://github.com/mrjasonphaneuf/support-tools/python/createPackages.py

Description:
    This script will configure and build an application from source, create a
    tar bundle, and optionally scp the bundle to the target servers and 
    extract the bundle into a target directory on the remote server if the
    deploy argument is given.

Usage:
   i.e. python createPackage.py --config createPackage.json -appname zlib-1.3.2 (--deploy)
"""

import os
import subprocess
import paramiko
import argparse
import json
import sys

def load_config(config_path, app_name):
    """Loads configuration from the JSON file provided and creates config variables"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"[!] Target configuration file missing: {config_path}")

    with open(config_path, 'r') as f:
        config = json.load(f)

    return {
        "SOURCE_DIR": config["src_root"] + "/" + app_name,
        "BUILD_TARGET_DIR": config["install_root"] + "/" + app_name,
        "TARBALL_NAME": "/tmp/" + app_name + "_dist.tar.gz",
        "SSH_USER": config["ssh_user"],
        "SSH_KEY_PATH": config["ssh_key_path"],
        "REMOTE_DEST_DIR": config["remote_dest_dir"],
        "TARGET_SERVERS": config["target_servers"]
    }

def compile_and_package(cfg):
    """Configure, compile and make the package."""

    if not os.path.exists(cfg['SOURCE_DIR']):
        print(f"[!] Target compilation path does not exist: {cfg['SOURCE_DIR']}", file=sys.stderr)
        return False

    print(f"[*] Entering build workspace: {cfg['SOURCE_DIR']}")
    os.chdir(cfg['SOURCE_DIR'])

    print("[*] Running configure...")
    conf_res = subprocess.run(["./configure", f"--prefix={cfg['BUILD_TARGET_DIR']}"],
    capture_output=True, text=True)
    if conf_res.returncode != 0:
        print(f"[!] ./configure validation aborted:\n{conf_res.stderr}")
        return False

    print("[*] Compiling via make...")
    make_res = subprocess.run(["make"], capture_output=True, text=True)
    if make_res.returncode != 0:
        print(f"[!] Build compilation failed:\n{make_res.stderr}")
        return False

    print(f"[*] Installing into: {cfg['BUILD_TARGET_DIR']}...")
    inst_res = subprocess.run(["make", "install"], capture_output=True, text=True)
    if inst_res.returncode != 0:
        print(f"[!] Installation aborted:\n{inst_res.stderr}")
        return False

    print(f"[+] Build successfully generated in: {cfg['BUILD_TARGET_DIR']}")
    print(f"[*] Creating tarball: {cfg['TARBALL_NAME']}")

    parent_dir = os.path.dirname(cfg['BUILD_TARGET_DIR'])
    dir_name = os.path.basename(cfg['BUILD_TARGET_DIR'])

    tar_res = subprocess.run(
        ["tar", "-czf", cfg['TARBALL_NAME'], "-C", parent_dir, dir_name],
        capture_output=True,
        text=True
    )

    if tar_res.returncode == 0:
        print("[+] Tarball creation successful.")
        return True
    else:
        print(f"[!] Tar ball creation failed:\n{tar_res.stderr}")
        return False

def deploy (cfg):
    """ Remote copy the tarball to target servers in the /tmp directory and extract to the target directory."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey = paramiko.RSKey.from_private_key_file(cfg['SSH_KEY_PATH'])

    for server in cfg['TARGET_SERVERS']:
        print(f"\n[*] Deploying to node: {server}")
        try:
            ssh.connect(hostname=server, username=cfg['SSH_USER'], pkey=pkey, timeout=10)
            sftp = ssh.open_sftp()
            remote_tarball_path = f"/tmp/{os.path.basename(cfg['TARBALL_NAME'])}"

            print(f"[*] Remote copying tarball ...")
            sftp.put(cfg['TARBALL_NAME'], remote_tarball_path)
            sftp.close()

            print(f"[*] Extracting the tarball ...")
            extract_cmd = f"sudo tar -xzf {remote_tarball_path} -C {cfg['REMOTE_DEST_DIR']}"
            stdin, stdout, stderr = ssh.exec_command(extract_cmd)

            if stdout.channel.recv_exit_status() == 0:
                print(f"[+] Tarball successfully extracted on host node: {server}")
                ssh.exec_command(f"rm -f {remote_tarball_path}")
            else:
                print(f"[!] Tarball extraction failed on {server}:\n{stderr.read().decode()}")
        except Exception as e:
            print(f"[!] Secure connection failed on host {server}: {e}")
        finally:
            ssh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build software package from source")
    parser.add_argument("-a", "--appname", required=True, help="Application name (e.g., httpd-2.4.68)")
    parser.add_argument("-c", "--config", default="createPackages.json", help="Path to json configuration file")
    parser.add_argument("-d", "--deploy", action="store_true", help="Copy the package to the target servers")
    args = parser.parse_args()

    try:
        cfg_data = load_config(args.config, args.appname)

        # Compile and generate the tarball local package asset
        if compile_and_package(cfg_data):
            # Check if the package is to be copied to the target servers
            if args.deploy:
                deploy(cfg_data)
                # Only clean up the local tarball if it was successfully shipped away
                if os.path.exists(cfg_data['TARBALL_NAME']):
                    os.remove(cfg_data['TARBALL_NAME'])
                print(f"\n[+] The package deployment for '{args.app}' is completed.")
            else:
                print(f"\n[+] Compilation completed. Package tarball is preserved at: {cfg_data['TARBALL_NAME']}")
                print("[*] Remote copy was bypassed (pass --deploy to execute rollout).")

    except Exception as err:
        print(f"[!] System processing halt: {err}")
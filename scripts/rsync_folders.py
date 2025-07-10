import argparse
import os
import subprocess
from typing import Any

folders = [
    # Rajeev
    {"src": "/mnt/Data/NextCloud/data/rajeev/files/Media/.", "dst": "/mnt/Content/Pictures/Rajeev"},
    # Iva
    {"src": "/mnt/Data/NextCloud/data/iva/files/Media/.", "dst": "/mnt/Content/Pictures/Iva"},
    # Riya
    {"src": "/mnt/Data/NextCloud/data/riya/files/Media/.", "dst": "/mnt/Content/Pictures/Riya"},
    # Riva
    {"src": "/mnt/Data/NextCloud/data/riva/files/Media/.", "dst": "/mnt/Content/Pictures/Riva"},
]


def sync_all_folders(folders: list[Any], dry_run: bool) -> None:
    for folder in folders:
        src_folder = folder["src"]
        dst_folder = folder["dst"]
        sync_folder(src_folder, dst_folder, dry_run)


def sync_folder(src_folder: str, dst_folder: str, dry_run: bool) -> None:
    if not os.path.exists(src_folder):
        print(f"Error: Soruce {src_folder} does not exists, skipping")
        return
    elif not os.path.isdir(src_folder):
        print(f"Error: Soruce {src_folder} either does not exists or not a folder, skipping")
        return

    if os.path.exists(dst_folder):
        if not os.path.isdir(dst_folder):
            print(f"Error: Destination {dst_folder} is not a folder, skipping")
            return
    else:
        os.makedirs(dst_folder)

    print(f"Syncing: {src_folder} => {dst_folder}")

    cmd: list = [
        "rsync",
        "--verbose",
        "--recursive",
        "--times",
        "--progress",
        "--delete",
        "--delete-excluded",
        "--exclude=.*",
        src_folder,
        dst_folder
    ]
    if dry_run:
        cmd.append("--dry-run")
    instance: subprocess.CompletedProcess = subprocess.run(cmd)
    if instance.returncode == 0:
        print(f"Synced {src_folder} to {dst_folder}")
    else:
        print(f"Error in syncing {src_folder} to {dst_folder}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ProgramName", description="What the program does", epilog="Text at the bottom of help")
    parser.add_argument("-d", "--dry-run", action="store_true")
    args = parser.parse_args()
    sync_all_folders(folders, args.dry_run)

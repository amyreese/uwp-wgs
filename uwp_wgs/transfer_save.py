"""Automate Snowrunner save file renaming described in https://blog.s505.su/2021/08/how-to-transfer-snowrunner-game-saves.html"""
import argparse
import struct
import os
import shutil
from uwp_wgs import container


def copy_file(input_dir, input_name, output_dir, output_name, dry_run):
    input = os.path.join(input_dir, input_name)
    output = os.path.join(output_dir, f"{output_name}.cfg")
    print(f"Copy {input} to {output}")
    if not dry_run:
        shutil.copy2(input, output)

def copy_rename_save(save_list, input_dir, output_dir, dry_run):
    for decoded_filename, hashed_filename in save_list:
        copy_file(input_dir, hashed_filename, output_dir, decoded_filename, dry_run)

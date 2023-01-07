"""Parse UWP container file"""
import shutil
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from rich import print

Translator = Callable[[Path], Path]


@dataclass
class ContainerFile:
    filename: Path
    hashname: Path


@dataclass
class Container:
    root: Path
    files: list[ContainerFile] = field(default_factory=list)


def decode_hash(hash_bytes: bytes) -> str:
    new_hash_bytes = bytearray()
    new_hash_bytes.append(hash_bytes[3])
    new_hash_bytes.append(hash_bytes[2])
    new_hash_bytes.append(hash_bytes[1])
    new_hash_bytes.append(hash_bytes[0])
    new_hash_bytes.append(hash_bytes[5])
    new_hash_bytes.append(hash_bytes[4])
    new_hash_bytes.append(hash_bytes[7])
    new_hash_bytes.append(hash_bytes[6])
    return new_hash_bytes.hex().upper() + hash_bytes[8:].hex().upper()


def parse_file_bytes(file_bytes: bytes) -> ContainerFile:
    filepath = file_bytes[:-32].decode("utf-16").strip("\x00")
    hash1 = decode_hash(file_bytes[-32:-16])
    hash2 = decode_hash(file_bytes[-16:])
    if hash1 != hash2:
        raise ValueError(f"Inconsistent hash for {filepath}")
    return ContainerFile(Path(filepath), Path(hash1))


def load_container(input_dir: Path) -> Container:
    files = [f for f in input_dir.glob("container.*") if f.is_file()]
    if len(files) != 1:
        raise FileNotFoundError(f"No single 'container.XYZ' file found in {input_dir}")
    container_path = files[0]

    container_files: list[ContainerFile] = []
    with open(container_path, "rb") as cf:
        _header = struct.unpack("I", cf.read(4))[0]
        numfiles = struct.unpack("I", cf.read(4))[0]
        for i in range(numfiles):
            container_files.append(parse_file_bytes(cf.read(160)))
    return Container(root=input_dir, files=container_files)


def dump_container(container: Container, output_dir: Path, translator: Optional[Translator] = None) -> None:
    if translator is None:
        translator = Path

    print(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for cfile in container.files:
        out = translator(cfile.filename)
        src = container.root / cfile.hashname
        dst = output_dir / out
        print(f"{cfile.hashname} -> {out}")
        shutil.copyfile(src, dst)

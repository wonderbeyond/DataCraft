from typing import Union, Tuple, List
import os
import re
from pathlib import Path
import logging

import yaml

logger = logging.getLogger(__name__)


def fs_load(
    inputs_dir: Union[str, Path],
    pattern: Union[str, re.Pattern],
    include_dir: Union[str, re.Pattern, None] = None,
    exclude_dir: Union[str, re.Pattern, None] = None,
    include_hidden: bool = False,
):
    """Load data specs from the filesystem."""
    inputs_dir = Path(inputs_dir) if isinstance(inputs_dir, str) else inputs_dir
    include_dir = re.compile(include_dir) if isinstance(include_dir, str) else include_dir
    exclude_dir = re.compile(exclude_dir) if isinstance(exclude_dir, str) else exclude_dir
    pattern = re.compile(pattern) if isinstance(pattern, str) else pattern

    spec_files: List[str] = []
    specs = []

    def _walk(
        dir: Path,
        loc: Tuple[str] = ()
    ):
        loc_str = os.path.join(*loc)
        take_current_dir: bool = True

        if exclude_dir and exclude_dir.match(loc_str):
            return

        if include_dir and not include_dir.match(loc_str):
            take_current_dir = False

        with os.scandir(dir) as it:
            for e in it:
                if e.name.startswith('.') and not include_hidden:
                    continue
                if e.is_dir():
                    _walk(e.path, (*loc, e.name))
                elif take_current_dir and e.is_file() and pattern.match(e.name):
                    spec_files.append(e.path)

    _walk(inputs_dir, '/')

    for spec_file in spec_files:
        with open(spec_file) as f:
            print(f'Reading {spec_file}')
            for doc in yaml.safe_load_all(f):
                specs.append(doc)

    print(f'Loaded {len(specs)} specs from {len(spec_files)} files.')
    for spec in specs:
        print(spec)

import argparse
import datacraft.loader


def main():
    parser = argparse.ArgumentParser(
        description='Make dataset from description.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-c', '--config', dest='config', default='craft.yaml')
    parser.add_argument('--pattern', help='Pattern to match input files by name.', default=r'.*\.ya?ml')
    parser.add_argument('--include-dir', help='Directories to include while matching input files.')
    parser.add_argument('--exclude-dir', help='Directories to bypass while matching input files.')
    parser.add_argument('inputs_dir', nargs='?', default='.')

    args = parser.parse_args()

    datacraft.loader.fs_load(
        inputs_dir=args.inputs_dir,
        pattern=args.pattern,
        include_dir=args.include_dir,
        exclude_dir=args.exclude_dir,
    )


if __name__ == '__main__':
    main()

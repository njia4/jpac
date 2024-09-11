import re
import os
import glob
import json
import datetime
import pathlib
import logging
import argparse

# TODO: move these into a config file
PATH_DATA_PARENT = pathlib.Path('/Users/njia/DataVault')
PATH_NAS_MACHINE3 = pathlib.Path('/Volumne/qpu3')
PATH_DATA_MACHINE3 = PATH_NAS_MACHINE3 / 'qpu3-dev/storage'
FORMAT_DATA_PATH_NAME = r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})-(.+)'

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

def jlogger(log_level):
    log_str = f''
    pass 

def make_date_path(date: datetime.datetime = datetime.datetime.now()) -> pathlib.PosixPath:
    date_stamp = date.strftime('%Y-%m-%d')
    date_path = pathlib.Path(PATH_DATA_PARENT) / date_stamp

    try:
        date_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Date folder ({date_path}) created!")
    except Exception as e:
        logger.error()
        print(e)

    return date_path

def make_data_path(parent_path: pathlib.PosixPath = make_date_path(), data_name: str = 'exp') -> pathlib.PosixPath:
    date_time_stamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    data_datetime_name = date_time_stamp+'-'+ data_name
    data_path = parent_path / data_datetime_name

    try:
        data_path.mkdir(parents=True, exist_ok=True)
        logger.info("")
    except Exception as e:
        print(e)
    
    return data_path

def make_datetime_file_name(file_name):
    date_time_stamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    return '{}-{}'.format(date_time_stamp, file_name)
    
def parse_path_name(path):
    path_name = os.path.split(path)[-1]

    r = re.match(FORMAT_DATA_PATH_NAME, path_name)
    if not r:
        logger.error(f'Failed to parse the path name {path_name}')
        return 
    
    date = f'{r.group(1)}-{r.group(2)}-{r.group(3)}'
    time = f'{r.group(4)}:{r.group(5)}:{r.group(6)}'
    name = r.group(7)

    return date, time, name
    
def list_path(args):
    if args.parent:
        parent_path = pathlib.Path(args.parent.strip())
        logger.info(f'Parent data path: {parent_path}')
    elif args.date:
        date_stamp = datetime.datetime.strptime(args.date.strip(), '%Y-%m-%d')
        parent_path = make_date_path(date_stamp)
        logger.info(f'Parent data path: {parent_path}')
    else:
        parent_path = make_date_path()

    paths = parent_path.glob('*')

    header = "".join(f'{h:<12}' for h in ['Date', 'Time', 'Name'])
    print(header + '\n' + '-'*50)
    for _path in paths:
        if not _path.is_dir():
            continue
        date, time, name = parse_path_name(_path)
        print( f'{date:<12}{time:<12}{name}' )

def create_data_path(args) -> pathlib.PosixPath: 
    if args.parent:
        parent_path = pathlib.Path(args.parent.strip())
        logger.info(f'Parent data path: {parent_path}')
    elif args.date:
        date_stamp = datetime.datetime.strptime(args.date.strip(), '%Y-%m-%d')
        parent_path = make_date_path(date_stamp)
        logger.info(f'Parent data path: {parent_path}')
    else:
        parent_path = make_date_path()

    data_name = 'exp' if args.name.strip() == '' else args.name

    data_path = make_data_path(parent_path, data_name)
    print(data_path)

    return data_path

def main():
    parser = argparse.ArgumentParser()
    
    cmd_parsers = parser.add_subparsers(dest='command')

    cmd_create_parser = cmd_parsers.add_parser('create', help='Create new path for the data')
    cmd_create_path_group = cmd_create_parser.add_mutually_exclusive_group(required=False)
    cmd_create_path_group.add_argument('-p', '--parent', type=str, help="Specify the parent path directly")
    cmd_create_path_group.add_argument('-d', '--date', type=str, help="Specify the date (will convert to parent path)")
    cmd_create_parser.add_argument('-n', '--name', type=str, default='', help='Name of the experiment')
    cmd_create_parser.set_defaults(func=create_data_path)
    
    cmd_list_parser = cmd_parsers.add_parser('list', help='List experimental path')
    cmd_list_path_group = cmd_list_parser.add_mutually_exclusive_group(required=False)
    cmd_list_path_group.add_argument('-p', '--parent', type=str, default='', help='Parent path for the data')
    cmd_list_path_group.add_argument('-d', '--date', type=str, default='', help='Date path to look at')
    cmd_list_parser.set_defaults(func=list_path)

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

import argparse
import hashlib
import os
import shutil
import time

parser = argparse.ArgumentParser(description='One way synchronization of two folders.')
parser.add_argument('source', metavar='source', type=str, help='Source folder path')
parser.add_argument('replica', metavar='replica', type=str, help='Replica folder path')
parser.add_argument('interval', metavar='interval', type=int, help='Interval for synchronization in seconds')
parser.add_argument('log_file', metavar='log', type=str, help='the path to the log file')
args = parser.parse_args()


def current_path():
    print("Current working directory is:", os.getcwd())
    print()


def change_directory(path):
    # print("Changing directory to: ", path)
    os.chdir(path)


def iterate_folder(path):
    change_directory(path)
    for (root, dirs, files) in os.walk('.', topdown=True):
        print(root)
        print(dirs)
        print(files)
        print('--------------------------------')


def folder_synchronization(source_folder, replica_folder, log_file):
    change_directory(source_folder)
    for (root, directories, files) in os.walk('.', topdown=True):
        for name in files:
            source_path = os.path.join(root, name)
            replica_path = os.path.join(replica_folder, source_path)
            my_file = open(source_path, 'rb')
            md5_source = hashlib.md5(my_file.read()).hexdigest()
            if os.path.exists(replica_path):
                my_file = open(replica_path, 'rb')
                md5_replica = hashlib.md5(my_file.read()).hexdigest()
            else:
                md5_replica = None
            if md5_replica != md5_source:
                shutil.copy2(source_path, replica_path)
                log(log_file, f"Copied {name}")
            my_file.close()
        for dir in directories:
            subdirectory = os.path.join(source_folder, dir)
            replica_subdir = os.path.join(replica_folder, dir)
            if not os.path.exists(replica_subdir):
                dir_path = os.path.join(replica_folder, dir)
                os.mkdir(dir_path)
                log(log_file, f"Creating {dir} directory")
            folder_synchronization(subdirectory, replica_subdir, log_file)


def removing(source_folder, replica_folder, log_file):
    change_directory(replica_folder)
    for (root, directories, files) in os.walk('.', topdown=True):
        for name in files:
            replica_path = os.path.join(root, name)
            relative_path = os.path.relpath(replica_path, replica_folder)
            source_path = os.path.join(source_folder, relative_path)

            if not os.path.exists(source_path):
                os.remove(replica_path)
                log(log_file, f"File not found in source, deleting {name}")
        for dir in directories:
            dir_path = os.path.join(root, dir)
            source_dir_path = os.path.join(source_folder, dir_path)
            replica_subdir = os.path.join(replica_folder, dir_path)
            if not os.path.exists(source_dir_path):
                shutil.rmtree(replica_subdir)
                log(log_file, f"Directory not found in source, deleting {dir}")


def log(log_path, message):
    print(message)
    log_path = os.path.join(log_path, "log.txt")
    my_log = open(log_path, 'a')
    my_log.write(f"{message}\n")
    my_log.close()


if __name__ == '__main__':
    while True:
        folder_synchronization(args.source, args.replica, args.log_file)
        removing(args.source, args.replica, args.log_file)
        time.sleep(args.interval)

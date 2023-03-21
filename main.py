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
    # print("Current working directory is:", os.getcwd())
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


        for i in directories:
            #dir_path = os.path.join(root, i)
            #source_dir_path = os.path.join(source_folder, dir_path)
            #replica_dir = os.path.join(replica_folder, dir_path)
            dir_path = os.path.join(root, i)
            source_dir_path = os.path.join(source_folder, dir_path)
            replica_dir = os.path.join(replica_folder, dir_path)
            print(dir_path)
            if not os.path.exists(replica_dir):
                if root!=".":
                    replicadir=os.path.join(replica_folder,i)
                    finalreplicadir=os.path.join(replicadir,root)
                    print(finalreplicadir)
                    #os.mkdir(finalreplicadir)
                else:
                    print(root)
                    print(dir_path)
                    print(i)
                    dirpath=os.path.join(replica_folder, i)
                    os.mkdir(dirpath)
                    log(log_file, f"Directory does not exist, creating {i}")
            if os.path.exists(source_dir_path):
                change_directory(source_dir_path)
                current_path()
                for (root, directories, files) in os.walk('.', topdown=True):
                    for name in files:
                        source_path = os.path.join(dir_path, name)
                        absolute_path = os.path.join(source_folder, source_path)
                        replica_path = os.path.join(replica_folder, source_path)

                        my_file = open(absolute_path, 'rb')
                        md5_source = hashlib.md5(my_file.read()).hexdigest()

                        if os.path.exists(replica_path):
                            my_file = open(replica_path, 'rb')
                            md5_replica = hashlib.md5(my_file.read()).hexdigest()
                        else:
                            md5_replica = None
                        if md5_replica != md5_source:
                            shutil.copy2(absolute_path, replica_path)
                            log(log_file, f"Copying {name} from {i}")
                        my_file.close()

        # deleting from replica
        change_directory(replica_folder)
        for (root, directories, files) in os.walk('.', topdown=True):
            for name in files:
                replica_path = os.path.join(root, name)
                relative_path = os.path.relpath(replica_path, replica_folder)
                source_path = os.path.join(source_folder, relative_path)

                if not os.path.exists(source_path):
                    print(replica_path)
                    os.remove(replica_path)

            for i in directories:
                dir_path = os.path.join(root, i)
                source_dir_path = os.path.join(source_folder, dir_path)
                replica_dir = os.path.join(replica_folder, dir_path)
                if not os.path.exists(source_dir_path):
                    shutil.rmtree(dir_path)
                    log(log_file, f"Deleting {i}")
                if os.path.exists(source_dir_path):
                    change_directory(replica_dir)
                    for (root, directories, files) in os.walk('.', topdown=True):
                        for name in files:
                            replica_path = os.path.join(dir_path, name)
                            replica_path_absolute = os.path.join(replica_dir, name)
                            relative_path = os.path.relpath(replica_path, replica_folder)
                            source_path = os.path.join(source_folder, replica_path)
                            if not os.path.exists(source_path):
                                os.remove(replica_path_absolute)
                                log(log_file, f"Deleting {name} from {replica_dir}")


def log(log_path, message):
    print(message)
    log_path = os.path.join(log_path, "log.txt")
    my_log = open(log_path, 'a')
    my_log.write(f"{message}\n")
    my_log.close()


if __name__ == '__main__':
    while True:
        folder_synchronization(args.source, args.replica, args.log_file)
        time.sleep(args.interval)

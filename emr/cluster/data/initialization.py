import os

bucket_name = "hyun"
cluster_name = "test"

def main():
    configure_python()
    configure_zeppelin()
    configure_livy()


def configure_python():
    # emr numpy version is too old to use awswrangler. and emr install numpy after bootstrapping.
    # so, run this code after emr install numpy.
    os.system("sudo python3 -m pip install -U --ignore-installed numpy")


def configure_zeppelin():
    os.system(f"sudo aws s3 cp s3://{bucket_name}/emr/{cluster_name}/zeppelin-site.xml /etc/zeppelin/conf.dist/zeppelin-site.xml")
    os.system(f"sudo aws s3 cp s3://{bucket_name}/emr/{cluster_name}/shiro.ini /etc/zeppelin/conf.dist/shiro.ini")

    # it doesn't work on bootstrap. so, running on initialization
    os.system(f"sudo aws s3 cp s3://{bucket_name}/emr/{cluster_name}/interpreter.json /home/hadoop/interpreter.json")

    def replace_hostname(path, new_path):
        import socket
        hostname = socket.gethostname()

        def read_file(file_path):
            with open(file_path, 'r') as f:
                return f.read()

        def write_file(file_path, data):
            with open(file_path, 'w') as f:
                f.write(data)

        interpreter_json = read_file(path)
        interpreter_json = interpreter_json.replace("ip-1-1-1-1", hostname)
        write_file(new_path, interpreter_json)

    replace_hostname("/home/hadoop/interpreter.json", "/home/hadoop/interpreter_new.json")
    os.system("sudo cp /home/hadoop/interpreter_new.json /etc/zeppelin/conf.dist/interpreter.json")
    os.system("sudo rm /home/hadoop/interpreter.json /home/hadoop/interpreter_new.json")
    os.system("sudo service zeppelin restart")


def configure_livy():
    # livy ignore pyFiles on spark-conf/spark-defaults,
    os.system("sudo aws s3 cp spark-defaults-livy.conf /etc/livy/conf.dist/spark-defaults.conf")


if __name__ == '__main__':
    main()

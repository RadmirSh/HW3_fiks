import pytest
from checkers import check_positive_output, get_output
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return check_positive_output(
        f"mkdir -p {data['input_path']} {data['output_path']} {data['external_path']} {data['external_path2']}",
        "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['file_count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if check_positive_output(f"cd {data['input_path']}; "
                                 f"dd if=/dev/urandom of={filename} bs={data['block_size']} count=1 iflag=fullblock", ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def clear_folders():
    return check_positive_output(
        f"rm -rf {data['input_path']}/* {data['output_path']}/* {data['external_path']}/* {data['external_path2']}/*",
        "")


@pytest.fixture()
def make_sub_folder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not check_positive_output(f"cd {data['input_path']}; mkdir {subfoldername} ", ''):
        return None, None
    if not check_positive_output(f"cd {data['input_path']}/{subfoldername};"
                                 f" dd if=/dev/urandom of={testfilename} bs={data['block_size']} count=1 iflag=fullblock", ''):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    check_positive_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']}{data['output_path']}/bad_arx",
                          "Everything is Ok")
    check_positive_output(f"truncate -s 1 {data['output_path']}/bad_arx.{data['archive_type']}", "")


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%s.%f")}')
    yield
    print(f'\nFinish: {datetime.now().strftime("%H:%M:%s.%f")}')


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = get_output('cat /proc/loadavg')
    check_positive_output(f"echo 'time:{time} count:{data['file_count']} size;{data['block_size']} stat:{stat}' >> stat.txt", '')
import yaml
from checks import check_negative_output

with open('configures.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_files, make_folders, clear_folders, make_bad_arx):
        result1 = check_negative_output(f"cd {data['output_path']};"
                                    f" 7z e bad_arx.{data['archive_type']} -o{data['external_path']} -y", "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, make_bad_arx):
        assert check_negative_output(f"cd {data['output_path']}; 7z t bad_arx.{data['archive_type']} ",  "ERRORS"),\
            "test2 FAIL"
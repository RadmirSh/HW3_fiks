import yaml
from checks import check_negative_output

with open('configures.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        result1 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result2 = check_negative_output(f"cd {data['output_path']}; ls", f"arx2.{data['archive_type']}")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        result1 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result2 = check_negative_output(f"cd {data['output_path']}; 7z e arx2.{data['archive_type']} -o{data['external_path']} -y",
                           "Everything is Ok")
        result3 = check_negative_output(f"cd {data['external_path']}; ls", make_files[0])
        assert result1 and result2 and result3, "test2 FAIL"

    def test_step3(self, clear_folders, make_files):
        result2 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result1 = check_negative_output(f"cd {data['output_path']}; 7z x arx2.{data['archive_type']} -o{data['external_path2']}",
                           "Everything is Ok")
        assert result1 and result2, "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        result1 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result2 = check_negative_output(f"cd {data['output_path']}; 7z l arx2.{data['archive_type']}", make_files[0])
        assert result1 and result2, "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        result2 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result1 = check_negative_output(f"cd {data['output_path']}; 7z t arx2.{data['archive_type']}",
                        "Everything is Ok")
        assert result1 and result2, "test5 FAIL"

    def test_step6(self):
        assert check_negative_output(f"cd {data['input_path']}; 7z u {data['output_path']}/arx2.{data['archive_type']}",
                        "Everything is Ok"), "test6 FAIL"

    def test_step7(self, make_files, make_sub_folder):
        result2 = check_negative_output(f"cd {data['input_path']}; 7z a -t{data['archive_type']} {data['output_path']}/arx2",
                           "Everything is Ok")
        result1 = check_negative_output(f"cd {data['output_path']}; 7z d arx2.{data['archive_type']}",
                        "Everything is Ok")
        assert result1 and result2, "test7 FAIL"
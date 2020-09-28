import os
import shutil

file_path = 'H:\\movie\\v\\'
sub_task = os.listdir(file_path)
print(sub_task)

target_file = 'H:\\movie\\v\\mv\\'

dir_list = [file_path + i for i in sub_task]
count = 0
for i in dir_list:
	s = os.walk(i)
	for root_path, sub_dir, file_name_list in s:
		for file in file_name_list:
			base_file = root_path + '\\' + file
			file__ = os.path.splitext(file)
			if file__[1] == '.mp4':
				print(file)
				count += 1
				print(count)
				s = file__[1]
				print(s)
				targets_file = target_file + str(count) + '.mp4'
				print(target_file)

				shutil.copy(base_file, targets_file)
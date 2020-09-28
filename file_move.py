for i in dir_list:
	s = os.walk(i)
	for root_path, sub_dir, file_name_list in s:
		count = 0
		for file in file_name_list:
			count += 1
			base_file = root_path + '\\' + file
			file__ = os.path.splitext(file)
			if file__[1] == '.mp4':
				target_file = str(count) + '.mp4'
				print(base_file)
				print(target_file)
				shutil.move(base_file, target_file)
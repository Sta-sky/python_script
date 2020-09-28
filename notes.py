python的os模块，文件路径，文件写入：

遍历目录下以及子目录下所有文件：os.walk()
	返回三个参数：
		root_path_str, sub_dir_list, file_name_list = os.walk(file_path)
        	root_path_str: 当前遍历的根目录----str
            sub_dir_list: 当前目录中的子目录列表--list
            file_name_list: 当前目录中的文件列表---list

读取文件后缀名: ---os.path.splitext(file_path)
	返回一个元祖：
    	suffix_tuple = file_suffix = os.path.splitext(file_path)
        	suffix_tuple ---- > ('C:\\Users\\dwx917920\\Desktop\\操作指南\\交换机原理', '.pdf')
        # 取出后缀名
        suffix = suffix_tuple[1].split[1]
        
读取传入的文件或目录下的文件名：os.path.basename(file_path)
	依次返回文件或目录名称
    	file_name = os.path.basename(root_path + '\\' + file_name)
        
小结：
	可利用os.walk()遍历目录下的文件，通过os.path.basename获取文件的名，通过os.path,splitext()来获取文件后缀；
    

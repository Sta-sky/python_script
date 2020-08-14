
python的crypt加解密
pip install pycryptodome

$ 使用pyhton在linux命令行调用文件 中的方法
$ cd  /opt/FusionCloudDeploy/FusionCloudDeploy/utils/security
python -c 'import crypt; print(crypt.decrypt( "ZD4E7naUEkqJM4l/uWym/dJzhFHDWGRPxDJqFljnGmM="))'
python -c 'import crypt; print(crypt.encrypt("hello"))'



python的ipaddress模块的用法


import ipaddress

一、基础概念：

    ipaddress.ip_address()----------传入任意进制的数，自动创建返回一个ipv4或者ipv6地址，此函数会自动判断地址类别；

    ipaddress.ip_network()---------创建网络——使用格式为：ipaddress.ip_network('网络地址/掩码位数')相当于ipaddress.ip_network('网络网关/掩码位数')
    
    ps:
       网络地址指该ip段的第一个ip地址，网关，是该网段内的ip地址；因为strict参数的加入，
       可以直接使用网关通过strict将网关置为网络地址；就可以判断，ip是否在该平面内了
    

二、通过一个平面网关掩码，跟另一平面ip地址，判断此ip地址是否属于前者的平面内；
		ip_gateway = '25.1.0.1'
		ip_mask = '255.255.0.0'
        wangt_check_ip = '25.1.0.25'
        
        ip_and_mask
	    for check_ip in check_ip_list:
        	result = ipaddress.ip_address(check_ip) in ipaddress.ip_network(ip_and_mask, strict=False)
            if result:
            	print('在同一平面内')
            else:
            	print('不在同一平面内')

    eg：
        使用注意点：

            ipaddress.ip_network()--默认情况下，如果入参中设置了主机位，如‘192.168.1.1/24’，则会弹出错误提示——设置了主机位：
                主机位 : {192.168.1.0是没有设置主机位。从0开始的 ；  而192.168.1.1是从第一个 主机开始的  ip地址的最后一个数算是主机位}
            会报如下错误：
                        raise ValueError('%s has host bits set' % self)
                    ValueError: 192.168.1.1/24 has host bits set
            通过设置strict=False实现附加位强制为0；可以解决报错问题
                ipaddress.ip_network('192.168.1.1/24',strict=False)


    使用网关跟子网掩码，跟另一个平面的ip地址，可以判断两者是否在同一平面内，ip_address() in ip_network()


三、常用查询操作：
net=ipaddress.ip_network('192.168.1.0/24')
	(1)查看网络中独立地址个数
		print(net.num_ipaddress)
	(2)打印主机地址
    	for host in net.hosts():
        	print(host)
            
    (3)获取网络掩码：
    	net.netmask





sehll.md
变量自增：

1. i=`expr $i + 1`;
2. let i+=1;
3. ((i++));
4. i=$[$i+1];
5. i=$(( $i + 1 )

$LINENO--------脚本中打印执行代码对应的行数

$ 对变量进行操作后赋值给另一个变量要注意：---- 变量后面的语句是一条命令，并对命令进行echo输出，变量才会有值，没有echo 变量为None 
$ s=`export LD_LIBRARY_PATH=/opt/huawei-data-protection/ebackup/libs/:;/opt/huawei-data-protection/ebackup/db/bin/gsql -d admindb -U GaussDB -W Huawei@CLOUD8! -p 6432 -c "select COMPLETEVERSION from VERSION;"`
$ version= `echo $s | awk -F' ' '{print $3}'` $LINENO

    

 
数组 ：
my_array=(A B "C" D)
echo "第一个元素为: ${my_array[0]}"




匹配文件后缀或文件名 : 
name=${file#*.} #匹配文件后缀
name=${file%.*} #匹配文件名 



if语句 ：

 if [ -f /FileA -a -O /FileB ]; then

    if [ -f file ] ：如果文件存在
    if [ -d … ] ：如果目录存在
    if [ -s file ] ：如果文件存在且非空
    if [ -r file ] ：如果文件存在且可读
    if [ -w file ] ：如果文件存在且可写
    if [ -x file ] ： 如果文件存在且可执行
    
    逻辑非 ： !
        if [ ! -d $num ] ：表示如果不存在目录$num
        
    逻辑或 -o
        if [ 表达式1  –o 表达式2 ]  表示条件表达式的或
    逻辑与 –a
        if [ 表达式1  –a  表达式2 ]  表示条件表达式的与
        
        
    -eq 等于
    -nq 不等于
    -gt 大于
    -ge 大于等于
    -lt 小于
    -le小于等于



shell中常用字符含义
&& ：表示如果符号&&前面表达式为真，则执行&&符号后面的表达式
||：表示如果符号||前面表达式为假，则执行||符号后面的表达式。



shell中的case
case "${L_OPERATION}" in
         upload)
             log_info "[main(),$LINENO]upload"
             upload
             ;;
 
         precheck)
             log_info "[main(),$LINENO]precheck"
             precheck
             ;;
 
         upgrade)
             log_info "[main(),$LINENO]upgrade"
             log_info "[main(),$LINENO]before upgrade now write flag to ${G_UPGRADE_FLAG_FILE}"
             date > ${G_UPGRADE_FLAG_FILE}
             upgrade
             ;;
esac
shell中的sed

sed命令不会修改原文件，删除命令只表示某些行不打印输出，而不是从原文件中删去。

-n,--quiet,--silent  　　静默输出，默认情况下，sed程序在所有的脚本指令执行完毕后，将自动打印模式空间中的内容，这些选项可以屏蔽自动打印。
-e script            　　允许多个脚本指令被执行
-i,--in-place        　　直接修改源文件，经过脚本指令处理后的内容将被输出至源文件（源文件被修改）慎用！

a,append        追加
i,insert        插入
d,delete        删除


-p 匹配的行

-a 追加
# sed输出的文本中，在第二行后（第三行）添加 mmzs 
sed "2a mmzs" s.txt     ---------- 在第二行后，就是第三行，添加mmzs

-n 只输出与条件匹配的字符

-p  对应的行
sed -n '2p'  s.txt  ----------------输出s.txt文件第二行

sed -n '/abc/p' s.txt ------------- 输出包含abc对应行的字符；

sed '/ss/d' s.txt   ----------------删除有ss的行

            #   -i直接修改文件，
            
sed -i 's/haha/xixi' s.txt ---------对haha所在的行修改为xixi

sed -i '/ss/d' s.txt ---------------删除有ss的行

sed -i '/ff/10p' s.txt -------------删除第10行




Linux命令

mrpm包解压命令
$ rpm包解压
$ rpm2cpio FileName.rpm | cpio -div

#  端口查询
$ netstat -a

# grep过滤出带关键字的文件
$ grep -rl '关键字' '路径'；

# windows格式转linux格式
$ dos2unix + 转码文件


$ 使用pyhton在linux命令行调用文件 中的方法
$ cd  /opt/FusionCloudDeploy/FusionCloudDeploy/utils/security
python -c 'import crypt; print(crypt.decrypt( "ZD4E7naUEkqJM4l/uWym/dJzhFHDWGRPxDJqFljnGmM="))'
python -c 'import crypt; print(crypt.encrypt("hello"))'


$ linux 中上传文件或执行命令，没有权限；一般
    FCD的/home/pkg/目录  :



GIT

git本地新建分支推送到远程
$ git checkout -b  “分支名称”；   新建本地分支

$ git branch；     查看是否创建成功以及目前在哪个分支

$ git  push -u origin "分支名称"；本地推送到远程

$ git push -u origin master_8.0.5.SPC100_dyy  将分支推送到远程指定分支

$ git branch -d master_8.0.5.SPC100_dyy # 删除分支

$ git rm -r .idea    删除文件




交换机

# 根据mac地址查询对应的交换机端口
$ dis mac-address | include mac_id

# 显示所有交换机上端口配置信息
$ display current-configuration

#进入系统视图
$ system-view

#进入指定端口视图  (进入2号端口)
$ interface 10GE1/0/2

#进入接口视图
$ interface vlanif vlanid


# 查看当前界面属性
$ dis this

# 查看1073接口所有相连接的端口
$ dis vlan 1073

# 修改特权用户名密码
$ super password

# 交换机名
$sysname

# 配置VLANIP址
$ ip address 10.65.1.1 255.255.0.0

# 静态路由＝网关
$ ip route-static 0.0.0.0 0.0.0.0 10.65.1.2

# 设置端口工作模式
$ port link-type {trunk|access|hybrid}

# 创建VLAN
$ vlan 3

# 设置trunk端口PVID
$ port trunk pvid vlan 3

# 设置vlan的pvid
$ port hybrid pvid vlan <id>



Opensack 
Internal_Base平面是 OpenStack内部管理网络，用于OpenStack控制节点间的内部通信，具体来讲：OpenStack首节点发现其他的OpenStack节点，传输主机软件给其他OpenStack节点，完成PXE安装；Internal_Base使用的IP段默认为172.28.X.X，DHCP方式分配IP地址（如果需要修改IP网段，需要通过修改系统配置文件来实现
eBackup装机就是通过从openstack中使用dhcp分配ip的方式获取到装机ip，装出的机器会跟openstack的internal_base平面网络互通。


可用分区 ： 
 查询物理主机节点 ： nova hypervisor-list
 查询某个物理主机信息 ：nova hypervisor-show hypervisorId
查询主机的详细信息：cps host-show hostid 
 查询所有可用分区 : nova availability-zone-list

主机查询 ： 
 nova host-list : 查询所有主机
 
 nova hypervison-show hostid ： 查询主机与可用分区的详细信息

虚拟机 ： 
  nova list ：查询所有虚拟机
 nova list --host hostid ：查询某个主机下的虚拟机

查询openstack中注册的个服务访问地址以及配置域名：
	openstack catalog list
查询镜像列表
	openstack image list
查看镜像
	openstack iamge show id
删除镜像
	openstack image delete id
       
       
       
python的进制转换函数：
  
  ↓	   2进制		8进制		10进制			16进制
2进制	 -		bin(int(x, 8))	  bin(int(x, 10))	bin(int(x, 16))
8进制	oct(int(x, 2))	   -		  oct(int(x, 10))	oct(int(x, 16))
10进制	int(x, 2)	int(x, 8)		-		int(x, 16)
16进制	hex(int(x, 2))	hex(int(x, 8))	  hex(int(x, 10))	   -
       
       
总结  ： 
       任意进制转换成二进制： 
           bin(int('数值',‘数值对应的进制’))
      		eg:bin(int('23',8))----------八进制的数转换成二进制的数
       
       二进制 ： bin()
       八进制：oct(int('',''))
       十进制：int()
       十六进制：hex(int('',''))
       
       
 
       
 # 再次添加 ： 
       # shell中的diff 比较两个文件内容是否相同
	#/bin/sbin
	file1=/test.txt
	file2=/tmp/nihao.txt
	diff $file1 $file2 > /dev/null
	echo $?
	if [ $? == 0 ]; then
	    echo "相同"
	else
	    echo "两者不相同"
	fi
       
# Linux 
       	$ linux查看那些用户正在远程连接主机，并杀死不用的ssh连接:
	w / who都可以， 查看情况如下
        USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
        hcp      pts/0     15:07    9.00s  0.00s  0.00s -bash
        root     pts/1     14:56    7.00s  0.09s  0.00s w
	    杀死 hcp 命令：
		pkill -9 -t pts/0
	    查看那个是我正在使用的远程连接
		who am i

	$ linux查询正在使用的进程 ： 
		查询系统中全部进程:
			ps -ef 
	    列出此次登录的进程有关的进程：
		ps -l
	    杀死进程 ： 
	    kill -9 pid

	按文件名寻找文件：
		find path -name file_name
	    find path -

	用户登录设置文件：
		设置认证几次，设置修改密码时可以使用以前登录过的密码
		vi /etc/pam.d/system-auth


	linux、win中  添加路由:
		win ： 
		route add 192.168.120.12 mask 255.255.0.0 -p 192.168.0.1
	    linux:
			route add default gw 192.168.1.1 ------ 添加默认路由

	lsattr 命令用于显示文件属性：
		用chattr执行改变文件或者目录的属性，可执行lsattr指令 查询其属性。

	    chattr +i /etc/resolve.conf  # 用chattr命令防止系统中某个关键文件被修改
		# 然后用mv /etc/resolv.conf等命令操作于该文件，都是得到Operation not permitted 的结果。vim编辑该文件时会提示W10: Warning: Changing a readonly file错误。要想修改此文件就要把i属性去掉：

	    lsattr /etc/resolve.conf  # 使用 lsattr 命令来显示文件属性
       

shell
       查看/tmp 的磁盘使用情况
       	    [root@eBackup etc]#   df -h | sed -n '/\/tmp/p' | awk -F' ' '{print $5}' | sed 's/ //g'
		51%
	 解析 ： df -h--------------------------- 查看使用率， 
       		sed -n '/\/tmp/p'--------------- 过滤出包含/tmp的行 ‘\’转义/tmp中的跟路径
       		awk -F' ' '{print $5}' --------- 用空格分割，过滤出使用率的参数，
       		sed 's/ //g' ------------------- 去除输出内容的所有空格
       
       将输出的eBakcup系统 信息，中第一个字母 e 替换成 T
       		showsys | sed -n '5p' | awk -F '|' '{print $1}' | sed 's/e/T/'
       将输出的eBakcup系统 信息，中所有的字母 e 替换成 T
       		showsys | sed -n '5p' | awk -F '|' '{print $1}' | sed 's/e/T/g'
       
       

       	
       

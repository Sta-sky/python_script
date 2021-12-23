import ipaddress


"""
网络号的计算方法，将ip地址与子网掩码，转换成二进制的数，之后做按位与运算，得出的结果
        在转换成十进制，得到的ip就是网络号
主机号的计算方法：将子网掩码取反再与ip地址按位与运算
                （取反：’255.255.255.0’-----‘0.255.255.255’          
按位与 ： & 遇1得1，
总结 ：
    网络号=IP地址&子网掩
    主机号=IP地址&(取反后的子网掩码)
"""

class NetworkTool:

    @staticmethod
    def check_ip_segment(check_params):
        """

        :param check_params:
            check_params是一个列表，[ip_gateway,ip_netmask,check_ip_list]
            check_ip_list: 也是一个列表
        :return: 返回True or False
        """
        ip_gateway = check_params[0]
        ip_netmask = check_params[1]
        check_ip_list = check_params[2]
        ip_mask_num = str(sum([bin(int(x)).count("1") for x in ip_netmask.
                              split(".")]))
        ip_and_mask = ip_gateway + '/' + ip_mask_num
        print(ip_and_mask)

        for check_ip in check_ip_list:
            result = ipaddress.ip_address(check_ip) in ipaddress.ip_network(
                ip_and_mask, strict=False)
            if result:
                return True
            else:
                print("check ip:%s ip跟 %s 网络不是共平面" % (check_ip, ip_and_mask))
                return False

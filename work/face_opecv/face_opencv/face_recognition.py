
import os
import cv2

import numpy
import time

"""
    环境:
        python版本：3.7.8
        依赖包：
            numpy == 1.19.2
            opencv-python == 4.5.5.62
            opencv-contrib-python == 4.5.5.62

    代码逻辑：
    
    face_recognition.py
        人脸识别类：
            FaceRecognition
        
        方法：
            get_face_data：图片预处理函数
                1、获取save_user_face.py中采集到本地的人脸图片
                2、读取人脸图片，用cv2完成灰度转换，将转换后的ndarray数据存储再list中，
                3、为图片用户进行序号标记，序号存储再list中
            
            check_face_data: 人脸检测函数
                1、调用cv2的face.EigenFaceRecognizer_create接口创建人脸识对象
                2、将预处理的图片list数据转换为ndarray数据，传入face对象的训练函数中，
                3、打开摄像头，获取人脸数据，并处理成跟保存时一样的大小，一样的灰度图片。
                4、当识别次数达到20次，即为识别成功。
            
            
            handle_similarity：
                1、将check_face_data第三步获取的人脸数据，进行传入predict中进相似度对比，
                2、得到结果，并给当前用户人别成功次数+1
            
            judge_user_success：
                判断用户成功次数，返回bool值
                
            run:
                1、程序启动入口
                2、可以无限多次识别，给用户选择权
    * 注意路径中不能含有中文字符
    
"""


class FaceRecognition(object):
    
    def __init__(self, ):
        self.current_name = None
        # 图片加载路径
        self.load_face_path = f"{os.path.abspath('FaceImg')}/face/"
        self.list_dir = os.listdir(self.load_face_path)
        
        # 人脸数据list
        self.face_data_list = []
        # 文件名称list
        self.data_item_list = []
        self.user_dict = {item: 0 for item in self.list_dir}
    
    def get_face_data(self):
        """
            获取人脸文件夹下所有子文件夹
        """
        # 遍历文件夹  获取图片
        for item, dir in enumerate(self.list_dir):
            sub_dir = os.listdir(f"{self.load_face_path}{dir}")
            for file in sub_dir:
                filename = f"{self.load_face_path}{dir}/{file}"
                # 读取图片，获取图片数据，有值则存入两个list中
                image = cv2.imread(filename)
                # 灰度处理 COLOR_BGR2GRAY
                # cvtColor: cv2的颜色空间转换函数，实现RGB转HSV，HSI等颜色
                image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
                if image.size != 0:
                    # 将数据转换为一维数组存放在集合中
                    self.face_data_list.append(image.reshape(-1))
                    self.data_item_list.append(item)
        print('数据获取完成！')
    
    def check_face_data(self):
        print('开始检测人脸！')
        time_start = time.time()
        # 将列表转换为ndarray格式数据
        face_data = numpy.array(self.face_data_list)
        item_data = numpy.array(self.data_item_list)
        # 调用cv的face接口引擎 ， 创建脸部特征识别器
        face_obj = cv2.face.EigenFaceRecognizer_create()
        # 学习数据
        face_obj.train(face_data, item_data)
        # 打开摄像头
        video = cv2.VideoCapture(0)
        is_open = video.isOpened()
        if not is_open:
            print('打开摄像头失败...')
            raise
        # 加载人脸数据
        face_datector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        
        # 循环获取摄像头人脸数据
        count = 0
        while True:
            time.sleep(0.3)
            flag, img = video.read()
            # 改变图片为灰度图
            img_gray = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
            # 扫描图片获取人脸位置
            face = face_datector.detectMultiScale(image=img_gray, scaleFactor=1.1, minNeighbors=4)
            
            # 用户输入q退出程序
            index = cv2.waitKey(1000 // 24)
            if ord('q') == index:
                break
            if flag:
                if isinstance(face, tuple):
                    print("当前人脸数据为空！")
                else:
                    # 遍历返回面部数据, 调用cv2的脸部坐标解析接口，绘出脸部位置矩形
                    count = self.handle_similarity(face, img, img_gray, face_obj, count)
                cv2.imshow("FaceImg", img)
                if self.judge_user_success(self.current_name):
                    cv2.destroyAllWindows()
                    video.release()
                    return  f'识别成功, 识别出的用户为：{self.current_name}'
                elif time.time() - time_start >= 60:
                    cv2.destroyAllWindows()
                    video.release()
                    return f'{self.current_name}人脸识别失败!'
            else:
                cv2.destroyAllWindows()
                video.release()
                return '摄像头读取数据失败！'

    def handle_similarity(self, face, img, img_gray, face_obj, count):
        """ 处理图片相似度 """
        for x, y, w, h in face:
            # 接口参数:  被绘画的图片 起点位置 终点位置 边框颜色 边框宽度
            cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=1)
            # 从视频画面中截取前摄像头的脸部图片数据
            face_img = img_gray[y:y + h, x:x + w]
            # 处理当前脸部图片大小为200，与保存的人脸图片大小一致，方便后续判断相似度，
            face_img = cv2.resize(face_img, dsize=(200, 200))
        
            # 返回值为数组 表示为对应的图片 相似度
            result = face_obj.predict(face_img)
            
            # 获取对应的名称
            self.current_name = self.list_dir[result[0]]
            current_count = self.user_dict[self.current_name]
            print(f"\033[3;34m当前识别结果为: {self.current_name}, 总共为第：{count}次识别，识别正确：{current_count}次\033[m")
            # 判断相似度
            
            if result[1] < 2000:
                a1 = "error"
                cv2.putText(img, a1, (x, y), cv2.FONT_ITALIC, 1, [0, 0, 255], 2)
            else:
                cv2.putText(img, self.current_name, (x, y), cv2.FONT_ITALIC, 1, [0, 0, 255], 2)
                # 为当前识别出的用户次数 + 1
                self.user_dict[self.current_name] = self.user_dict.get(self.current_name) + 1
        count = self.user_dict[self.current_name]
        return count


    def judge_user_success(self, user_name):
        """ 判断用户成功次数 """
        for key, val in self.user_dict.items():
            if key == user_name:
                if val == 20:
                    return True
        return False

    def run(self):
        self.get_face_data()
        while True:
            result = self.check_face_data()
            print(result)
            flag = input("是否还要继续识别？ \n 请输入: 选项y/n")
            if flag == "n":
                break
            for key in self.user_dict.keys():
                self.user_dict[key] = 0


if __name__ == '__main__':
    face = FaceRecognition()
    face.run()
    

# 如果检测到底能不能识别不同的人，采集一个人的人脸图片 将程序运行  找另一个人进行人脸检测
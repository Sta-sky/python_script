import cv2
import os
import tqdm

"""

    环境:
        python版本：3.7.8
        依赖包：
            opencv-python == 4.5.5.62
            opencv-contrib-python == 4.5.5.62


    save_user_face:
        get_user:
            1、循环获取用户输入的用户名，对用户名做去重处理，
            2、给用户选择空间，让用户做后续是否再次录入处理
        
        save_face： 保存脸部信息功能
            1、打开摄像头
            2、循环采集摄像头数据
            3、调用cv2的CascadeClassifier读取训练好的头像轮廓xml文件haarcascade_frontalface_alt.xml
                将摄像头上的人脸坐标数据截取，
            4、将截取的图片保存本地，完成采集
            5、采集50个退出
    
    * 采集保存注意路径中不能含有中文字符
"""


class SaveUserFase(object):
    def __init__(self):
        # 用户名
        self.user_name = None
        # 图片保存路径
        self.load_face_path = f"{os.path.abspath('FaceImg')}/face/"
        
    def get_user(self):
        while True:
            user_name = input("请输入当前录入脸部信息的用户名: ")
            if os.path.exists(f"{self.load_face_path}{user_name}"):
                print('人脸信息已经存在，重新输入姓名！')
                continue
            flag = input(f"当前录入信息的用户名为: {user_name}'\n"
                  f"请确认当前用户名是否正确y/n：")
            
            if flag != 'y':
                print('===')
                continue
            self.user_name = user_name
            self.save_face()
            continue_flag = input(f'当前 {self.user_name} 人脸信息采集完成,\n'
                                  f'如须继续采集，请输入y，否则输入n结束采集：')
            if continue_flag == 'n':
                print("Bye!")
                break


    def save_face(self):
        # 打开摄像头
        video = cv2.VideoCapture(0)
        is_open = video.isOpened()
        if not is_open:
            print('打开摄像头失败...')
            raise
        # 设置保存路径
        if (not os.path.exists(self.load_face_path + self.user_name)):
            os.mkdir(self.load_face_path + self.user_name)
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
        count = 1
        is_break = False
        with tqdm.tqdm(total=50) as bar:
            while True:
                bar.set_description("当前采集进度为:")
                # 每个人脸采集五十个信息
                flag, video_img = video.read()
                faces = face_detector.detectMultiScale(video_img)
                if count > 50:
                    break
                for x, y, w, h in faces:
                    cv2.rectangle(video_img, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=2)
                    #  跟布局返回的数组 判断有没有标记到人脸有没有标记到，无则返回空元组
                    tip = "w:save   q:exit"
                    if is_break:
                        if not isinstance(faces, tuple): # 实例判断
                            # 只保存人脸，不是全部的当前帧的图片
                            face_photo = video_img[y:y + h, x:x + w]
                            # 图片尺寸转换
                            newImg = cv2.resize(face_photo, dsize=(200, 200), )
                            # 保存图片到本地
                            face_name_path = f"{self.load_face_path}{self.user_name}/{count}.jpg"
                            cv2.imwrite(face_name_path, newImg)
                            count += 1
                            bar.update(1)
                    else:
                        cv2.putText(video_img, tip, (20, 20), cv2.FONT_ITALIC, 1, [0, 0, 255], 2)
                # 显示图片
                cv2.imshow('get face info', video_img)
                index = cv2.waitKey(1000 // 24)
                if ord('w') == index:
                    is_break = True
                elif ord('q') == index:
                    break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    save_user_face_obj = SaveUserFase()
    save_user_face_obj.get_user()

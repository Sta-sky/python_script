import matplotlib.pyplot as plt
#from matplotlib import colors
import numpy as np
import jieba
from PIL import Image
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
data = open('./keywords.txt','r',encoding='utf-8').read()  #生成词云的文档，读取中文txt必须采用utf-8编码
cut_text = " ".join(jieba.cut(data))  #设置jieba分词，因原文本含有大量文字
background_Image = np.array(Image.open('panda2.png')) #设置指定图片
#image_colors=ImageColorGenerator(background_Image)
#color_list=['#3574C8','#295C97','#039FE8'] #设置指定字体颜色
#color_list=['#66CCCC'] #设置指定字体颜色
#color_map=colors.ListedColormap(color_list)
stopwords=set(STOPWORDS)  #过滤，设置停用词
stopwords.add("的")
stopwords.add("无")
stopwords.add("暂无")
stopwords.add("很好")
stopwords.add("好")
stopwords.add("是")
stopwords.add("多")
wordcloud = WordCloud(
        background_color = 'white', #背景颜色，根据图片背景设置，默认为黑色
        #background_color=None, mode="RGBA",
        mask = background_Image, #笼罩图
        #colormap=color_map,
        font_path = 'C:\Windows\Fonts\SIMLI.TTF',#若有中文需要设置才会显示中文
        stopwords=stopwords,
        max_font_size=300,
        max_words=2000,
        scale=8,
        random_state=42,
        #margin=2
        ).generate(cut_text)
#plt.imshow(wordcloud.recolor(color_func=image_colors),interpolation='bilinear')
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file(r'stateowned_wordcloud.jpg')

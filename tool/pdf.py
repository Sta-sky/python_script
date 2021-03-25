import os
import re

import html2text
import pdfkit
from markdown import markdown
from pymdownx import superfences

"""


1、将markdown文档转换为 pdf 
    1、先将markdown转换为 html格式
    2、将html格式转换为pdf，并写入本地
    3、读出本地的pdf文件，写入response中，返回前端下载

2、将markdown文件返回前端为markdown格式-----普通返回，会导致markdown格式不识别，很难看
    1、markdown转为html，
    2、再通过   html2text下的handle方法，转换为markdown格式
    3、将转换后返回的数据写入response中，返回前端
    
注 ： 
    html生成pdf中的img标签中的src地址不能为服务器地址，会报错

依赖包：    
    pip install python-markdown-math
    pip install markdown_checklist
    pip install pygments
    pip install pymdown-extensions
"""

class MarkdownPdf:
    def __init__(self):

        self.html = '''
            <!DOCTYPE html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
                    <title>文件下载</title>
                </head>
                <body>
                    <article class="markdown-body">
                        {}
                    </article>
                </body>
            </html>
            '''
        self.extensions = [
                'toc',  # 目录，[toc]
                'extra',  # 缩写词、属性列表、释义列表、围栏式代码块、脚注、在HTML的Markdown、表格
            ]
        self.third_party_extensions = [
                'mdx_math',  # KaTeX数学公式，$E=mc^2$和$$E=mc^2$$
                'markdown_checklist.extension',  # checklist，- [ ]和- [x]
                'pymdownx.magiclink',  # 自动转超链接，
                'pymdownx.caret',  # 上标下标，
                'pymdownx.superfences',  # 多种块功能允许嵌套，各种图表
                'pymdownx.betterem',  # 改善强调的处理(粗体和斜体)
                'pymdownx.mark',  # 亮色突出文本
                'pymdownx.highlight',  # 高亮显示代码
                'pymdownx.tasklist',  # 任务列表
                'pymdownx.tilde',  # 删除线
            ]
        self.extensions.extend(self.third_party_extensions)
        self.extension_configs = {
                'mdx_math': {
                    'enable_dollar_delimiter': True  # 允许单个$
                },
                'pymdownx.superfences': {
                    "custom_fences": [
                        {
                            'name': 'mermaid',  # 开启流程图等图
                            'class': 'mermaid',
                            'format': superfences.fence_div_format
                        }
                    ]
                },
                'pymdownx.highlight': {
                    'linenums': True,  # 显示行号
                    'linenums_style': 'pymdownx-inline'  # 代码和行号分开
                },
                'pymdownx.tasklist': {
                    'clickable_checkbox': True,  # 任务列表可点击
                }
            }

    def md_to_html(self, content):
        # MarkDown转HTML
        html_text = markdown(
            content, output_format='html', extensions=self.extensions, extension_configs=self.extension_configs)
        return html_text

    def html_to_pdf(self, texts, save_path):
        # HTML转PDF
        config = pdfkit.configuration(wkhtmltopdf=r"D:\soft_ware\htmltopdf\wkhtmltopdf\bin\wkhtmltopdf.exe")
        html = self.html.format(texts)
        pdfkit.from_string(html, save_path, options={'encoding': 'utf-8'}, configuration=config)

    @classmethod
    def html_to_markdown(cls, html_text):
        text_maker = html2text.HTML2Text()
        text_maker.bypass_tables = False
        markdown_text = text_maker.handle(html_text)
        return markdown_text


if __name__ == '__main__':
    to_obj = MarkdownPdf()
    with open('markdown笔记.md', 'r', encoding='utf-8') as fp:
        text = fp.read()
    md_content = to_obj.md_to_html(text)
    path_ = os.path.abspath('../') + '/test.pdf'
    to_obj.html_to_pdf(md_content, path_)

from PyPDF2 import PdfFileReader

pdf_document = "IgnitionSmartEqp_V202.pdf"

with open(pdf_document, "rb") as filehandle:
    pdf = PdfFileReader(filehandle)
    # 使用getDocumentInfo获取文档信息
    info = pdf.getDocumentInfo()
    # 使用getNumPages获取文档页数，页面从0开始计数
    pages = pdf.getNumPages()

    print (info)
    print ("number of pages: %i" % pages)
    for item in range(0, pages - 1):
        page1 = pdf.getPage(item)
        print(f"当前第{item}页")
        print(page1.extractText(), 'info')

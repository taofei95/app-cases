from pywebio import *
from pywebio.input import *
from pywebio.output import *
import requests
import time

def url_check(url):
    if url == '':
        return 'url不能为空'

def bmi():
    put_markdown("""
        # OFA-图像描述(英文)
        ## 图像描述是什么？
        如果你希望为一张图片配上一句文字，或者打个标签，OFA模型就是你的绝佳选择。你只需要输入任意1张图片的url或者上传本地的图片，就能快速收获一段精准的描述。本页面下方提供了在线体验的服务，欢迎使用！   
        """).style('display: block; margin-bottom:10px;')
    
    options = [
        {
            "label": '输入图片url',
            "value": 'web_image',
            "selected": True,
            "disabled": False,
        },
        {
            "label": '上传本地图片',
            "value": 'upload_image',
            "selected": False,
            "disabled": False,
        },
    ]
    selector = select('选择图片方式:', options=options, multiple=False)
    
    if selector == 'web_image':
        url = input("请输入图片的url:", type=URL, validate=url_check)
        put_image(url).style('height:400px; width:800px; margin-top:20px;')
        
        with put_loading(color='primary').style('width:4rem; height:4rem; display: block; margin:auto; margin-top:30px;'):
            res = requests.post(url='http://192.168.4.91:8080/web_image',
                    headers={"Content-Type": "application/json"},
                    json={"url": url})
            style([put_text(res.text)], 'margin-top:20px; font-size:20px;')
        
    else:
        f = file_upload(accept='image/*', placeholder='上传本地图片',
            multiple=False, max_size=0, required=True)
        put_image(f.get('content')).style('height:400px; width:800px; margin-top:30px;')
        
        with put_loading(color='primary').style('width:4rem; height:4rem; display: block; margin:auto; margin-top:30px;'):
            url = 'http://192.168.4.91:8080/upload_image'
            files = {'image': f.get('content')}
            data = {'name': f.get('filename')}
            res = requests.post(url, data, files=files)
            style([put_text(res.text)], 'margin-top:20px; font-size:30px;')

if __name__ == '__main__':
    start_server(bmi, port=12345)
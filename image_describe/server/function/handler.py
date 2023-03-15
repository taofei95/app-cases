import os
import uuid
import json
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

def handle_upload(event, context):
    files = event.files
    image = files.get('image')
    if 'image' not in files or image is None:
        return {
            'statusCode': 400,
            'body': 'missing image'
        }

    form = event.form
    name = form.get('name')
    if 'name' not in form or name == '':
        return {
            'statusCode': 400,
            'body': 'missing name'
        }

    image_root_path = '/image_tmp'
    if not os.path.exists(image_root_path):
        os.mkdir(image_root_path)

    prefix = uuid.uuid1()
    image_path = image_root_path + str(prefix) + '-' + name
    with open(image_path, 'wb') as f:
        f.write(image.stream.read())

    img_captioning = pipeline(Tasks.image_captioning, model='damo/ofa_image-caption_coco_distilled_en', model_revision='v1.0.1')
    result = img_captioning(image_path)

    os.remove(image_path)

    return {
        'statusCode': 200,
        'body': result[OutputKeys.CAPTION]
    }

def handle_web(event, context):
    body = json.loads(event.body.decode('utf-8'))
    url = body.get('url')
    if 'url' not in body or url == '':
        return {
            'statusCode': 400,
            'body': 'missing url'
        }

    img_captioning = pipeline(Tasks.image_captioning, model='damo/ofa_image-caption_coco_distilled_en', model_revision='v1.0.1')
    result = img_captioning(url)

    return {
        'statusCode': 200,
        'body': result[OutputKeys.CAPTION]
    }
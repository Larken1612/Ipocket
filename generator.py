import asyncio, json
from serpapi import GoogleSearch
import requests
import openai
import shutil
import json
import sys
import cv2
import re
import os

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog

sys.stdout.reconfigure(encoding='utf-8')

OPEN_AI_API_KEY = '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'
GOOGLE_SEARCH_API_KEY = '61383337ca1a73267283eb31ec1680673acfaf3cec648c21fcdf2e31ce112342'
openai.api_key = OPEN_AI_API_KEY

jsonInputFilePath = './input.json'
jsonOutputFilePath = './information.js'

print("it worked")

class Prompt:
    def __init__(self, top=None, which_top=None):
        self.top = top
        self.which_top = which_top

    def generate_prompt(self):
        return 'Hãy cho tôi biết {} {} kèm với mô tả chi tiết dài khoảng 250-300 từ của chúng dưới dạng một mảng chứa các kiểu json với các thuộc tính như sau: "item": (tên), "category": (viết phân loại tìm kiếm vào đây, chỉ theo 1 phân loại duy nhất, có các phân loại Địa điểm, Động vật, Dụng cụ, Sản phẩm, Dịch vụ, Người nổi tiếng, Sự kiện, Âm nhạc, Công nghệ, Thể thao, Món ăn, Công thức nấu ăn, Trò chơi, Kỹ năng, Câu chuyện, Phim ảnh, Sách, Lịch sử, Văn hóa, Sức khỏe, Làm đẹp), "description": (mô tả). Chỉ trả về mảng, không viết viết thêm bất cứ thứ gì khác và trả lời bằng tiếng Việt.'.format(self.top, self.which_top)

class ObjectDetector:
    def __init__(self):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
        self.cfg.MODEL.DEVICE = "cpu" 

        self.detector = DefaultPredictor(self.cfg)

    def predict(self, image_path):
        image = cv2.imread(image_path)
        confidence_threshold = 0.85

        predictions = self.detector(image)
        instances = predictions["instances"]

        class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).get("thing_classes")

        entities = [class_names[pred_class] for pred_class, pred_score in zip(instances.pred_classes, instances.scores) if pred_score > confidence_threshold]

        return entities
    
class ResponseGenerator:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.detector = ObjectDetector()

    def generate_response(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.prompt}
            ]
        )
                                          
        response = completion.choices[0].message['content']
        print(type(response))
        print(response)
        try:
            response = json.loads(response)
        except json.decoder.JSONDecodeError:
            print('Data is not a valid JSON string')

        items = [str(item['category']+ " " + item['item']) for item in response]

        print('Done top list')
        
        # for i in range(len(items)):
        #     while True:
        #         try:
        #             image = self.image_select(items[i])
        #             response[i]['image'] = image

        #             print('Done', items[i])
        #             break
            
        #         except:
        #             print('Error at', items[i])
        #             continue
        return response
    
    # def image_select(self, item):
    #     download_folder = 'downloads'

    #     if os.path.exists(download_folder):
    #         shutil.rmtree(download_folder)

    #     os.makedirs(download_folder)

    #     image_search = GoogleSearch({"q": item, "engine": "google_images", "ijn": "0", "api_key": GOOGLE_SEARCH_API_KEY})

    #     images_results = image_search.get_dict()["images_results"]
    #     images_results = list(filter(lambda image: (str(image['original']).split('.')[-1] in ['jpg', 'png', 'jpeg']), images_results))
    #     images_results = list(filter(lambda image: image['original_width'] >= image['original_height'], images_results))
    #     images_results = list(filter(lambda image: image['original_width'] >= 860, images_results))
    #     images_results = list(filter(lambda image: image['original_height'] >= 720, images_results))
    #     images_results = list(filter(lambda image: image['is_product'] is False, images_results))

    #     images_links = [result['original'] for result in images_results]
    #     original = ''

    #     for index, link in enumerate(images_links):
    #         try:
    #             image_name = image_name = str(index) + '.jpg'
    #             image_path = os.path.join(download_folder, image_name)

    #             response = requests.get(link, timeout=5)
    #             response.raise_for_status()
                
    #             with open(image_path, 'wb') as file:
    #                 file.write(response.content)

    #             print(f"Tải xuống thành công: {image_name}")

    #             entities = self.detector.predict(image_path)

    #             try:
    #                 if 'person' not in entities:
    #                     original = link
    #                     break

    #             except:
    #                 print(image_name)
    #         except Exception as e:
    #             print(f"Lỗi khi tải xuống {link}: {str(e)}")

    #     shutil.rmtree(download_folder)
    #     return original

        # for image in os.listdir(download_folder):
        #     try:
        #         image_path = os.path.join(download_folder, image)
        #         entities = self.detector.predict(image_path)

        #         if 'person' not in entities:
        #             trustworthy_images.append(image.split('.')[0])
            
        #     except:
        #         print(image)

        # images = [images_results[int(index)] for index in trustworthy_images]
        # image = max(images, key=lambda image: image['original_width'] * image['original_height'])
    
async def getResponse():
    with open(jsonInputFilePath, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    top = int(json_data['top'])
    req = json_data['request']

    print(top, req)

    prompt = Prompt(top, req)

    response_generator = ResponseGenerator(prompt=prompt.generate_prompt())
    response = response_generator.generate_response()
    return response

async def writeInfo():
    response = await getResponse()

    infor = []

    for i in range(0, len(response)):
        infor.append({"item": response[i]['item'],
                    "description": response[i]['description'],
                    # "image": response[i]['image']
                    })

    infor_to_file = "export const infor = " + str(infor)

    with open(jsonOutputFilePath, "w", encoding="utf-8") as file:
        file.write(infor_to_file)

asyncio.run(writeInfo())
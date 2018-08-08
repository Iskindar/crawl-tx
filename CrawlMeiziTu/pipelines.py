# -*- coding: utf-8 -*-
import os
import requests
from CrawlMeiziTu.settings import IMAGES_STORE

class CrawlmeizituPipeline(object):

    def process_item(self, item, spider):
        fold_name = "".join(item['title'])
        header = {
            'USER-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': 'UM_distinctid=16496fb29e3b2-0594917d89bd28-3c604504-1fa400-16496fb29e40',
            #需要查看图片的cookie信息，否则下载的图片无法查看
        }
        images = []
        # 所有图片放在一个文件夹下
        dir_path = '{}'.format(IMAGES_STORE)
        if not os.path.exists(dir_path) and len(item['src']) != 0:
            os.mkdir(dir_path)
        if len(item['src']) == 0:
            with open('..//check.txt', 'a+') as fp:
                fp.write("".join(item['title']) + ":" + "".join(item['url']))
                fp.write("\n")

        for jpg_url, name, num in zip(item['src'], item['alt'],range(0,100)):
            file_name = name + str(num)
            file_path = '{}//{}'.format(dir_path, file_name)
            images.append(file_path)
            if os.path.exists(file_path) or os.path.exists(file_name):
                continue

            with open('{}//{}.jpg'.format(dir_path, file_name), 'wb') as f:
                req = requests.get(jpg_url, headers=header)
                f.write(req.content)

        return item
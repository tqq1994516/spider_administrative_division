# useful for handling different item types with a single interface
import codecs
import json
import os

import attr
import MySQLdb
from MySQLdb.cursors import DictCursor


class SpiderAdministrativeDivisionPipeline:
    def __init__(self):
        # 连接数据库,使用mysqlclient库链接
        self.connect = MySQLdb.connect(
            host='192.168.136.128',
            port=3306,
            user='root',
            passwd='123456',
            db='house_helper',
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor  # 设置为json格式返回
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        item_str = json.dumps(attr.asdict(item), ensure_ascii=False)
        item_json = json.loads(item_str)
        for i in range(len(item_json['area_name'])):
            try:
                self.cursor.execute('''select * from administrative_division where area_id=%s''',
                                    (item_json['area_id'][i],))
                data = self.cursor.fetchone()
                if data is None:
                    self.cursor.execute(
                        '''insert into administrative_division(area_id, area_name, hierarchy, higher_id) value (%s, %s, %s, %s)''',
                        (item_json['area_id'][i], item_json['area_name'][i], item_json['hierarchy'],
                         item_json['higher_id'],))
                    self.connect.commit()
                elif data['area_name'] == item['area_id'][i]:
                    return item
                else:
                    self.cursor.execute(
                        '''update administrative_division set area_name=%s, hierarchy=%s, higher_id=%s where area_id=%s''',
                        (item_json['area_name'][i], item_json['hierarchy'], item_json['higher_id'], item_json['area_id'][i],))
                    self.connect.commit()
            except Exception as e:
                print(e)
                # 发生错误时回滚
                self.connect.rollback()
        return item  # 必须实现返回

    def close_spider(self, spider):
        # 关闭数据库
        self.connect.close()

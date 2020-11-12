# coding:utf8
import os
import time
from os import walk
import csv
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticObj:
    def __init__(self, index_name, index_type, ip="127.0.0.1"):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        # self.es = Elasticsearch([ip])
        # 用户名密码状态
        self.es = Elasticsearch([ip], http_auth=('elastic', 'password'),
                                port=9200)

    def create_index(self, index_name="ott", index_type="ott_type"):
        _index_mappings = {
            "mappings": {
                "properties": {
                    "id": {
                        "type": "short"
                    },
                    "title": {
                        "type": "text",
                        "index": True
                    },
                    "date": {
                        "type": "date",
                        "index": True,
                    },
                    "keyword": {
                        "type": "text",
                        "index": True
                    },
                    "source": {
                        "type": "keyword",
                        "index": True
                    },
                    "link": {
                        "type": "text",
                        "index": True
                    }
                }
            }
        }
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        result = self.es.indices.exists(index=self.index_name)
        print(result)
        if not result:
            res = self.es.indices.create(index=self.index_name,
                                         body=_index_mappings)
            print(res)
        else:
            print('索引已经存在，')


    def IndexData(self):
        """
        从csv目录上的文件中，读取全部csv文件，
        :return:
        """
        csvdir = 'D:/work/ElasticSearch/exportExcels'
        filenamelist = []

        # 读取当前目录 {csvdir} 以及子目录下  所有的csv文件
        for (dirpath, dirnames, filenames) in walk(csvdir):
            filenamelist.extend(filenames)
            break
        total = 0
        for file in filenamelist:
            csvfile = csvdir + '/' + file
            self.Index_Data_FromCSV(csvfile)
            total += 1
            print(total)
            time.sleep(10)

    def Index_Data_FromCSV(self, csvfile):
        '''
        从CSV文件中读取数据，并存储到es中
        :param csvfile: csv文件，包括完整路径
        :return:
        '''
        s = csv.excel()
        list = s.quoting(csvfile)
        index = 0
        doc = {}
        for item in list:
            if index > 1:  # 第一行是标题
                doc['title'] = item[0]
                doc['link'] = item[1]
                doc['date'] = item[2]
                doc['source'] = item[3]
                doc['keyword'] = item[4]
                res = self.es.index(index=self.index_name, body=doc)
                print(res['created'])
            index += 1
            print(index)

    def Index_Data(self):
        '''
        创建或者更新文档
        :return:
        '''
        list = [
            {"date": "2017-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "title": "付费 电视 行业面临的转型和挑战"
             },
            {"date": "2017-09-13",
             "source": "中国文明网",
             "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
             "keyword": "电视",
             "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             }
        ]
        id_base = 1
        for item in list:
            res = self.es.index(
                index="test_ni", id=id_base, doc_type='mode', body=item)
            filed_result = res['_shards']['failed']
            id_base += 1
            if not filed_result:
                print('创建成功，')

    def bulk_Index_Data(self):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        list = [
            {"date": "2016-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "title": "付费 电视 行业面临的转型和挑战",
             "id": 1
             },
            {"date": "2015-09-13",
             "source": "中国文明网",
             "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
             "keyword": "电视",
             "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心",
             "id": 2
             },
            {"date": "2014-09-13",
             "source": "人民电视",
             "link": "http://tv.people.com.cn/BIG5/n1/2017/0913/c67816-29533981.html",
             "keyword": "电视",
             "title": "中国第21批赴刚果（金）维和部隊启程--人民 电视 --人民网",
             "id": 3
             },
            {"date": "2013-09-13",
             "source": "站长之家",
             "link": "http://www.chinaz.com/news/2017/0913/804263.shtml",
             "keyword": "电视",
             "title": "电视 盒子 哪个牌子好？ 吐血奉献三大选购秘笈",
             "id": 4
             }
        ]
        ACTIONS = []
        i = 1
        for line in list:
            action = {
                "_index": self.index_name,
                "_id": i,  # _id 也可以默认生成，不赋值
                "_source": {
                    "date": line['date'],
                    "source": line['source'],
                    "link": line['link'],
                    "keyword": line['keyword'],
                    "title": line['title'],
                    "id": line['id']}
            }
            i += 1
            ACTIONS.append(action)
            # 批量处理
        success, _ = bulk(self.es, ACTIONS, index=self.index_name,
                          raise_on_error=True)
        print('Performed %d actions' % success)

    def Delete_Index_Data(self, id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, id=id)
        print(res)

    def parse_get_result_and_print(self, result):
        if result and result['found']:
            print(result['_source']['date'], result['_source']['source'],
                  result['_source']['link'], result['_source']['keyword'],
                  result['_source']['title'])
        else:
            print('查询失败')

    def parse_search_result_and_print(self, result):
        fileds = result['_shards']['failed']
        if fileds:
            print(f'查询有失败,失败个数为{fileds}个')
        res_list = result['hits']['hits']
        for data in res_list:
            print(data)

    def query_id_doc_info(self, id):
        res = self.es.get(index=self.index_name, id=id)
        # # 输出查询到的结果
        self.parse_get_result_and_print(res)

    def query_term_doc_info(self, keyword):
        """
        term keyword必须等于字段的值， 全匹配
        :param keyword:
        :return:
        """
        body = {
            "query": {
                "term": {
                    'source': keyword
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_get_terms_doc_info(self, keyword1, keyword2):
        """
        全匹配文档字段中的多个值，如下：
            匹配source 的名为keyword1，keyword2的值
        :param keyword1:
        :param keyword2:
        :return:
        """
        body = {
            "query": {
                "terms": {
                    "source": [
                        keyword1, keyword2
                    ]
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_bool_doc_info(self):
        """
        复合查询
        bool有3类查询关系，must(都满足),should(其中一个满足),must_not(都不满足）
        经测试must 好像不能在bool中作为条件了，不确定，待定
        :return:
        """
        body = {
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "term": {
                                "source": "慧聪网"
                            }
                        },
                        {
                            "term": {
                                "date": "2016-09-13"
                            }
                        }
                    ]
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_cut_slic_doc_info(self):
        """
        切片查询
        :return:
        """
        body = {
            "query": {
                "match_all": {}
            },
            "from": 2,  # 从第二条数据开始
            "size": 4,  # 获取4条数据
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_range_scope_doc_info(self):
        """
        根据运算符号查询
        """
        body = {
            "query": {
                "range": {
                    "date": {
                        "gte": "2014-12-05",    # 大于这个日期
                        "lte": "2016-10-09"     # 小于这个日期
                    }
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_re_doc_info(self):
        """
        根据re通配来查询 文档对应字段中包含需要匹配的值
        :return:
        """
        body = {
            "query": {
                "wildcard": {
                    "title": "*电*"
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_prefix_doc_info(self):
        """
        查询 source字段前缀为 “中”的文档信息
        :return:
        """
        body = {
            "query": {
                "prefix": {
                    "source": "中"
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_doc_totle_count(self):
        res = self.es.count(index=self.index_name)
        print(res['count'])

    def query_match_doc_info(self):
        """
        查询出对应字段包含关键字的文档信息
        :return:
        """
        body = {
            "query": {
                "match": {
                    "人民电视": "人民"
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_multi_match_doc_info(self):
        """
        多个字段中查询包含关键字的文档信息，用列表形式表示
        :return:
        """
        body = {
            "query": {
                "multi_match": {
                    "query": "人",
                    "fields": ['source', 'title']
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)

    def query_order_doc_info(self):
        """
        排序查询  文本类型不支持，会报错
        :return:
        """
        body = {
            "query": {
                "match_all": {}
            },
            "sort": {
                "id": {               # 根据日期排序
                    "order": "desc"      # asc升序， desc降序
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        self.parse_search_result_and_print(res)


if __name__ == '__main__':
    obj = ElasticObj("dangyy", "ott_type", ip="127.0.0.1")

    # TODO 创建索引库，生成数据
    # 创建索，文档，定义文档字段查询方式这种映射方式，
    # 6.X版本后，不支持自定义类型，默认生成 _doc类型
    # obj.create_index()

    # 可以创建索引库，批量插入数据
    # obj.bulk_Index_Data()

    # 可以创建索引库， 循环一条一条插入数据
    # obj.Index_Data()

    # TODO csv 文件操作
    # 从指定目录下，读取全部csv文件，写入elsticsearch中
    # obj.IndexData()

    # 从csv中读取数据，插入elastcisearch中
    # obj.Index_Data_FromCSV(csvfile)

    # TODO 查询数据
    # 根据文档id查询信息
    # obj.query_id_doc_info(2)

    # 等于查询，term与terms[查询出多个],
    # obj.query_term_doc_info('www')
    # obj.query_terms_doc_info('慧聪网', '中国文明网')

    # 条件查询,should(其中一个满足),must_not(都不满足)
    # obj.query_bool_doc_info()

    # 切片查询
    # obj.query_cut_slic_doc_info()

    # 范围查询
    # obj.query_range_scope_doc_info()

    # 通配查询
    # obj.query_re_doc_info()

    # 前缀查询
    # obj.query_prefix_doc_info()

    # 查询所有文档的数量
    # obj.query_doc_totle_count()

    # match 查询字段字段包含关键字的文档信息
    # obj.query_match_doc_info()

    # 多个字段中查询包含关键字的文档信息
    # obj.query_multi_match_doc_info()

    # 排序查询,
    # obj.query_order_doc_info()

    # TODO 删除数据
    # 通过id 删除索引中的一条文档
    # obj.Delete_Index_Data(1)





import pymongo
import redis
import json
def main():
    redis_conn = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    mongo_coon = pymongo.MongoClient(host='127.0.0.1', port=27017)
    while True:
        soure,data=redis_conn.blpop(['jdredis:items'])
        item=json.loads(data)
        db_name=item['db']
        collection_name=db_name
        db = mongo_coon[db_name]
        collection = db[collection_name]
        collection.save(item)



if __name__ == '__main__':
    main()
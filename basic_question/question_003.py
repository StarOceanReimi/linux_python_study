#!/usr/bin/python
import redis, question_001 as pcode_gen

dbconfig = dict(host='localhost', port=6379, db=0)

def save_promo(remark):
    r = redis.StrictRedis(**dbconfig)
    r.delete(remark)
    pcg = pcode_gen.PromoCodeGenerator(200, 20)
    codes = pcg.get_codes()
    for code in codes:
        r.rpush(remark, code)
    r.save()
    print 'Promotion Coded Saved!'

if __name__ == '__main__':
    save_promo('old_customer_10_discount')

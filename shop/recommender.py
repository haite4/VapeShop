import redis
from django.conf import settings
from shop.models import Product


r = redis.StrictRedis(
    port=settings.REDIS_PORT,
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB
)


#

class Recommender:


    def get_product_id(self, id):
        return f"product:{id} purchased_with"
    


    
    def product_bought(self, products):
        
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            print(product_id)
            for with_id in products_ids:
                if product_id != with_id:
                    result  = r.zincrby(self.get_product_id(product_id),
                                    1,
                                with_id
                              )
                    
    def suggest_product_for(self,product, max_result=6):
        products_ids = [p.id for p in product]
        if products_ids:

            
            if len(product) == 1:
                suggestions = r.zrange(
                    self.get_product_id(products_ids[0]),
                    0, -1 , desc=True
                )[:max_result]

            else:
                flat_ids = "".join([str(id) for id in products_ids])
                tmp_key = f"tmp_{flat_ids}"
                keys = [self.get_product_id(id) for id in products_ids]
                r.zunionstore(tmp_key, keys)
                r.zrem(tmp_key, *products_ids)
                suggestions = r.zrange(tmp_key, 0, -1 , desc=True)[:max_result]
                r.delete(tmp_key)

            suggestions_ids  = [int(id) for id in suggestions]
            product_suggestions = list(Product.objects.filter(id__in=suggestions_ids))
            product_suggestions.sort(key=lambda x: suggestions_ids.index(x.id))
            
            return product_suggestions




    def clear_purchases(self):
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_id(id))

            


    
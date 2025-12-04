from celery import shared_task
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.product.models import Product



@shared_task
def calculate_similar_products () : 
    products = Product.objects.all()
    product_tags = {}
    
    for product in products : 
        tag = ""
        tag = tag + product.title + " "
        if product.brand : 
            tag = tag + product.brand.name + " "
        if product.category : 
            tag = tag + product.category.title + " "
        for feature in product.product_features.all() : 
            tag = tag + f"{feature.key} {feature.value}"
        product_tags[product.id] = tag

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(product_tags.values())
    similarity = cosine_similarity(tfidf_matrix)

    for index,product_id in enumerate(product_tags) :
        distances = sorted(enumerate(similarity[index]),reverse=True,key=lambda x : x[1])[1:6]
        try : 
            product = Product.objects.get(id=product_id)
        except : 
            pass
        similar_products = []
        for i,score in distances : 
            similar_product_id = list(product_tags.keys())[i]
            try : 
                p = Product.objects.get(id=similar_product_id)
                similar_products.append(p)
            except : pass 
        product.similar_products.set(similar_products)


    

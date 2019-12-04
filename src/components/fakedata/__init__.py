from src.models.user import db, User, OAuth, Token, Order, Order_item, Order_status_id
from src.models.product import Product, Inventory, Inventory_item, Rating, rating_count, Category, Store
from src.models.trading import Shipment, Invoice, Invoice_status, Payment
import random

from flask import Blueprint , render_template, jsonify

fakedata_blueprint = Blueprint('fakebp', __name__)

categories = [
    'fruits', 'vegetables', 'seasoning'
]

inventories = ['District 7', 'Thu Duc district']

i_i = [
    {
        "stock": 62,
        "time": "2019/12/31",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 57,
        "time": "2019/12/28",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 64,
        "time": "2019/12/28",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 70,
        "time": "2019/12/15",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 52,
        "time": "2019/12/21",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 89,
        "time": "2019/12/31",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 76,
        "time": "2019/12/30",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 92,
        "time": "2019/12/19",
        "expired_date": "2020/01/12"
    },
    {
        "stock": 82,
        "time": "2019/12/22",
        "expired_date": "2020/01/11"
    },
    {
        "stock": 55,
        "time": "2019/12/18",
        "expired_date": "2020/01/20"
    },
    {
        "stock": 62,
        "time": "2019/12/23",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 58,
        "time": "2019/12/28",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 60,
        "time": "2019/12/16",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 90,
        "time": "2019/12/21",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 68,
        "time": "2019/12/28",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 54,
        "time": "2019/12/20",
        "expired_date": "2020/01/20"
    },
    {
        "stock": 68,
        "time": "2019/12/30",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 60,
        "time": "2019/12/18",
        "expired_date": "2020/01/10"
    },
    {
        "stock": 70,
        "time": "2019/12/18",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 75,
        "time": "2019/12/29",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 79,
        "time": "2019/12/20",
        "expired_date": "2020/01/12"
    },
    {
        "stock": 81,
        "time": "2019/12/23",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 55,
        "time": "2019/12/28",
        "expired_date": "2020/01/11"
    },
    {
        "stock": 63,
        "time": "2019/12/19",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 71,
        "time": "2019/12/27",
        "expired_date": "2020/01/20"
    },
    {
        "stock": 64,
        "time": "2019/12/27",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 88,
        "time": "2019/12/31",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 59,
        "time": "2019/12/24",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 59,
        "time": "2019/12/21",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 78,
        "time": "2019/12/25",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 75,
        "time": "2019/12/29",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 88,
        "time": "2019/12/16",
        "expired_date": "2020/01/07"
    },
    {
        "stock": 95,
        "time": "2019/12/28",
        "expired_date": "2020/01/10"
    },
    {
        "stock": 93,
        "time": "2019/12/29",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 83,
        "time": "2019/12/26",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 75,
        "time": "2019/12/24",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 64,
        "time": "2019/12/19",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 74,
        "time": "2019/12/23",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 86,
        "time": "2019/12/27",
        "expired_date": "2020/01/12"
    },
    {
        "stock": 68,
        "time": "2019/12/28",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 60,
        "time": "2019/12/17",
        "expired_date": "2020/01/12"
    },
    {
        "stock": 86,
        "time": "2019/12/24",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 73,
        "time": "2019/12/31",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 70,
        "time": "2019/12/26",
        "expired_date": "2020/01/14"
    },
    {
        "stock": 80,
        "time": "2019/12/16",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 77,
        "time": "2019/12/27",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 100,
        "time": "2019/12/17",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 85,
        "time": "2019/12/17",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 69,
        "time": "2019/12/21",
        "expired_date": "2020/01/07"
    },
    {
        "stock": 67,
        "time": "2019/12/21",
        "expired_date": "2020/01/10"
    },
    {
        "stock": 75,
        "time": "2019/12/25",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 50,
        "time": "2019/12/31",
        "expired_date": "2020/01/19"
    },
    {
        "stock": 65,
        "time": "2019/12/18",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 84,
        "time": "2019/12/24",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 91,
        "time": "2019/12/19",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 67,
        "time": "2019/12/15",
        "expired_date": "2020/01/20"
    },
    {
        "stock": 78,
        "time": "2019/12/19",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 94,
        "time": "2019/12/26",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 55,
        "time": "2019/12/31",
        "expired_date": "2020/01/14"
    },
    {
        "stock": 94,
        "time": "2019/12/30",
        "expired_date": "2020/01/19"
    },
    {
        "stock": 94,
        "time": "2019/12/28",
        "expired_date": "2020/01/11"
    },
    {
        "stock": 73,
        "time": "2019/12/31",
        "expired_date": "2020/01/17"
    },
    {
        "stock": 71,
        "time": "2019/12/27",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 81,
        "time": "2019/12/31",
        "expired_date": "2020/01/12"
    },
    {
        "stock": 54,
        "time": "2019/12/18",
        "expired_date": "2020/01/15"
    },
    {
        "stock": 100,
        "time": "2019/12/31",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 64,
        "time": "2019/12/15",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 70,
        "time": "2019/12/16",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 78,
        "time": "2019/12/24",
        "expired_date": "2020/01/13"
    },
    {
        "stock": 78,
        "time": "2019/12/24",
        "expired_date": "2020/01/05"
    },
    {
        "stock": 88,
        "time": "2019/12/26",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 52,
        "time": "2019/12/31",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 83,
        "time": "2019/12/23",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 91,
        "time": "2019/12/27",
        "expired_date": "2020/01/10"
    },
    {
        "stock": 57,
        "time": "2019/12/30",
        "expired_date": "2020/01/10"
    },
    {
        "stock": 50,
        "time": "2019/12/15",
        "expired_date": "2020/01/11"
    },
    {
        "stock": 50,
        "time": "2019/12/25",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 65,
        "time": "2019/12/23",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 51,
        "time": "2019/12/26",
        "expired_date": "2020/01/14"
    },
    {
        "stock": 71,
        "time": "2019/12/20",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 64,
        "time": "2019/12/17",
        "expired_date": "2020/01/11"
    },
    {
        "stock": 83,
        "time": "2019/12/18",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 83,
        "time": "2019/12/21",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 93,
        "time": "2019/12/29",
        "expired_date": "2020/01/19"
    },
    {
        "stock": 57,
        "time": "2019/12/18",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 93,
        "time": "2019/12/24",
        "expired_date": "2020/01/16"
    },
    {
        "stock": 64,
        "time": "2019/12/18",
        "expired_date": "2020/01/07"
    },
    {
        "stock": 88,
        "time": "2019/12/17",
        "expired_date": "2020/01/20"
    },
    {
        "stock": 52,
        "time": "2019/12/27",
        "expired_date": "2020/01/18"
    },
    {
        "stock": 79,
        "time": "2019/12/20",
        "expired_date": "2020/01/08"
    },
    {
        "stock": 70,
        "time": "2019/12/18",
        "expired_date": "2020/01/09"
    },
    {
        "stock": 73,
        "time": "2019/12/15",
        "expired_date": "2020/01/06"
    },
    {
        "stock": 83,
        "time": "2019/12/28",
        "expired_date": "2020/01/19"
    },
    {
        "stock": 95,
        "time": "2019/12/26",
        "expired_date": "2020/01/14"
    },
    {
        "stock": 63,
        "time": "2019/12/24",
                "expired_date": "2020/01/11"
    },
    {
        "stock": 55,
        "time": "2019/12/21",
                "expired_date": "2020/01/14"
    },
    {
        "stock": 73,
        "time": "2019/12/23",
                "expired_date": "2020/01/18"
    },
    {
        "stock": 75,
        "time": "2019/12/22",
                "expired_date": "2020/01/10"
    },
    {
        "stock": 91,
        "time": "2019/12/20",
                "expired_date": "2020/01/18"
    },
    {
        "stock": 100,
        "time": "2019/12/25",
                "expired_date": "2020/01/16"
    }
]

fruit_product = [['Apple', 'https://www.walmart.ca/en/ip/apple-gala/6000195494284', 'gam'], ['Avocado', 'https://images.eatsmarter.de/sites/default/files/styles/576x432/public/avocado-fotolia-600x450.jpg', 'gam'], ['Banana', 'http://buyfv.com/wp-content/uploads/2019/01/10000025-2_3-fresho-banana-robusta.jpg', 'gam'], ['Coconut', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVMEklVSrhnZTPMcMz8t4d5x-NGLFDBZ703bFG6r_sDKntyn9w&s', 'unit'], ['Grape', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROfRR0dudAEg7DFfMoRQom_kXXrrTsw8FgWVHbhKR60Nf2oMAUiw&s', 'gam'], ['Mango', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSz6jtchGZGiR38Cj8FdzywopoMSiyo7gJON8J2FmYdxTsrUEbb&s', 'gam'],
                 ['Orange', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToBnHvC2lea0nC8LecgwotZiI7RhCFJsTv0JKPttLzLQvFdFF7&s', 'gam'], ['Dragon fruit', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFxguw9NULcOIKmSUUMP4a9uQos0xmanvo4QPI2BRb3YdfMJ8nZQ&s', 'gam'], ['Watermelon', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkL4UyUjb81Ecw4Z1SDA-JFV9oe2zgxlv4_99VBERkvWichiUz&s', 'gam'], ['Pineaple', 'https://i5.walmartimages.com/asr/dd2a5d3c-d358-4579-8ece-59ce1804ab5b_9.0b874251fccc645fd98ac76e797c2d2a.jpeg?odnWidth=450&odnHeight=450&odnBg=ffffff', 'gam'], ['Papayya', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaqNWeGRhl-m7m0KmYxmOxncf3lWA8tNe2Tzd-o_zBXn4PxsaCAA&s', 'gam']]

vegetable_product = [['Bell pepper', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrcDPSIQqP1Uo1lK7GUlYRSpCf1edmQtEGGEJ5ay4QbAdQObwIDQ&s', 'gam'], ['Cauliflower', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOGNxkCVGuTZ2-E7L4WnidWPbZT63F6fKKblotH7n5H8F8GUY&s', 'gam'], ['Cabbage', 'https://pcdn.columbian.com/wp-content/uploads/2019/08/0830_met_cabbage-1226x0-c-default.jpg', 'gam'], ['Carrot', 'https://i5.walmartimages.ca/images/Enlarge/271/747/6000191271747.jpg', 'gam'], ['Cucumber',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzFuperqiyoF-6b2Vz6FWv0wndZ9jFdkABGLbnD_xvOPr3tBqRdA&s', 'gam'], ['Tomato', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnNWU9oih_G799tg1sc41vK5VGroGcK4XmudN2Zi_OTxZs6jIBGA&s', 'gam'], ['Pumpkin', 'https://www.duluthnewstribune.com/incoming/4684986-wtscwa-pumpkin-web.jpg/alternates/BASE_LANDSCAPE/pumpkin%20web.jpg', 'gam'], ['Green bean', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEBESKVXPO9nYPU8cwLGqjaNKBpHcobcSdVEjxeD1UYXWQhMgUiA&s', 'gam']]

seasoning_product = [['Onion', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6LOWhat5UFSjK3YcU-hCyC2A6b8sSZf3g0taMFPTT2vBZAgy6&s', 'gam'], ['Garlic', 'https://www.basketbazzar.com/wp-content/uploads/2019/05/Garlic.jpg', 'gam'], ['Turmeric', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9H01mkElD1fKidz9sOUqhDPSdrCGNY5DINkQ1Ls_4Kmlri0plzg&s', 'gam'],
                     ['Green onion', 'https://cdn.shopify.com/s/files/1/0135/9839/2378/products/Grreen_Onion_Bulb_800x560.png?v=1558314353', 'gam'], ['Pepper', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQB7vIiFa02_CsFtZreVdTJsijjy5Hf_wiD1NB6NqS4sUBZG9aRWg&s', 'gam']]

product_description = [
    {
        "name": "in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus vivamus vestibulum sagittis"
    },
    {
        "name": "adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae"
    },
    {
        "name": "eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in"
    },
    {
        "name": "leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut at dolor quis odio consequat varius integer ac leo"
    },
    {
        "name": "imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque"
    },
    {
        "name": "velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia"
    },
    {
        "name": "mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl"
    },
    {
        "name": "faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus sed vestibulum"
    },
    {
        "name": "metus sapien ut nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus"
    },
    {
        "name": "nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia"
    }
]

store_name = [
    {
        "name": "Mynte"
    },
    {
        "name": "Quimba"
    },
    {
        "name": "Jayo"
    },
    {
        "name": "Meezzy"
    },
    {
        "name": "Jazzy"
    },
    {
        "name": "Rhyloo"
    },
    {
        "name": "Yombu"
    },
    {
        "name": "Eazzy"
    },
    {
        "name": "Realblab"
    },
    {
        "name": "Ozu"
    }
]

@fakedata_blueprint.route('/')
def craete_fake_date():
    # for el in categories:
    #     new_cate = Category(body=el)
    #     db.session.add(new_cate)
    #     db.session.commit()

    # for el in inventories:
    #     new_i = Inventory(location=el)
    #     db.session.add(new_i)
    #     db.session.commit()

    # for store in store_name:
    #     new_store = Store(name=store['name'])
    #     db.session.add(new_store)
    #     db.session.commit()

    # for el in i_i:
    #     new_II = Inventory_item(inventory_id=random.randint(
    #         1, 2), store_id=random.randint(1, 10), stock=el['stock'], time=el['time'], expired_date=el['expired_date'])
    #     db.session.add(new_II)
    #     db.session.commit()

    # for x in range(0, 30):
    #     ran = random.randint(0, 10)
    #     ran_price = random.randint(1, 5)*1000
    #     new_product = Product(name=fruit_product[ran][0], discription=product_description[random.randint(
    #         0, 9)]['name'], img_url=fruit_product[ran][1], price=ran_price, inventory_item_id=random.randint(1, 99), category_id=1)
    #     db.session.add(new_product)
    #     db.session.commit()

    # for x in range(0, 30):
    #     ran = random.randint(0, 7)
    #     ran_price = random.randint(1, 5)*1000
    #     new_product = Product(name=vegetable_product[ran][0], discription=product_description[random.randint(
    #         0, 9)]['name'], img_url=vegetable_product[ran][1], price=ran_price, inventory_item_id=random.randint(1, 99), category_id=2)
    #     db.session.add(new_product)
    #     db.session.commit()

    # for x in range(0, 30):
    #     ran = random.randint(0, 4)
    #     ran_price = random.randint(1, 5)*1000
    #     new_product = Product(name=seasoning_product[ran][0], discription=product_description[random.randint(
    #         0, 9)]['name'], img_url=seasoning_product[ran][1], price=ran_price, inventory_item_id=random.randint(1, 99), category_id=3)
    #     db.session.add(new_product)
    #     db.session.commit()

    return jsonify({'head' : 'success!'})
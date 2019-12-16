from src.models.user import db, User, OAuth, Token, Order, Order_item, Order_status
from src.models.product import Product, Inventory, Rating, Category
from src.models.trading import Shipment, Invoice, Invoice_status, Payment
import random

from flask import Blueprint , render_template, jsonify

fakedata_blueprint = Blueprint('fakebp', __name__)

categories = [
    'fruits', 'vegetables', 'seasoning'
]

inventories = ['District 7', 'Thu Duc district']

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

order_status = ['Proceeding', 'Delivering', 'Delivered', 'Canceled', 'In cart']

stores = [
    {
        "id": 1,
        "login_name": "Markus",
        "password": "1234",
        "img_url": "https://robohash.org/etnesciuntiste.jpg?size=100x100&set=set1",
        "store_name": "Janyx"
    }, {
        "id": 2,
        "login_name": "Corabelle",
        "password": "1234",
        "img_url": "https://robohash.org/asperioresinaliquam.bmp?size=100x100&set=set1",
        "store_name": "Eamia"
    }, {
        "id": 3,
        "login_name": "Drusie",
        "password": "1234",
        "img_url": "https://robohash.org/nonsitdolor.png?size=100x100&set=set1",
        "store_name": "BlogXS"
    }, {
        "id": 4,
        "login_name": "Maximilian",
        "password": "1234",
        "img_url": "https://robohash.org/voluptasnonvero.png?size=100x100&set=set1",
        "store_name": "Meedoo"
    }, {
        "id": 5,
        "login_name": "Drugi",
        "password": "1234",
        "img_url": "https://robohash.org/eligendiautdeserunt.jpg?size=100x100&set=set1",
        "store_name": "Dynabox"
    }, {
        "id": 6,
        "login_name": "Ilene",
        "password": "1234",
        "img_url": "https://robohash.org/vellaboreet.bmp?size=100x100&set=set1",
        "store_name": "Photofeed"
    }, {
        "id": 7,
        "login_name": "Illa",
        "password": "1234",
        "img_url": "https://robohash.org/laboriosamvelitanimi.jpg?size=100x100&set=set1",
        "store_name": "Jatri"
    }, {
        "id": 8,
        "login_name": "Essy",
        "password": "1234",
        "img_url": "https://robohash.org/repudiandaeconsequaturqui.png?size=100x100&set=set1",
        "store_name": "Zoozzy"
    }, {
        "id": 9,
        "login_name": "Stinky",
        "password": "1234",
        "img_url": "https://robohash.org/quoquodquam.bmp?size=100x100&set=set1",
        "store_name": "Skaboo"
    }, {
        "id": 10,
        "login_name": "Jackie",
        "password": 12340,
        "img_url": "https://robohash.org/quiinharum.bmp?size=100x100&set=set1",
        "store_name": "Zoozzy"
    }
]

users = [
    {"id":1,"login_name":"Piegrome","img_url":"https://robohash.org/namametincidunt.png?size=200x200&set=set1"},
    {"id":2,"login_name":"Bolderstone","img_url":"https://robohash.org/remminusmodi.png?size=200x200&set=set1"},
    {"id":3,"login_name":"Axleby","img_url":"https://robohash.org/doloreconsequaturquisquam.png?size=200x200&set=set1"},
    {"id":4,"login_name":"Gerge","img_url":"https://robohash.org/nihilrepellendusea.png?size=200x200&set=set1"},
    {"id":5,"login_name":"Ellings","img_url":"https://robohash.org/quoautnihil.png?size=200x200&set=set1"},
    {"id":6,"login_name":"Keling","img_url":"https://robohash.org/doloremquevelitexcepturi.png?size=200x200&set=set1"},
    {"id":7,"login_name":"Kleinerman","img_url":"https://robohash.org/quamvoluptatumet.png?size=200x200&set=set1"},
    {"id":8,"login_name":"Chetter","img_url":"https://robohash.org/istesiteaque.png?size=200x200&set=set1"},
    {"id":9,"login_name":"Jedrachowicz","img_url":"https://robohash.org/situllamamet.png?size=200x200&set=set1"},
    {"id":10,"login_name":"Sayce","img_url":"https://robohash.org/harumdistinctioitaque.png?size=200x200&set=set1"},
    {"id":11,"login_name":"Vella","img_url":"https://robohash.org/utverorepudiandae.png?size=200x200&set=set1"},
    {"id":12,"login_name":"Kenvin","img_url":"https://robohash.org/magninobisdolores.png?size=200x200&set=set1"},
    {"id":13,"login_name":"Perazzo","img_url":"https://robohash.org/quasifugiatsunt.png?size=200x200&set=set1"},
    {"id":14,"login_name":"Beart","img_url":"https://robohash.org/autemaliquammaxime.png?size=200x200&set=set1"},
    {"id":15,"login_name":"Tomasik","img_url":"https://robohash.org/sapienteoditrepellendus.png?size=200x200&set=set1"},
    {"id":16,"login_name":"Neasam","img_url":"https://robohash.org/inerrorautem.png?size=200x200&set=set1"},
    {"id":17,"login_name":"Greenstock","img_url":"https://robohash.org/ututipsum.png?size=200x200&set=set1"},
    {"id":18,"login_name":"Vermer","img_url":"https://robohash.org/quaevelitexercitationem.png?size=200x200&set=set1"},
    {"id":19,"login_name":"Kale","img_url":"https://robohash.org/suscipitnecessitatibusexcepturi.png?size=200x200&set=set1"},
    {"id":20,"login_name":"Portwaine","img_url":"https://robohash.org/occaecatiteneturnesciunt.png?size=200x200&set=set1"},
    {"id":21,"login_name":"Shefton","img_url":"https://robohash.org/aliasassumendafuga.png?size=200x200&set=set1"},
    {"id":22,"login_name":"Guinane","img_url":"https://robohash.org/sequiconsequunturenim.png?size=200x200&set=set1"},
    {"id":23,"login_name":"Gitthouse","img_url":"https://robohash.org/idlaboreesse.png?size=200x200&set=set1"},
    {"id":24,"login_name":"Lyngsted","img_url":"https://robohash.org/aliquiddelectuset.png?size=200x200&set=set1"},
    {"id":25,"login_name":"Dellar","img_url":"https://robohash.org/cupiditateexplicaboesse.png?size=200x200&set=set1"},
    {"id":26,"login_name":"Latham","img_url":"https://robohash.org/voluptatemaccusantiumeligendi.png?size=200x200&set=set1"},
    {"id":27,"login_name":"Bamb","img_url":"https://robohash.org/doloremquequiafacere.png?size=200x200&set=set1"},
    {"id":28,"login_name":"Sigg","img_url":"https://robohash.org/quodveroet.png?size=200x200&set=set1"},
    {"id":29,"login_name":"Lasham","img_url":"https://robohash.org/dolorehiceaque.png?size=200x200&set=set1"},
    {"id":30,"login_name":"Lattimore","img_url":"https://robohash.org/quiimpeditsuscipit.png?size=200x200&set=set1"},
    {"id":31,"login_name":"Rozet","img_url":"https://robohash.org/officiisperspiciatisneque.png?size=200x200&set=set1"},
    {"id":32,"login_name":"Budibent","img_url":"https://robohash.org/doloresvoluptasquidem.png?size=200x200&set=set1"},
    {"id":33,"login_name":"Mains","img_url":"https://robohash.org/temporeculpatotam.png?size=200x200&set=set1"},
    {"id":34,"login_name":"Orrow","img_url":"https://robohash.org/cumculpadoloremque.png?size=200x200&set=set1"},
    {"id":35,"login_name":"Gearty","img_url":"https://robohash.org/involuptasminus.png?size=200x200&set=set1"},
    {"id":36,"login_name":"Arni","img_url":"https://robohash.org/voluptatemsequitotam.png?size=200x200&set=set1"},
    {"id":37,"login_name":"Piddick","img_url":"https://robohash.org/saepequibusdamnesciunt.png?size=200x200&set=set1"},
    {"id":38,"login_name":"Acom","img_url":"https://robohash.org/minimaharumet.png?size=200x200&set=set1"},
    {"id":39,"login_name":"Clemenzi","img_url":"https://robohash.org/nemoillumlibero.png?size=200x200&set=set1"},
    {"id":40,"login_name":"Asgodby","img_url":"https://robohash.org/minusnostrumipsam.png?size=200x200&set=set1"},
]

ratings = [
    {"id":1,"rating":3,"comment":"aggregate granular e-commerce","user_id":25,"product_id":58},
    {"id":2,"rating":1,"comment":"disintermediate transparent e-services","user_id":20,"product_id":87},
    {"id":3,"rating":2,"comment":"facilitate back-end users","user_id":21,"product_id":34},
    {"id":4,"rating":4,"comment":"extend one-to-one platforms","user_id":35,"product_id":69},
    {"id":5,"rating":5,"comment":"envisioneer leading-edge technologies","user_id":38,"product_id":60},
    {"id":6,"rating":3,"comment":"harness front-end applications","user_id":47,"product_id":68},
    {"id":7,"rating":1,"comment":"seize bricks-and-clicks web services","user_id":20,"product_id":50},
    {"id":8,"rating":1,"comment":"aggregate integrated e-markets","user_id":31,"product_id":29},
    {"id":9,"rating":1,"comment":"leverage innovative eyeballs","user_id":32,"product_id":11},
    {"id":10,"rating":1,"comment":"architect synergistic supply-chains","user_id":27,"product_id":49},
    {"id":11,"rating":1,"comment":"implement best-of-breed functionalities","user_id":49,"product_id":24},
    {"id":12,"rating":5,"comment":"synergize best-of-breed metrics","user_id":20,"product_id":18},
    {"id":13,"rating":3,"comment":"engage B2C niches","user_id":33,"product_id":34},
    {"id":14,"rating":5,"comment":"integrate collaborative portals","user_id":38,"product_id":85},
    {"id":15,"rating":3,"comment":"mesh global architectures","user_id":20,"product_id":77},
    {"id":16,"rating":1,"comment":"target best-of-breed initiatives","user_id":36,"product_id":7},
    {"id":17,"rating":5,"comment":"iterate wireless infomediaries","user_id":13,"product_id":28},
    {"id":18,"rating":2,"comment":"target sticky methodologies","user_id":39,"product_id":12},
    {"id":19,"rating":3,"comment":"productize turn-key architectures","user_id":36,"product_id":32},
    {"id":20,"rating":2,"comment":"monetize granular channels","user_id":40,"product_id":30},
    {"id":21,"rating":4,"comment":"unleash leading-edge functionalities","user_id":46,"product_id":30},
    {"id":22,"rating":1,"comment":"maximize user-centric solutions","user_id":11,"product_id":78},
    {"id":23,"rating":5,"comment":"engage enterprise e-business","user_id":21,"product_id":7},
    {"id":24,"rating":1,"comment":"extend bricks-and-clicks e-business","user_id":46,"product_id":57},
    {"id":25,"rating":5,"comment":"expedite interactive relationships","user_id":48,"product_id":27},
    {"id":26,"rating":5,"comment":"engineer wireless mindshare","user_id":45,"product_id":14},
    {"id":27,"rating":1,"comment":"evolve sticky platforms","user_id":25,"product_id":5},
    {"id":28,"rating":4,"comment":"harness holistic convergence","user_id":40,"product_id":79},
    {"id":29,"rating":5,"comment":"incentivize extensible partnerships","user_id":22,"product_id":48},
    {"id":30,"rating":3,"comment":"visualize impactful infrastructures","user_id":21,"product_id":43},
    {"id":31,"rating":2,"comment":"scale next-generation experiences","user_id":11,"product_id":66},
    {"id":32,"rating":2,"comment":"architect user-centric infrastructures","user_id":37,"product_id":31},
    {"id":33,"rating":3,"comment":"e-enable 24/365 e-markets","user_id":40,"product_id":23},
    {"id":34,"rating":5,"comment":"engineer web-enabled markets","user_id":28,"product_id":31},
    {"id":35,"rating":5,"comment":"expedite viral portals","user_id":48,"product_id":6},
    {"id":36,"rating":1,"comment":"seize B2B functionalities","user_id":45,"product_id":51},
    {"id":37,"rating":5,"comment":"strategize turn-key technologies","user_id":49,"product_id":65},
    {"id":38,"rating":1,"comment":"redefine ubiquitous mindshare","user_id":20,"product_id":63},
    {"id":39,"rating":2,"comment":"innovate robust solutions","user_id":41,"product_id":88},
    {"id":40,"rating":3,"comment":"redefine global schemas","user_id":18,"product_id":27},
    {"id":41,"rating":5,"comment":"enhance 24/7 systems","user_id":22,"product_id":47},
    {"id":42,"rating":4,"comment":"matrix strategic mindshare","user_id":46,"product_id":30},
    {"id":43,"rating":1,"comment":"evolve end-to-end synergies","user_id":21,"product_id":84},
    {"id":44,"rating":5,"comment":"optimize sticky systems","user_id":35,"product_id":38},
    {"id":45,"rating":3,"comment":"matrix bricks-and-clicks users","user_id":49,"product_id":37},
    {"id":46,"rating":3,"comment":"innovate efficient relationships","user_id":11,"product_id":31},
    {"id":47,"rating":4,"comment":"iterate clicks-and-mortar channels","user_id":41,"product_id":88},
    {"id":48,"rating":2,"comment":"architect mission-critical web services","user_id":36,"product_id":77},
    {"id":49,"rating":5,"comment":"streamline value-added mindshare","user_id":39,"product_id":80},
    {"id":50,"rating":2,"comment":"syndicate bleeding-edge markets","user_id":42,"product_id":63},
    {"id":51,"rating":3,"comment":"e-enable enterprise schemas","user_id":48,"product_id":72},
    {"id":52,"rating":4,"comment":"whiteboard e-business infrastructures","user_id":31,"product_id":62},
    {"id":53,"rating":3,"comment":"evolve cutting-edge technologies","user_id":45,"product_id":23},
    {"id":54,"rating":4,"comment":"harness seamless partnerships","user_id":40,"product_id":34},
    {"id":55,"rating":4,"comment":"target impactful deliverables","user_id":23,"product_id":75},
    {"id":56,"rating":1,"comment":"unleash collaborative functionalities","user_id":15,"product_id":34},
    {"id":57,"rating":4,"comment":"synthesize clicks-and-mortar experiences","user_id":14,"product_id":16},
    {"id":58,"rating":1,"comment":"redefine distributed mindshare","user_id":48,"product_id":20},
    {"id":59,"rating":2,"comment":"generate world-class relationships","user_id":43,"product_id":75},
    {"id":60,"rating":1,"comment":"maximize collaborative bandwidth","user_id":40,"product_id":69},
    {"id":61,"rating":5,"comment":"matrix holistic initiatives","user_id":21,"product_id":26},
    {"id":62,"rating":2,"comment":"streamline back-end supply-chains","user_id":41,"product_id":28},
    {"id":63,"rating":1,"comment":"unleash granular models","user_id":28,"product_id":89},
    {"id":64,"rating":3,"comment":"brand impactful communities","user_id":11,"product_id":57},
    {"id":65,"rating":4,"comment":"redefine real-time systems","user_id":27,"product_id":62},
    {"id":66,"rating":4,"comment":"monetize user-centric web-readiness","user_id":13,"product_id":44},
    {"id":67,"rating":4,"comment":"synthesize 24/365 e-business","user_id":30,"product_id":81},
    {"id":68,"rating":5,"comment":"whiteboard mission-critical solutions","user_id":33,"product_id":20},
    {"id":69,"rating":2,"comment":"deliver dynamic architectures","user_id":25,"product_id":33},
    {"id":70,"rating":2,"comment":"matrix magnetic models","user_id":38,"product_id":16},
    {"id":71,"rating":4,"comment":"transform vertical e-business","user_id":25,"product_id":87},
    {"id":72,"rating":5,"comment":"monetize proactive infomediaries","user_id":36,"product_id":83},
    {"id":73,"rating":5,"comment":"mesh global architectures","user_id":42,"product_id":79},
    {"id":74,"rating":4,"comment":"exploit B2C platforms","user_id":11,"product_id":56},
    {"id":75,"rating":1,"comment":"repurpose front-end e-tailers","user_id":21,"product_id":23},
    {"id":76,"rating":3,"comment":"synergize B2C models","user_id":16,"product_id":67},
    {"id":77,"rating":4,"comment":"engineer out-of-the-box relationships","user_id":23,"product_id":77},
    {"id":78,"rating":3,"comment":"incubate interactive initiatives","user_id":12,"product_id":56},
    {"id":79,"rating":2,"comment":"scale world-class vortals","user_id":47,"product_id":29},
    {"id":80,"rating":1,"comment":"embrace strategic methodologies","user_id":35,"product_id":81},
    {"id":81,"rating":1,"comment":"brand proactive relationships","user_id":40,"product_id":25},
    {"id":82,"rating":2,"comment":"extend viral supply-chains","user_id":38,"product_id":26},
    {"id":83,"rating":5,"comment":"evolve frictionless methodologies","user_id":39,"product_id":56},
    {"id":84,"rating":4,"comment":"generate plug-and-play metrics","user_id":30,"product_id":54},
    {"id":85,"rating":4,"comment":"maximize virtual communities","user_id":34,"product_id":84},
    {"id":86,"rating":5,"comment":"implement B2C e-tailers","user_id":16,"product_id":38},
    {"id":87,"rating":1,"comment":"scale integrated initiatives","user_id":49,"product_id":45},
    {"id":88,"rating":2,"comment":"benchmark distributed paradigms","user_id":40,"product_id":64},
    {"id":89,"rating":1,"comment":"disintermediate holistic systems","user_id":43,"product_id":12},
    {"id":90,"rating":4,"comment":"morph efficient ROI","user_id":13,"product_id":26},
    {"id":91,"rating":2,"comment":"streamline dot-com portals","user_id":40,"product_id":66},
    {"id":92,"rating":1,"comment":"harness holistic networks","user_id":17,"product_id":86},
    {"id":93,"rating":1,"comment":"envisioneer bleeding-edge systems","user_id":19,"product_id":39},
    {"id":94,"rating":5,"comment":"transform plug-and-play e-services","user_id":12,"product_id":36},
    {"id":95,"rating":4,"comment":"synthesize open-source methodologies","user_id":49,"product_id":71},
    {"id":96,"rating":5,"comment":"morph scalable e-commerce","user_id":35,"product_id":57},
    {"id":97,"rating":4,"comment":"repurpose frictionless ROI","user_id":37,"product_id":1},
    {"id":98,"rating":1,"comment":"incentivize e-business supply-chains","user_id":42,"product_id":21},
    {"id":99,"rating":3,"comment":"deliver magnetic initiatives","user_id":32,"product_id":32},
    {"id":100,"rating":5,"comment":"repurpose innovative functionalities","user_id":27,"product_id":13},
    {"id":101,"rating":1,"comment":"implement innovative niches","user_id":19,"product_id":58},
    {"id":102,"rating":3,"comment":"synergize intuitive deliverables","user_id":45,"product_id":18},
    {"id":103,"rating":5,"comment":"empower extensible metrics","user_id":40,"product_id":67},
    {"id":104,"rating":2,"comment":"productize one-to-one schemas","user_id":30,"product_id":72},
    {"id":105,"rating":2,"comment":"orchestrate customized synergies","user_id":32,"product_id":41},
    {"id":106,"rating":2,"comment":"grow strategic initiatives","user_id":17,"product_id":37},
    {"id":107,"rating":2,"comment":"disintermediate robust action-items","user_id":41,"product_id":57},
    {"id":108,"rating":2,"comment":"disintermediate scalable partnerships","user_id":41,"product_id":11},
    {"id":109,"rating":1,"comment":"redefine B2C users","user_id":37,"product_id":80},
    {"id":110,"rating":3,"comment":"streamline B2B users","user_id":46,"product_id":70},
    {"id":111,"rating":2,"comment":"maximize e-business metrics","user_id":40,"product_id":87},
    {"id":112,"rating":5,"comment":"whiteboard strategic web services","user_id":22,"product_id":11},
    {"id":113,"rating":3,"comment":"enable revolutionary convergence","user_id":17,"product_id":42},
    {"id":114,"rating":1,"comment":"whiteboard viral content","user_id":45,"product_id":55},
    {"id":115,"rating":3,"comment":"incubate collaborative synergies","user_id":44,"product_id":57},
    {"id":116,"rating":5,"comment":"visualize ubiquitous web services","user_id":49,"product_id":4},
    {"id":117,"rating":1,"comment":"implement strategic users","user_id":49,"product_id":77},
    {"id":118,"rating":2,"comment":"matrix rich mindshare","user_id":31,"product_id":57},
    {"id":119,"rating":3,"comment":"grow rich portals","user_id":22,"product_id":16},
    {"id":120,"rating":3,"comment":"morph out-of-the-box supply-chains","user_id":17,"product_id":64},
    {"id":121,"rating":3,"comment":"evolve clicks-and-mortar ROI","user_id":33,"product_id":42},
    {"id":122,"rating":4,"comment":"leverage visionary portals","user_id":49,"product_id":85},
    {"id":123,"rating":2,"comment":"generate dot-com e-markets","user_id":45,"product_id":77},
    {"id":124,"rating":5,"comment":"orchestrate web-enabled schemas","user_id":37,"product_id":82},
    {"id":125,"rating":1,"comment":"enable turn-key vortals","user_id":34,"product_id":46},
    {"id":126,"rating":5,"comment":"exploit distributed supply-chains","user_id":19,"product_id":72},
    {"id":127,"rating":4,"comment":"engineer global e-business","user_id":26,"product_id":39},
    {"id":128,"rating":4,"comment":"strategize virtual systems","user_id":16,"product_id":86},
    {"id":129,"rating":5,"comment":"optimize bricks-and-clicks functionalities","user_id":22,"product_id":81},
    {"id":130,"rating":3,"comment":"monetize magnetic web-readiness","user_id":29,"product_id":57},
    {"id":131,"rating":4,"comment":"orchestrate best-of-breed synergies","user_id":17,"product_id":79},
    {"id":132,"rating":2,"comment":"scale clicks-and-mortar networks","user_id":12,"product_id":29},
    {"id":133,"rating":4,"comment":"recontextualize cross-platform channels","user_id":43,"product_id":31},
    {"id":134,"rating":5,"comment":"productize scalable ROI","user_id":39,"product_id":74},
    {"id":135,"rating":1,"comment":"streamline dot-com content","user_id":43,"product_id":79},
    {"id":136,"rating":1,"comment":"cultivate impactful methodologies","user_id":16,"product_id":51},
    {"id":137,"rating":4,"comment":"unleash sticky networks","user_id":19,"product_id":66},
    {"id":138,"rating":5,"comment":"empower end-to-end portals","user_id":21,"product_id":72},
    {"id":139,"rating":5,"comment":"facilitate next-generation networks","user_id":41,"product_id":84},
    {"id":140,"rating":2,"comment":"grow cross-media communities","user_id":33,"product_id":19},
    {"id":141,"rating":2,"comment":"benchmark clicks-and-mortar eyeballs","user_id":13,"product_id":51},
    {"id":142,"rating":5,"comment":"reintermediate transparent metrics","user_id":46,"product_id":2},
    {"id":143,"rating":4,"comment":"morph vertical relationships","user_id":14,"product_id":4},
    {"id":144,"rating":3,"comment":"deploy plug-and-play e-business","user_id":42,"product_id":87},
    {"id":145,"rating":3,"comment":"seize scalable e-services","user_id":36,"product_id":25},
    {"id":146,"rating":1,"comment":"cultivate one-to-one e-markets","user_id":27,"product_id":67},
    {"id":147,"rating":1,"comment":"embrace one-to-one infrastructures","user_id":46,"product_id":10},
    {"id":148,"rating":2,"comment":"brand vertical web services","user_id":29,"product_id":36},
    {"id":149,"rating":5,"comment":"target e-business channels","user_id":18,"product_id":32},
    {"id":150,"rating":2,"comment":"facilitate intuitive technologies","user_id":39,"product_id":41},
    {"id":151,"rating":4,"comment":"whiteboard compelling supply-chains","user_id":23,"product_id":64},
    {"id":152,"rating":3,"comment":"strategize collaborative systems","user_id":19,"product_id":64},
    {"id":153,"rating":4,"comment":"harness clicks-and-mortar markets","user_id":24,"product_id":13},
    {"id":154,"rating":3,"comment":"morph viral vortals","user_id":14,"product_id":15},
    {"id":155,"rating":5,"comment":"transition front-end metrics","user_id":37,"product_id":33},
    {"id":156,"rating":3,"comment":"empower global mindshare","user_id":44,"product_id":83},
    {"id":157,"rating":5,"comment":"architect leading-edge markets","user_id":49,"product_id":66},
    {"id":158,"rating":1,"comment":"leverage open-source e-commerce","user_id":30,"product_id":10},
    {"id":159,"rating":1,"comment":"incentivize killer channels","user_id":36,"product_id":8},
    {"id":160,"rating":2,"comment":"transition one-to-one synergies","user_id":23,"product_id":64},
    {"id":161,"rating":5,"comment":"visualize cross-platform initiatives","user_id":49,"product_id":22},
    {"id":162,"rating":1,"comment":"morph 24/7 synergies","user_id":24,"product_id":76},
    {"id":163,"rating":4,"comment":"brand cutting-edge partnerships","user_id":21,"product_id":75},
    {"id":164,"rating":5,"comment":"scale cross-media e-services","user_id":19,"product_id":59},
    {"id":165,"rating":1,"comment":"enable integrated web services","user_id":46,"product_id":29},
    {"id":166,"rating":1,"comment":"utilize enterprise infomediaries","user_id":34,"product_id":1},
    {"id":167,"rating":4,"comment":"embrace mission-critical vortals","user_id":44,"product_id":42},
    {"id":168,"rating":1,"comment":"revolutionize strategic models","user_id":15,"product_id":5},
    {"id":169,"rating":1,"comment":"strategize bricks-and-clicks partnerships","user_id":11,"product_id":71},
    {"id":170,"rating":1,"comment":"envisioneer bleeding-edge e-tailers","user_id":26,"product_id":38},
    {"id":171,"rating":1,"comment":"grow bleeding-edge architectures","user_id":35,"product_id":9},
    {"id":172,"rating":5,"comment":"brand virtual niches","user_id":39,"product_id":65},
    {"id":173,"rating":1,"comment":"whiteboard sticky applications","user_id":38,"product_id":86},
    {"id":174,"rating":4,"comment":"whiteboard next-generation initiatives","user_id":42,"product_id":13},
    {"id":175,"rating":2,"comment":"incubate collaborative ROI","user_id":40,"product_id":64},
    {"id":176,"rating":3,"comment":"morph customized technologies","user_id":35,"product_id":45},
    {"id":177,"rating":5,"comment":"whiteboard web-enabled communities","user_id":41,"product_id":8},
    {"id":178,"rating":5,"comment":"synergize vertical networks","user_id":35,"product_id":24},
    {"id":179,"rating":4,"comment":"incubate value-added schemas","user_id":27,"product_id":62},
    {"id":180,"rating":3,"comment":"expedite proactive portals","user_id":21,"product_id":17},
    {"id":181,"rating":1,"comment":"leverage best-of-breed communities","user_id":18,"product_id":37},
    {"id":182,"rating":3,"comment":"syndicate distributed relationships","user_id":47,"product_id":13},
    {"id":183,"rating":2,"comment":"harness plug-and-play bandwidth","user_id":43,"product_id":7},
    {"id":184,"rating":3,"comment":"envisioneer leading-edge e-tailers","user_id":29,"product_id":13},
    {"id":185,"rating":5,"comment":"matrix customized niches","user_id":40,"product_id":76},
    {"id":186,"rating":5,"comment":"engineer interactive paradigms","user_id":13,"product_id":64},
    {"id":187,"rating":1,"comment":"aggregate plug-and-play metrics","user_id":47,"product_id":1},
    {"id":188,"rating":1,"comment":"brand frictionless platforms","user_id":42,"product_id":59},
    {"id":189,"rating":2,"comment":"transition dot-com partnerships","user_id":48,"product_id":18},
    {"id":190,"rating":4,"comment":"target vertical interfaces","user_id":37,"product_id":34},
    {"id":191,"rating":3,"comment":"mesh extensible e-business","user_id":12,"product_id":53},
    {"id":192,"rating":5,"comment":"whiteboard enterprise niches","user_id":37,"product_id":21},
    {"id":193,"rating":4,"comment":"morph next-generation infrastructures","user_id":12,"product_id":54},
    {"id":194,"rating":5,"comment":"scale 24/7 bandwidth","user_id":13,"product_id":72},
    {"id":195,"rating":3,"comment":"harness dynamic content","user_id":36,"product_id":1},
    {"id":196,"rating":2,"comment":"morph next-generation deliverables","user_id":27,"product_id":9},
    {"id":197,"rating":4,"comment":"target efficient infrastructures","user_id":16,"product_id":13},
    {"id":198,"rating":2,"comment":"engage viral schemas","user_id":47,"product_id":44},
    {"id":199,"rating":5,"comment":"expedite value-added solutions","user_id":41,"product_id":23},
    {"id":200,"rating":1,"comment":"exploit scalable methodologies","user_id":45,"product_id":84},
    {"id":201,"rating":1,"comment":"strategize one-to-one content","user_id":16,"product_id":86},
    {"id":202,"rating":5,"comment":"enhance dot-com networks","user_id":16,"product_id":52},
    {"id":203,"rating":1,"comment":"productize enterprise schemas","user_id":46,"product_id":80},
    {"id":204,"rating":2,"comment":"transition compelling initiatives","user_id":46,"product_id":74},
    {"id":205,"rating":4,"comment":"benchmark cutting-edge functionalities","user_id":36,"product_id":87},
    {"id":206,"rating":3,"comment":"orchestrate out-of-the-box ROI","user_id":30,"product_id":1},
    {"id":207,"rating":2,"comment":"evolve back-end convergence","user_id":15,"product_id":21},
    {"id":208,"rating":3,"comment":"syndicate end-to-end models","user_id":35,"product_id":86},
    {"id":209,"rating":2,"comment":"brand 24/7 e-markets","user_id":32,"product_id":36},
    {"id":210,"rating":4,"comment":"implement transparent e-services","user_id":47,"product_id":86},
    {"id":211,"rating":5,"comment":"utilize leading-edge ROI","user_id":37,"product_id":65},
    {"id":212,"rating":1,"comment":"cultivate bricks-and-clicks users","user_id":47,"product_id":4},
    {"id":213,"rating":4,"comment":"repurpose sticky supply-chains","user_id":26,"product_id":62},
    {"id":214,"rating":1,"comment":"brand virtual functionalities","user_id":43,"product_id":55},
    {"id":215,"rating":1,"comment":"strategize impactful metrics","user_id":24,"product_id":84},
    {"id":216,"rating":2,"comment":"harness dot-com content","user_id":17,"product_id":38},
    {"id":217,"rating":4,"comment":"target sexy initiatives","user_id":39,"product_id":76},
    {"id":218,"rating":5,"comment":"incubate extensible action-items","user_id":49,"product_id":5},
    {"id":219,"rating":2,"comment":"monetize clicks-and-mortar networks","user_id":32,"product_id":2},
    {"id":220,"rating":4,"comment":"scale bleeding-edge initiatives","user_id":15,"product_id":36},
    {"id":221,"rating":4,"comment":"facilitate e-business systems","user_id":15,"product_id":38},
    {"id":222,"rating":4,"comment":"architect clicks-and-mortar content","user_id":38,"product_id":34},
    {"id":223,"rating":2,"comment":"transition compelling communities","user_id":14,"product_id":7},
    {"id":224,"rating":4,"comment":"syndicate global e-tailers","user_id":35,"product_id":66},
    {"id":225,"rating":1,"comment":"e-enable cross-media methodologies","user_id":46,"product_id":28},
    {"id":226,"rating":4,"comment":"iterate ubiquitous models","user_id":34,"product_id":69},
    {"id":227,"rating":4,"comment":"transform seamless methodologies","user_id":18,"product_id":64},
    {"id":228,"rating":3,"comment":"empower killer vortals","user_id":38,"product_id":60},
    {"id":229,"rating":4,"comment":"drive sexy paradigms","user_id":35,"product_id":61},
    {"id":230,"rating":3,"comment":"streamline value-added supply-chains","user_id":34,"product_id":44},
    {"id":231,"rating":1,"comment":"cultivate one-to-one infomediaries","user_id":17,"product_id":62},
    {"id":232,"rating":5,"comment":"reintermediate dot-com niches","user_id":11,"product_id":30},
    {"id":233,"rating":4,"comment":"unleash turn-key action-items","user_id":17,"product_id":73},
    {"id":234,"rating":5,"comment":"synthesize dynamic interfaces","user_id":16,"product_id":36},
    {"id":235,"rating":4,"comment":"extend 24/7 deliverables","user_id":16,"product_id":8},
    {"id":236,"rating":2,"comment":"deploy holistic relationships","user_id":27,"product_id":39},
    {"id":237,"rating":5,"comment":"utilize mission-critical supply-chains","user_id":40,"product_id":37},
    {"id":238,"rating":3,"comment":"facilitate dynamic methodologies","user_id":11,"product_id":69},
    {"id":239,"rating":5,"comment":"synthesize cross-platform web-readiness","user_id":16,"product_id":21},
    {"id":240,"rating":2,"comment":"reintermediate 24/365 functionalities","user_id":32,"product_id":1},
    {"id":241,"rating":4,"comment":"reintermediate cross-media e-business","user_id":20,"product_id":66},
    {"id":242,"rating":2,"comment":"deploy sticky functionalities","user_id":43,"product_id":86},
    {"id":243,"rating":3,"comment":"exploit dot-com platforms","user_id":14,"product_id":48},
    {"id":244,"rating":4,"comment":"enable wireless experiences","user_id":12,"product_id":85},
    {"id":245,"rating":3,"comment":"cultivate magnetic partnerships","user_id":48,"product_id":9},
    {"id":246,"rating":4,"comment":"synergize wireless web-readiness","user_id":19,"product_id":65},
    {"id":247,"rating":5,"comment":"implement e-business e-services","user_id":16,"product_id":3},
    {"id":248,"rating":1,"comment":"expedite intuitive supply-chains","user_id":30,"product_id":75},
    {"id":249,"rating":4,"comment":"aggregate rich functionalities","user_id":28,"product_id":75},
    {"id":250,"rating":1,"comment":"disintermediate web-enabled metrics","user_id":35,"product_id":84},
    {"id":251,"rating":4,"comment":"reintermediate dynamic technologies","user_id":48,"product_id":67},
    {"id":252,"rating":1,"comment":"productize virtual systems","user_id":11,"product_id":45},
    {"id":253,"rating":3,"comment":"optimize clicks-and-mortar experiences","user_id":42,"product_id":26},
    {"id":254,"rating":2,"comment":"evolve collaborative systems","user_id":46,"product_id":81},
    {"id":255,"rating":3,"comment":"productize cutting-edge methodologies","user_id":49,"product_id":25},
    {"id":256,"rating":2,"comment":"benchmark sticky ROI","user_id":35,"product_id":67},
    {"id":257,"rating":3,"comment":"reintermediate plug-and-play systems","user_id":21,"product_id":48},
    {"id":258,"rating":5,"comment":"generate strategic e-markets","user_id":11,"product_id":11},
    {"id":259,"rating":1,"comment":"incubate cross-platform systems","user_id":24,"product_id":12},
    {"id":260,"rating":1,"comment":"matrix vertical niches","user_id":22,"product_id":49},
    {"id":261,"rating":5,"comment":"redefine robust networks","user_id":16,"product_id":65},
    {"id":262,"rating":5,"comment":"engage world-class web-readiness","user_id":24,"product_id":12},
    {"id":263,"rating":2,"comment":"strategize front-end infomediaries","user_id":36,"product_id":75},
    {"id":264,"rating":3,"comment":"repurpose turn-key architectures","user_id":24,"product_id":31},
    {"id":265,"rating":2,"comment":"streamline dot-com initiatives","user_id":24,"product_id":84},
    {"id":266,"rating":3,"comment":"strategize enterprise applications","user_id":38,"product_id":22},
    {"id":267,"rating":1,"comment":"generate seamless schemas","user_id":32,"product_id":51},
    {"id":268,"rating":3,"comment":"synergize B2C e-tailers","user_id":25,"product_id":44},
    {"id":269,"rating":2,"comment":"harness global solutions","user_id":34,"product_id":66},
    {"id":270,"rating":5,"comment":"evolve intuitive e-markets","user_id":13,"product_id":81},
    {"id":271,"rating":5,"comment":"drive distributed paradigms","user_id":28,"product_id":82},
    {"id":272,"rating":5,"comment":"visualize seamless markets","user_id":42,"product_id":82},
    {"id":273,"rating":4,"comment":"reintermediate cross-platform paradigms","user_id":45,"product_id":12},
    {"id":274,"rating":3,"comment":"architect impactful channels","user_id":48,"product_id":79},
    {"id":275,"rating":4,"comment":"recontextualize B2C technologies","user_id":17,"product_id":9},
    {"id":276,"rating":4,"comment":"implement front-end action-items","user_id":23,"product_id":7},
    {"id":277,"rating":1,"comment":"enable dot-com vortals","user_id":27,"product_id":58},
    {"id":278,"rating":2,"comment":"incubate back-end solutions","user_id":11,"product_id":11},
    {"id":279,"rating":3,"comment":"architect proactive e-business","user_id":34,"product_id":81},
    {"id":280,"rating":3,"comment":"redefine best-of-breed e-commerce","user_id":47,"product_id":71},
    {"id":281,"rating":2,"comment":"productize visionary infrastructures","user_id":20,"product_id":85},
    {"id":282,"rating":5,"comment":"strategize bricks-and-clicks systems","user_id":43,"product_id":56},
    {"id":283,"rating":2,"comment":"syndicate value-added platforms","user_id":19,"product_id":84},
    {"id":284,"rating":4,"comment":"evolve cross-media deliverables","user_id":19,"product_id":81},
    {"id":285,"rating":3,"comment":"target plug-and-play experiences","user_id":33,"product_id":83},
    {"id":286,"rating":1,"comment":"evolve real-time infomediaries","user_id":27,"product_id":25},
    {"id":287,"rating":5,"comment":"scale frictionless relationships","user_id":15,"product_id":13},
    {"id":288,"rating":1,"comment":"evolve real-time vortals","user_id":19,"product_id":69},
    {"id":289,"rating":4,"comment":"innovate robust models","user_id":14,"product_id":70},
    {"id":290,"rating":2,"comment":"recontextualize web-enabled markets","user_id":40,"product_id":70},
    {"id":291,"rating":1,"comment":"maximize interactive vortals","user_id":27,"product_id":6},
    {"id":292,"rating":3,"comment":"seize virtual vortals","user_id":41,"product_id":49},
    {"id":293,"rating":4,"comment":"disintermediate revolutionary e-tailers","user_id":20,"product_id":87},
    {"id":294,"rating":1,"comment":"aggregate extensible applications","user_id":34,"product_id":37},
    {"id":295,"rating":2,"comment":"incubate one-to-one channels","user_id":16,"product_id":13},
    {"id":296,"rating":4,"comment":"target extensible bandwidth","user_id":27,"product_id":81},
    {"id":297,"rating":5,"comment":"leverage mission-critical e-commerce","user_id":47,"product_id":75},
    {"id":298,"rating":5,"comment":"e-enable robust communities","user_id":26,"product_id":20},
    {"id":299,"rating":4,"comment":"iterate mission-critical bandwidth","user_id":47,"product_id":77},
    {"id":300,"rating":2,"comment":"mesh extensible partnerships","user_id":23,"product_id":4},
    {"id":301,"rating":2,"comment":"incubate sexy architectures","user_id":22,"product_id":72},
    {"id":302,"rating":1,"comment":"enhance scalable content","user_id":35,"product_id":47},
    {"id":303,"rating":1,"comment":"exploit user-centric networks","user_id":22,"product_id":78},
    {"id":304,"rating":2,"comment":"implement plug-and-play models","user_id":20,"product_id":45},
    {"id":305,"rating":3,"comment":"drive next-generation bandwidth","user_id":22,"product_id":44},
    {"id":306,"rating":3,"comment":"cultivate one-to-one e-tailers","user_id":31,"product_id":40},
    {"id":307,"rating":2,"comment":"cultivate front-end models","user_id":43,"product_id":18},
    {"id":308,"rating":4,"comment":"synthesize back-end web-readiness","user_id":45,"product_id":33},
    {"id":309,"rating":3,"comment":"reintermediate turn-key synergies","user_id":35,"product_id":42},
    {"id":310,"rating":2,"comment":"integrate frictionless channels","user_id":15,"product_id":50},
    {"id":311,"rating":5,"comment":"transform strategic paradigms","user_id":28,"product_id":24},
    {"id":312,"rating":4,"comment":"innovate killer web-readiness","user_id":33,"product_id":87},
    {"id":313,"rating":2,"comment":"grow proactive portals","user_id":28,"product_id":40},
    {"id":314,"rating":1,"comment":"deliver open-source e-markets","user_id":45,"product_id":7},
    {"id":315,"rating":3,"comment":"morph revolutionary networks","user_id":37,"product_id":53},
    {"id":316,"rating":2,"comment":"harness back-end users","user_id":46,"product_id":17},
    {"id":317,"rating":2,"comment":"deliver integrated mindshare","user_id":13,"product_id":35},
    {"id":318,"rating":5,"comment":"incentivize frictionless e-markets","user_id":29,"product_id":58},
    {"id":319,"rating":5,"comment":"extend rich solutions","user_id":28,"product_id":57},
    {"id":320,"rating":3,"comment":"cultivate user-centric bandwidth","user_id":23,"product_id":4},
    {"id":321,"rating":4,"comment":"reinvent distributed eyeballs","user_id":26,"product_id":34},
    {"id":322,"rating":4,"comment":"extend frictionless paradigms","user_id":22,"product_id":59},
    {"id":323,"rating":3,"comment":"iterate clicks-and-mortar infrastructures","user_id":17,"product_id":41},
    {"id":324,"rating":2,"comment":"morph clicks-and-mortar infrastructures","user_id":11,"product_id":45},
    {"id":325,"rating":1,"comment":"synergize open-source mindshare","user_id":34,"product_id":61},
    {"id":326,"rating":3,"comment":"streamline viral models","user_id":46,"product_id":60},
    {"id":327,"rating":3,"comment":"transform efficient web-readiness","user_id":26,"product_id":58},
    {"id":328,"rating":1,"comment":"synthesize cross-platform infrastructures","user_id":23,"product_id":59},
    {"id":329,"rating":5,"comment":"maximize intuitive metrics","user_id":49,"product_id":85},
    {"id":330,"rating":2,"comment":"orchestrate innovative communities","user_id":12,"product_id":10},
    {"id":331,"rating":2,"comment":"benchmark cross-platform content","user_id":13,"product_id":27},
    {"id":332,"rating":3,"comment":"incentivize user-centric web services","user_id":28,"product_id":16},
    {"id":333,"rating":4,"comment":"syndicate next-generation users","user_id":46,"product_id":51},
    {"id":334,"rating":3,"comment":"e-enable intuitive web services","user_id":11,"product_id":43},
    {"id":335,"rating":4,"comment":"mesh holistic channels","user_id":39,"product_id":28},
    {"id":336,"rating":5,"comment":"syndicate visionary architectures","user_id":46,"product_id":50},
    {"id":337,"rating":3,"comment":"engage mission-critical communities","user_id":43,"product_id":25},
    {"id":338,"rating":4,"comment":"mesh cross-media methodologies","user_id":27,"product_id":1},
    {"id":339,"rating":1,"comment":"whiteboard enterprise partnerships","user_id":32,"product_id":67},
    {"id":340,"rating":3,"comment":"benchmark scalable bandwidth","user_id":26,"product_id":71},
    {"id":341,"rating":3,"comment":"harness turn-key functionalities","user_id":22,"product_id":21},
    {"id":342,"rating":3,"comment":"evolve global communities","user_id":29,"product_id":81},
    {"id":343,"rating":1,"comment":"grow front-end applications","user_id":34,"product_id":13},
    {"id":344,"rating":4,"comment":"recontextualize collaborative communities","user_id":43,"product_id":6},
    {"id":345,"rating":4,"comment":"target granular content","user_id":42,"product_id":70},
    {"id":346,"rating":3,"comment":"deploy next-generation paradigms","user_id":37,"product_id":67},
    {"id":347,"rating":1,"comment":"repurpose back-end eyeballs","user_id":47,"product_id":8},
    {"id":348,"rating":1,"comment":"cultivate dynamic e-tailers","user_id":26,"product_id":3},
    {"id":349,"rating":5,"comment":"maximize plug-and-play systems","user_id":27,"product_id":67},
    {"id":350,"rating":2,"comment":"visualize rich channels","user_id":14,"product_id":40},
    {"id":351,"rating":4,"comment":"recontextualize value-added metrics","user_id":29,"product_id":13},
    {"id":352,"rating":5,"comment":"transform B2C solutions","user_id":39,"product_id":22},
    {"id":353,"rating":1,"comment":"expedite sexy e-services","user_id":36,"product_id":74},
    {"id":354,"rating":2,"comment":"transition bleeding-edge schemas","user_id":28,"product_id":41},
    {"id":355,"rating":1,"comment":"recontextualize dot-com niches","user_id":25,"product_id":40},
    {"id":356,"rating":3,"comment":"maximize out-of-the-box channels","user_id":14,"product_id":14},
    {"id":357,"rating":3,"comment":"aggregate one-to-one paradigms","user_id":34,"product_id":45},
    {"id":358,"rating":2,"comment":"scale frictionless portals","user_id":16,"product_id":70},
    {"id":359,"rating":2,"comment":"expedite robust markets","user_id":29,"product_id":4},
    {"id":360,"rating":2,"comment":"expedite strategic e-markets","user_id":24,"product_id":16},
    {"id":361,"rating":5,"comment":"incentivize global supply-chains","user_id":41,"product_id":10},
    {"id":362,"rating":2,"comment":"syndicate rich deliverables","user_id":44,"product_id":84},
    {"id":363,"rating":2,"comment":"whiteboard B2B communities","user_id":49,"product_id":63},
    {"id":364,"rating":1,"comment":"deliver interactive bandwidth","user_id":41,"product_id":85},
    {"id":365,"rating":3,"comment":"disintermediate real-time convergence","user_id":23,"product_id":11},
    {"id":366,"rating":3,"comment":"cultivate 24/7 e-business","user_id":17,"product_id":28},
    {"id":367,"rating":4,"comment":"aggregate scalable eyeballs","user_id":35,"product_id":50},
    {"id":368,"rating":4,"comment":"implement B2B models","user_id":41,"product_id":67},
    {"id":369,"rating":2,"comment":"orchestrate open-source infrastructures","user_id":36,"product_id":46},
    {"id":370,"rating":1,"comment":"morph mission-critical methodologies","user_id":34,"product_id":17},
    {"id":371,"rating":4,"comment":"aggregate seamless communities","user_id":40,"product_id":72},
    {"id":372,"rating":4,"comment":"innovate holistic applications","user_id":11,"product_id":88},
    {"id":373,"rating":3,"comment":"maximize killer ROI","user_id":39,"product_id":85},
    {"id":374,"rating":5,"comment":"drive cross-media paradigms","user_id":22,"product_id":58},
    {"id":375,"rating":2,"comment":"whiteboard B2B applications","user_id":14,"product_id":22},
    {"id":376,"rating":2,"comment":"repurpose bricks-and-clicks functionalities","user_id":16,"product_id":83},
    {"id":377,"rating":4,"comment":"facilitate wireless deliverables","user_id":23,"product_id":32},
    {"id":378,"rating":5,"comment":"maximize cross-media e-markets","user_id":39,"product_id":88},
    {"id":379,"rating":2,"comment":"deploy scalable solutions","user_id":39,"product_id":84},
    {"id":380,"rating":1,"comment":"implement cutting-edge networks","user_id":22,"product_id":45},
    {"id":381,"rating":3,"comment":"disintermediate efficient relationships","user_id":22,"product_id":28},
    {"id":382,"rating":3,"comment":"grow plug-and-play deliverables","user_id":38,"product_id":76},
    {"id":383,"rating":4,"comment":"envisioneer best-of-breed initiatives","user_id":25,"product_id":83},
    {"id":384,"rating":4,"comment":"drive one-to-one relationships","user_id":20,"product_id":30},
    {"id":385,"rating":2,"comment":"embrace front-end e-tailers","user_id":44,"product_id":63},
    {"id":386,"rating":3,"comment":"engage compelling bandwidth","user_id":37,"product_id":4},
    {"id":387,"rating":5,"comment":"monetize magnetic content","user_id":18,"product_id":18},
    {"id":388,"rating":2,"comment":"architect out-of-the-box functionalities","user_id":16,"product_id":82},
    {"id":389,"rating":1,"comment":"mesh compelling synergies","user_id":14,"product_id":75},
    {"id":390,"rating":1,"comment":"utilize next-generation channels","user_id":12,"product_id":67},
    {"id":391,"rating":2,"comment":"cultivate customized e-commerce","user_id":49,"product_id":18},
    {"id":392,"rating":1,"comment":"generate interactive interfaces","user_id":13,"product_id":66},
    {"id":393,"rating":2,"comment":"leverage plug-and-play architectures","user_id":37,"product_id":83},
    {"id":394,"rating":2,"comment":"generate impactful infomediaries","user_id":49,"product_id":52},
    {"id":395,"rating":3,"comment":"optimize bleeding-edge e-services","user_id":24,"product_id":5},
    {"id":396,"rating":3,"comment":"syndicate B2B e-services","user_id":28,"product_id":40},
    {"id":397,"rating":3,"comment":"deploy best-of-breed deliverables","user_id":14,"product_id":73},
    {"id":398,"rating":2,"comment":"evolve bleeding-edge content","user_id":45,"product_id":89},
    {"id":399,"rating":4,"comment":"disintermediate granular users","user_id":20,"product_id":59},
    {"id":400,"rating":1,"comment":"visualize dynamic mindshare","user_id":34,"product_id":10}
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

    # for el in order_status:
    #     new_os = Order_status(status=el)
    #     db.session.add(new_os)
    #     db.session.commit()

    # for store in stores:
    #     new_store = User(login_name=store['login_name'], img_url=store['img_url'],store=True, store_name=store['store_name'])
    #     new_store.set_password(store['password'])
    #     db.session.add(new_store)
    #     db.session.commit()

    for user in users:
        new_user = User(login_name=user['login_name'], img_url=user['img_url'])
        db.session.add(new_user)
        db.session.commit()
    
    for x in range(0, 30):
        ran = random.randint(0, 10)
        ran_price = random.randint(1, 5)*1000
        new_product = Product(name=fruit_product[ran][0], discription=product_description[random.randint(
            0, 9)]['name'], img_url=fruit_product[ran][1], price=ran_price, category_id=1, user_owner_id=random.randint(1,9), stock=random.randint(100,200), time="2019/12/15", expired_date="2020/01/10", inventory_id=random.randint(1,2))
        db.session.add(new_product)
        db.session.commit()

    for x in range(0, 30):
        ran = random.randint(0, 7)
        ran_price = random.randint(1, 5)*1000
        new_product = Product(name=vegetable_product[ran][0], discription=product_description[random.randint(
            0, 9)]['name'], img_url=vegetable_product[ran][1], price=ran_price, category_id=2, user_owner_id=random.randint(1,9), stock=random.randint(100,200), time="2019/12/15", expired_date="2020/01/10", inventory_id=random.randint(1,2))
        db.session.add(new_product)
        db.session.commit()

    for x in range(0, 30):
        ran = random.randint(0, 4)
        ran_price = random.randint(1, 5)*1000
        new_product = Product(name=seasoning_product[ran][0], discription=product_description[random.randint(
            0, 9)]['name'], img_url=seasoning_product[ran][1], price=ran_price, category_id=3, user_owner_id=random.randint(1,9), stock=random.randint(100,200), time="2019/12/15", expired_date="2020/01/10", inventory_id=random.randint(1,2))
        db.session.add(new_product)
        db.session.commit()

    for rating in ratings:
        new_rating = Rating(rating=rating['rating'], comment=rating['comment'], user_id=rating['user_id'], product_id=rating['product_id'])
        db.session.add(new_rating)
        db.session.commit()
    return jsonify({'head' : 'success!'})
Spisać wymagania:  
  
Co będzie robił  
  Wykrywał czy osoba na nagraniu kamery je
Czego nie będzie robił:  
  Wykrywał czy osoba pije.
  Wykrywał co je osoba.
Diagramy UML:  

[[UML.canvas|UML]]

Gotowe sieci z klasy detection  

Wykrywanie jedzenia

| Model   | Liczba epok | mAP@0.5 | mAP@0.5:0.95 |
| ------- | ----------- | ------- | ------------ |
| YOLOv5s | 172         | 0.907   | 0.671        |
| YOLOv5m | 112         | 0.897   | 0.666        |
| YOLOv5l | 118         | 0.94    | 0.73         |
| YOLOv5x | 62          | 0.779   | 0.533        |
| YOLOv8s | 70          | 0.963   | 0.82         |
|         |             |         |              |
|         |             |         |              |
https://github.com/670669662/Yolov5-Human-Tracking
https://github.com/mrvackgl/food-detection-yolov5

Założenia, jakby to miało działać:  
	Wykrywałby człowieka
	Wykrywałoby jedzenie
	Oceniałoby czy jedzenie po prostu sobie leży, czy jest jedzone
Znaleźć przede wszystkim baze danych  

https://research.google.com/youtube8m/explore.html

https://storage.googleapis.com/openimages/web/visualizer/index.html?type=relationships&set=train&c=eat
| Dataset Name              | Food Category               | Total # Images/Class | Image Source                                    |
|---------------------------|-----------------------------|----------------------|-------------------------------------------------|
| UECFOOD-100               | Japanese Foods              | 14,361 (100)         | Captured by mobile camera                       |
| Food-101                  | American Foods              | 101,000 (101)        | Crawled from web                                |
| UECFOOD-256               | Japanese Foods              | 25,088 (256)         | Captured by mobile camera                       |
| UNCIT-FD1200              | Generic                     | 4754 (1200)          | Acquired using smartphone                       |
| UNCIT-FD889               | Italian Foods               | 3583 (899)           | Acquired with a smartphone                      |
| PFID                      | American Fast Foods         | 1038 (61)            | Fast food data captured in multiple restaurants |
| Vireo-Food 172            | Chinese Foods               | 110,241 (172)        | Downloaded from web                             |
| ChineseFoodNet            | Chinese dishes              | 192,000 (208)        | Gathered from web                               |
| Food-50                   | Japanese Foods              | 5000 (50)            | Crawled from web                                |
| Food-85                   | Japanese Foods              | 8500 (85)            | Existing food databases                         |
| Foodlog                   | Japanese Foods              | 6512 (2000)          | Captured by users                               |
| Turkish foods-15          | Turkish Dishes              | 7500/15              | Collected from other datasets                   |
| Pakistani Food Dataset    | Pakistani Dishes            | 4928 (100)           | Crawled from web                                |
| Indian Food Database      | Indian Foods                | 5000 (50)            | Downloaded from web                             |
| VegFru                    | Generic (Fruit and VEG)     | 160,731 (292)        | Collected from search engine                    |
| Fruits 360 Dataset        | Generic (Fruit)             | 71,125 (103)         | Camera                                          |
| FruitVeg-81               | Generic (Fruit and VEG)     | 15,630 (81)          | Collected using mobile phone                    |
| Wedge Shape foods dataset | American Foods              | 3 categories         | Controlled environment                          |
| TADA                      | Artificial And Generic Food | 256 (11)             | Controlled environment                          |
| FNDDS                     | American Foods              | 7000                 | Images of food acquired by users                |
| Chen                      | Chinese Foods               | 5000/50              | Crawled from the Internet                       |
| ETHZ Food-101             | American Foods              | 100,000 (101)        | Crawled from web                                |
| Rice dataset              | Generic (Rice)              | 1 food type          | Acquired from user                              |
| FOOD201-Segmented         | American Foods              | 12625                | Manually annotated dataset                      |
| UPMC Food-101             | Generic                     | 100,000 (101)        | Crawled from web                                |
| UNIMB 2015                | Generic                     | 2000 (15)            | Using a Samsung Galaxy S3 smartphone            |
| TADA(19 foods)            | American Foods              | 19 categories        | Controlled environment                          |
| Dishes                    | Chinese Restaurant Foods    | 117,504 (3832)       | Download from dianping                          |
| Menu-Match                | Generic Restaurant Food     | 646 (41)             | Captured from social media                      |
| Food-975                  | Chinese Foods               | 37,785 (975)         | Collected from restaurants                      |
| UNIMB 2016                | Italian Foods               | 1027 (73)            | Captured from dining tables                     |
| Food500                   | Generic                     | 148,408 (508)        | Crawled from web                                |
| Food-11                   | Generic                     | 16,643 (11)          | Other food datasets                             |
| ECUSTFD                   | Generic                     | 2978 (19)            | Acquired using smartphone                       |
| THFood-50                 | Thai Foods                  | 700/50               | Downloaded from web                             |
| FOOD524DB                 | Generic                     | 247,636 (524)        | Existing food database                          |
| FLD-469                   | Japanese Foods              | 209,700 (469)        | Smart Phone camera                              |
| FoodX-251                 | Generic                     | 158,000 (251)        | Collected from web                              |
| AI-Crowd                  | Swiss Foods                 | 25,389               | Volunteer Users                                 |
| EgocentricFood            | Generic                     | 5038 (9)             | Taken by a wearable egocentric vision camera    |
| MAFood-121                | Spanish Foods               | 21,175               | Google search engine                            |


  
python pytorch -> tensoflow  
  
Wybierz licencje
	MIT LICENSE
# DjangoProject-PrintingPlatforme
This large online platform, built using a microservices architecture, comprises two distinct domains: one for sellers and another for buyers. Throughout the development of this web application, I made a conscious effort to select the best technologies for each function. For communication between the backend and frontend, I utilized REST API for its superior performance. Additionally, I implemented GraphQL, a meta-library, to minimize frontend data overload. Finally, I utilized two different protocols, HTTP and WebSocket, to enable efficient and reliable notification handling. 
# How to start using this backend application 
1- Before cloning this repo you should start a virtual envirenment using : virtualenv venvname (in windows)<br>
2- Clone the app in the virtual env using : git clone https://github.com/grosvenor01/DjangoProject-PrintingPlatforme.git <br>
3- Go to the Scripts folder and aactivate the virtualenv <br>
4- Install all requirements from the rqts.txt file <br>
5- You can now access the revo_app folder and run the server, for runing the server you can use two methods the first one is run the command py manage.py runserver (the notification system will not work bcs he need asgi file excuted) , for runing the websocket protocole ( the graphql routes don't work gonna fi this one )  run : daphne revo_app.asgi:application (before runing this command you should install the redis server from this link : https://github.com/tporadowski/redis/releases after install it open new cmd prompt and run redis-server)
# API Documentation 
## GET http://lcalhost:8000/graphql/
you can specify the table you want get it for example : (you can check data base architecture to know the data you can get)<br>
Query{<br>
1-SellerById(id:{id}){<br>
  User{<br>
      username<br>
      email<br>
      }<br>
  seller_photo .... <br>
}<br>
2-PostById(id:{id}){<br>
}<br>
3-AllPosts{<br>
}<br>
4-OrdersBySellerId(id:{id}){<br>
}<br>
5-reviewsByPostId(id:{id}){<br>
}<br>
6-NotificationByRecieverId(id:{id}){<br>
}
}
## ws://localhost:8000/ws/notification/{room_name}/$
used to establish connection with websocket protocole for asyncrone notification system you should send reciever : id (reciever id), send : {sender id} (9oli nmdlk example kifah t9der dirha)
## POST http://lcalhost:8000/register/
This api is used to register or add a new user to the platforme 
### request example : 
{"username":"root","email":"root@gmail.com",password:"......."} ( in case of the user use the gmail or fb registration you should just send his username , email , and choose one of his data to use as password this data ou can get from google api response)
## POST http://lcalhost:8000/login/
This api is used to login a user and generate a token saved in the cookies of his browser this token is used each time when the user access to the platforme to not login evry time
in the case in the token is expired the user should re login 
### request example : 
{"username":"root",password:"......."} ( a token will sended and registred in the browser of the user and we will use it after to do all the rest of APIs )
## POST http://lcalhost:8000/seller/
managine the seller of the platforme like  create a seller accound , update it ... etc 
### request example : 
{
    "photo": null,
    "specialiste": "3D printing modeler",
    "available": "True",
    "address": "148 rue hassiba ben bouali",
    "phone": "+213799483879",
    "birthday": "2002-12-08",
    "sex": "Male",
    "description": "modeling senior",
    "skills": "modeling,3D printing,arduino,solide works",
    "reviews": 4
}
## PUT http://lcalhost:8000/seller/
### request example : 
{
"id":1,
"specialiste": "3D printer",
}
## POST http://lcalhost:8000/post/
to create new service from the sellers 
### request example : 
{ 
    "post_video" :null,
    "post_image" : null, 
    "post_title" : "the title",
    "post_description" :"the description",
    "materials" : "PLA (Polylactic Acid)",
    "post_keywords" :"some,keywords,separated,by,comma", 
    "maxSize_height" :54,
    "maxSize_width" :54,
    "nb_reviews" : 100,
    "free_delivery" :"Available", 
    "return_delivery" :"Available"
}<br>
for some field there is specific data should be send here is it the column and the specific data : 
materiels : 
![materiels](https://github.com/grosvenor01/DjangoProject-PrintingPlatforme/assets/96534255/5b4c4782-5608-45f1-8b20-c5d2fffb08de)<br>
free_delivery & return_delivery : <br>
![delivery](https://github.com/grosvenor01/DjangoProject-PrintingPlatforme/assets/96534255/af28ce9c-05be-4e98-90f1-6f96361a5317)
## PUT http://lcalhost:8000/post/
### request example : 
{
    "id":1,
    "free_delivery" :"Not available"
}<br>
## DELETE http://lcalhost:8000/post/
### request example :
{
    "id" :1
}<br>
## POST http://lcalhost:8000/order/
Ths api is used to manage orders , create one , .... follow te status of it each time ... etc 
### request example : 
{ 
    "seller" : 1,
    "location" : "148 rue address",
    "total_amount" : 162.23,
    "status" : "pending"
}
## PUT http://lcalhost:8000/order/
### request example : 
{
"id":1,
"status" : "shipped"
}
## GET http://lcalhost:8000/statistics/
used for the dashboard data 

## POST http://lcalhost:8000/post/reviews/
### request example : 
{
    "rating":3,
    "text":"here we dont go ",
    "post":2 (post id)
}
## PUT http://lcalhost:8000/post/reviews/
### request example : 
{
    "text":"here we go ",
}
## DELETE http://lcalhost:8000/post/reviews/
### request example : 
{
    "id":2,
}
## GET http://lcalhost:8000/recomandation/sellers/
### request example : 
{
}


Loyiha tavsifi
    
    Online Driver loyihasi – bu ikki turdagi foydalanuvchi tizimi: Driver va Client asosida ishlaydigan oddiy zakaz boshqaruv tizimi.

    Userlar bitta telefon raqam bilan 2 ta role orqali register qilish imkoniyani mavjud.
    
    Driver: ishga tayyor bo‘lganda online holatiga o‘tadi, zakaz qabul qilgach busy bo‘ladi va ish tugagach offline holatiga qaytadi.
    
    Client: ilovada zakaz yaratadi va mavjud bo‘lgan online va bo‘sh driverlardan biri zakazga biriktiriladi.
    
    Order statuslari: minimal ravishda quyidagilar ishlatiladi: CREATED → ASSIGNED → COMPLETED.
    
    Real-time yangilanishlar: Driver va client o‘zlarining holatlari va order xabarlarini WebSocket orqali oladi.
    
    Loyiha Docker orqali containerlarda ishga tushiriladi, PostgreSQL bazasi va Redis Channels uchun ishlatiladi.





Loyihani ishga tushirish bo'yicha ko'rsatmalar:
1. Clone olish
    git clone https://github.com/FarhodGanijonov/Driver.git

2. Venv muhitini yaratish va requirements.txt file orqali kutubxonalarni o'rnatish:
      python3 -m venv venv 

    Pip ni yangilash:
      python -m pip install --upgrade pip

   Requirements.txt file ni install qilish:
        pip install -r requirements.txt

3. Loyihani docker container yordamida ishga tushirish:

      Container va image yaratish:
          docker-compose build

     Containerlarni ishga tushirish:
         docker-compose up -d

     Container ishga tushganligini ko'rish:
          docker ps

     Container id si orqali containerga kirib superuser yaratish yani admin panel uchun login parol yaratish:

         docker exec -it myproject_container /bin/bash

         python manage.py createsuperuser

         va login parol yaratasiz oynasi ochiladi yaratib qoyasiz.

   Containerdan chiqasiz:

        exit 

4. Loyiha localda run qilingan bolsa swagger ni brauzerda ochish:

        http://127.0.0.1:8021/swagger/



5. Endpointlar royxati:

       1. Register driver or client: JWT token talab qilinadi
              http://127.0.0.1:8021/users/register/<role>/

       2. Login driver or client: JWT token talab qilinadi
              http://127.0.0.1:8021/users/login/<role>/

       3. Client order create api: JWT token talab qilinadi
              http://127.0.0.1:8021/client/order/create/

       4. Client order list va list filter status EXAMPLE: "?status=completed": JWT token talab qilinadi
              http://127.0.0.1:8021/client/order/list/

       5. Client order detail get: JWT token talab qilinadi
              http://127.0.0.1:8021/client/orders/order_id/

       6. Client o'zini statusini update qilishi mumkin faqat: JWT token talab qilinadi
              http://127.0.0.1:8021/client/client_id/status/
              
       7. Driver statusni o'zi boshqarishi uchun api: JWT token talab qilinadi
              http://127.0.0.1:8021/driver/driver_id/status/

       8. Client online driverlar listini korish uchun api: JWT token talab qilinadi
              http://127.0.0.1:8021/driver/online/  


6. Websocker API 

       1. Driver userlar uchun websocket ga ulanish api: Headers orqali Bearer token bilan websocketga ulanadi:
              ws://127.0.0.1:8021/ws/driver/

       1. Client userlar uchun websocket ga ulanish api: Headers orqali Bearer token bilan websocketga ulanadi:
              ws://127.0.0.1:8021/ws/client/   





Konfiguratsiya talablari

    Python: 3.10
    
    Django: 4.2.10
    
    Django REST Framework: 3.16.1
    
    Redis: 7.1.0 (Channels uchun)
    
    Django Channels: 4.3.2
    
    Daphne: 4.2.10 (ASGI server WebSocket ishlatish uchun)
    
    PostgreSQL: 14+ (GeoDjango uchun PointField ishlatiladi)
    
    WebSocket: Driver va client real-time status va order xabarlari uchun Channels orqali ishlatiladi
    

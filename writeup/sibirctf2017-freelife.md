---
title: Neo's Fun - Write Up SibirCtf2017 freelife
---

# SibirCtf2017 freelife

Нам дан сервис на Django. Разбираем его.  
После просмотра кофигурации и содержимого сайта, меняем дефолный пароль на суперпользователя в админке.
(Который создатся при импорте `main/static/catch.py`)  
В админке смотри Main -> Infos.  
Много email'ов. Пример одного из:  
![alt](/files/sibirctf2017-freelife_screen_user.png)  
`ccn` - похож на флаг.  
Дальше разбираем сервис.  
Что ещё бросается в глаза - это файл `main/view.py`.  
А точнее странная обработка исключения.  

```python
email = request.POST.get('email')
name = request.POST.get('name')
address = request.POST.get('address')
ccn = request.POST.get('ccn')
phone = request.POST.get('phone')
data = Info.objects.filter(email=email)

if data.count() > 0:
        return render(request, 'member.html', {"data":data.values()})
try:
    Info.objects.create(
            email=email,
            name=name,
            address=address,
            ccn=ccn,
            phone=phone)
except:
    data = Info.objects.filter()
    return render(request, 'member.html', {"data":data.values()})
```

`Info` - это модель, через которую общается django с бд.  
Вызов `Info.objects.create` вставляет в неё новую строку. Вставка может провалиться, если подали невалидные данные.  
Теперь посмотрим `member.html`.  

```html
{ % for i in data % }
<table class='table table-hover'>
  <tr>
    <td>email</td>
    <td>{ {i.email} }</td>
  </tr>
  <tr>
    <td>name</td>
    <td>{ {i.name} }</td>
  </tr>
  <tr>
    <td>address</td>
    <td>{ {i.address} }</td>
  </tr>
  <tr>
    <td>name</td>
    <td>{ {i.name} }</td>
  </tr>
  <tr>
    <td>phone</td>
    <td>{ {i.phone} }</td>
  </tr>
  <tr>
    <td>ccn</td>
    <td>{ {i.ccn} }</td>
  </tr>
{ % endfor % }
```

Цикл, значит страница может отображать много записей.  
Вернёмся к БД.  
Смотрим описание таблицы main_info в sqlitebrowser:  
![alt](/files/sibirctf2017-freelife_screen_db.png)  
Чтобы выполнился код обработки исключения нужно: отправить не GET запрос или нулевое значение поля (если запрос по POST).  
Поэтому отправляем запрос с методом PUT ( или другим не GET, POST или HEAD ).  
`curl -X PUT http://192.168.1.6:8000/contact`  
И получаем все записи на текущим момент.  
Убираем обработку исключений - закрываем уязвимость.  
Теперь осталось написать скрипт, например [такой](/files/sibirctf2017-freelife_script.py).  
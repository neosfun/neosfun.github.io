---
title: Neo's Fun - Write Up SibirCtf2018 Thefakebook
---

# SibirCTF2018 Thefakebook

## Обзор

Все команды получили виртуальную машину с уязвимыми сервисами, которые самостоятельно стартовались при запуске.

![alt](/files/thefakebook/01_index_page.png)

Сервис Thefakebook работал на 8000 порту, а исходники лежали в директории `/home/user/thefakebook`. Структура сервиса выглядела так:

- core/
	- static/
	- templates/
	- \_\_init\_\_.py
	- admin.py
	- apps.py
	- models.py
	- school\_schoices.py
	- test.py
	- views.py
- thefakebook
	- \_\_init\_\_.py
	- settings.py
	- urls.py
	- wsgi.py
- Dockerfile
- manage.py
- requirements.txt

Нас интересует файл views.py, т.к. в нем расположена основная логика приложения. Осложняет анализ обфусцированный код.

## Деобфускация

### Подготовка

Чтобы отделить функции друг от друга можно воспользоваться утилитой autopep8

```bash
sudo pip3 install autopep8
autopep8 views.py > views_pep8.py
```

С помощью функции поиск-замена вашего любимого текстового редактора, заменяем названия переменных на изначальные, например есть код 
```python
from django.db.models import Q as Я
from django.contrib.auth.models import User as ʼʽʾʿ

from django.contrib.auth.decorators import login_required as Декоратор_гыг
from core.models import Profile as ݒݓݔ
from core.models import AccountInfo as ɾɿ
from core.models import BasicInfo as ఋఌఱశಣಹఋೲ
from core.models import ContactInfo as ಅಘౙపఠಖనల
```

Заменяем все строки в файле:

- Я -> Q
- `ݒݓݔ` -> User
- Декоратор_гыг -> login_required
- и т.д. 

Следующие названия переменных тоже можно заменить

```python
ۮۯۺۻۼ = dict
ಈಈಗడಒಯಱಜ = Friendship
నథಉఓಬಔಠಯ = Message
```

### Деобфускация на примере функции `messages_view`

```
@login_required
@JUST_DO_IT
def messages_view(ߪߩߨٴʹ, profile_id):
    ХочетсяСмеятСЯ = Profile.objects.filter(id=profile_id)
    if not ХочетсяСмеятСЯ or ХочетсяСмеятСЯ.first() == ߪߩߨٴʹ.user.profile:
        raise Http404("ʼʽʾʿ does not exist")
    ХочетсяСмеятСЯ = ХочетсяСмеятСЯ.first()
    if ߪߩߨٴʹ.method == "POST":

        title = ߪߩߨٴʹ.POST.get("subject", "<no subject>")
        body = ߪߩߨٴʹ.POST.get("text", "")
        Message.objects.create(message_from=ߪߩߨٴʹ.user.profile, message_to=ХочетсяСмеятСЯ,
                               created=datetime.datetime.now(), title=title, body=body)
    username = ߪߩߨٴʹ.user.profile.account_info.name
    messages_query = Message.objects.filter(Я(Я(message_from=ߪߩߨٴʹ.user.profile) | Я(message_to=ߪߩߨٴʹ.user.profile) | Я(
        message_to__account_info__name=ߪߩߨٴʹ.user.profile.contact_info.about_me))).filter(Я(message_from=ХочетсяСмеятСЯ) | Я(message_to=ХочетсяСмеятСЯ))
    Message.objects.filter(message_from=ХочетсяСмеятСЯ,
                           message_to=ߪߩߨٴʹ.user.profile).update(readed=True)
    messages = [{"profile": {"id": message.message_from.id, "name": message.message_from.account_info.name, "avatar": get_avatar_url(message.message_from)},
                 "time": message.created, "title": message.title, "body": message.body} for message in messages_query]
    data = {'username': username, "user": ߪߩߨٴʹ.user,
            "friend_name": ХочетсяСмеятСЯ.account_info.name, "messages": messages}
    return render(ߪߩߨٴʹ, 'aftersignin/viewmessages.html', data)
```

Заменяем переменные по контексту и делаем удобные для нашего понимания переносы. Должно в итоге быть как то так:

```
@login_required
@JUST_DO_IT
def messages_view(request, profile_id):
    target_profile = Profile.objects.filter(id=profile_id)

    if not target_profile or target_profile.first() == request.user.profile:
        raise Http404("User does not exist")

    target_profile = target_profile.first()

    if request.method == "POST":
        title = request.POST.get("subject", "<no subject>")
        body = request.POST.get("text", "")
        Message.objects.create(message_from=request.user.profile, message_to=target_profile,
                               created=datetime.datetime.now(), title=title, body=body)

    username = request.user.profile.account_info.name

    messages_query = Message.objects.filter(
        Q(
            Q(message_from=request.user.profile) |
            Q(message_to=request.user.profile) |
            Q(message_to__account_info__name=request.user.profile.contact_info.about_me)
        )
    ).filter(
        Q(message_from=target_profile) |
        Q(message_to=target_profile)
    )

    Message.objects.filter(message_from=target_profile,
                           message_to=request.user.profile).update(readed=True)

    messages = [
        {
            "profile":
                {
                    "id": message.message_from.id,
                    "name": message.message_from.account_info.name,
                    "avatar": get_avatar_url(message.message_from)
                },
            "time": message.created,
            "title": message.title,
            "body": message.body
        } for message in messages_query
    ]

    data = {
        'username': username,
        "user": request.user,
        "friend_name": target_profile.account_info.name,
        "messages": messages}

    return render(request, 'aftersignin/viewmessages.html', data)
```

Код из-за переносов может перестать работать, однако нам нужно всего-лишь разобраться в коде, найти уязвимость и исправить. Обфусцировать боевой сервис вовсе не обязательно.

### Разбор функционала `messages_view`

Пытаемся понять, что делает каждая конструкция:

```python
@login_required
@JUST_DO_IT
def messages_view(request, profile_id):
    # Фильтруем всех пользователей (профили) с id == profile_id
    target_profile = Profile.objects.filter(id=profile_id)

    # Если не нашли или profile_id наш, возвращаем ошибку
    if not target_profile or target_profile.first() == request.user.profile:
        raise Http404("User does not exist")

    # target_profile - найденный профиль
    target_profile = target_profile.first()

    # Если было получено сообщение, добавляем его в бд
    if request.method == "POST":
        title = request.POST.get("subject", "<no subject>")
        body = request.POST.get("text", "")
        Message.objects.create(message_from=request.user.profile, message_to=target_profile,
                               created=datetime.datetime.now(), title=title, body=body)

    # Наш username
    username = request.user.profile.account_info.name

    # Фильтруем сообщения, чтобы выводить только нужные
    messages_query = Message.objects.filter(
        Q(
            Q(message_from=request.user.profile) |
            Q(message_to=request.user.profile) |
            Q(message_to__account_info__name=request.user.profile.contact_info.about_me)
        )
    ).filter(
        Q(message_from=target_profile) |
        Q(message_to=target_profile)
    )
    
    # "Прочитываем" пришедшие сообщения .update(readed=True) 
    Message.objects.filter(message_from=target_profile,
                           message_to=request.user.profile).update(readed=True)

    # Придаем сообщениям необходимую структуру
    messages = [
        {
            "profile":
                {
                    "id": message.message_from.id,
                    "name": message.message_from.account_info.name,
                    "avatar": get_avatar_url(message.message_from)
                },
            "time": message.created,
            "title": message.title,
            "body": message.body
        } for message in messages_query
    ]
    
    # Необходимые для шаблона html данные
    data = {
        'username': username,
        "user": request.user,
        "friend_name": target_profile.account_info.name,
        "messages": messages}

    # Возвращаем html страницу
    return render(request, 'aftersignin/viewmessages.html', data)
```

### Подозрительная конструкция

```
messages_query = Message.objects.filter(
    Q(
        Q(message_from=request.user.profile) |
        Q(message_to=request.user.profile) |
        Q(message_to__account_info__name=request.user.profile.contact_info.about_me)
    )
).filter(
    Q(message_from=target_profile) |
    Q(message_to=target_profile)
)
```

Про Q объекты можно почитать тут [django making queries](https://docs.djangoproject.com/en/2.1/topics/db/queries/) раздел "Complex lookups with Q objects".

По-хорошему мы должны получить сообщения, которые мы отправили собеседнику или собеседник отправил нам, однако в конструкции лишнее условие `Q(message_to__account_info__name=request.user.profile.contact_info.about_me)`.

Условие означает примерно следующее: "Имя получателя сообщения = информации в about me текущего пользователя (под которым мы авторизировались)".

## Эксплуатация уязвимости

### Выбираем цель

user_dd432b0c2

![alt](/files/thefakebook/03_users.png)

### Изменяем информацию своего профиля

![alt](/files/thefakebook/04_profile_edit.png)

### Переходим по ссылке `/messages/<target_id>`

![alt](/files/thefakebook/05_flag.png)

Сдаем найденный флаг.

## Вместо итога

Целью сервиса Thefakebook было показать, что обфускация программного кода не панацея, а скорее способ испугать человека, который будет этот код разбирать.

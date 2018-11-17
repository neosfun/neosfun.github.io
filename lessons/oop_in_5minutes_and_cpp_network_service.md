---
title: Neo's Fun - ООП за 5 минут и сетевой сервис на c++
---
# Базовые термины

* Полиморфизм
* Наследование
* Инкапсуляция

Помним всегда что полиморфизм без наследования не возможен (во всяком случае в c++).

## ООП за пять минут.

1. У нас есть объекты из одного класса области (например фрукты).
2. У каждого объекта есть имя (или тип) и набор параметров: (апельсин: оранжевый и кислый, помидор: красный и сочный)
3. Для более удобной обработки мы хотим сложить все объекты в один массив (это только один шаблонов использования)

Теперь опишем базовый класс

```
Класс Фруктоовощ:
    имя(): строка, по умолчанию "";
    сорт(): строка, по умолчанию "";
    какого_он_цвета(): строка, по умолчанию "";
    он_кислый(): число, по умолчанию 0; # 0-10
    он_сладкий(): число, по умолчанию 0; # 0-10
    он_горький(): число, по умолчанию 0; # 0-10
    на_складе(): число, по умолчанию 0; # 0-10
    ... и тд.
    скрыть переменную А = 0;
```

Далее опишем несколько классов наследуя их от Фркутоовощ

**класс Мандарин_Морокко**
```
Класс Мандарин_Морокко от Фруктоовощ:
    имя(): вернуть "Мандарин";
    сорт(): вернуть "Морокко";
    какого_он_цвета(): вернуть "оранжевый";
    он_кислый(): вернуть 2;
    он_сладкий(): вернуть А + 8;
    на_складе(): вернуть 10;
```

**класс Мандарин_Китайский**
```
Класс Мандарин_Китайский от Фруктоовощ:
    имя(): вернуть "Мандарин";
    сорт(): вернуть "Китайский";
    какого_он_цвета(): вернуть "оранжевый";
    он_кислый(): вернуть 3;
    он_сладкий(): вернуть 5;
    на_складе(): вернуть 20;
```

**класс Апельсин1**
```
Класс Апельсин1 от Фруктоовощ:
    имя(): вернуть "апельсин";
    сорт(): вернуть "1";
    какого_он_цвета(): вернуть "оранжевый";
    он_кислый(): вернуть 7;
    он_сладкий(): вернуть 3;
    он_горький(): вернуть 1;
    на_складе(): вернуть 5;
```

**класс Помидор**
```
Класс Помидор от Фруктоовощ:
    имя(): вернуть "помидор";
    сорт(): вернуть "ачинский";
    какого_он_цвета(): вернуть "красный";
    он_сладкий(): вернуть 2;
    на_складе(): вернуть 100;
```

Теперь опищем основной алгоритм, например для поиска самого сладкого фрукта:

```
Массив фо[]: Фруктоовощ;
фо[0] = создать Мандарин_Морокко;
фо[1] = создать Мандарин_Китайский;
фо[2] = создать Апельсин1;
фо[3] = создать Помидор;

индекс_самого_сладкого_фрукта = -1
значение_сладости = 0

цикл индекс от 0 до 3:
    если фо[индекс].он_сладкий() больше чем значение_сладости:
        значение_сладости = фо[индекс].он_сладкий()
        индекс_самого_сладкого_фрукта = индекс

если индекс_самого_сладкого_фрукта > 0:
    распечатать фо[индекс_самого_сладкого_фрукта]
```

Теперь где здесь что:

* `Фруктоовощ` - это базовый класс или класс-родитель
* `Мандарин_Морокко`, `Мандарин_Китайский`,...  - это дочерний класс или класс-потомок
* `Класс Помидор от Фруктоовощ` - это и есть наследование то есть у дочернего класса есть все методы что и у родительского
* `он_сладкий(): вернуть А + 8;` - При наследование свойства объекта инкапсулируеются то есть в дочернем объекте есть все такие же свойства. Нуу и нет необходимости определять какие то методы - так как они уже есть (!)
* `имя()`, `сорт()`, `какого_он_цвета()`, ... - это полиморфные методы то есть в дочерних классах их можно переопределить (поменять/подменить реализацию)


В этом примере есть все три основных свойства ООП - полиморфизм, наследование, инкапсуляция.

* полиморфизм - возможность менять реализацию в дочернем классе некоторых методов.
* наследование - возможность наследовать свойства и методы от определенного класса.
* инкапсуляция - данные и методы их обработки содержаться вместе.

## Далее попробуем соорудить что нить полезное с использвоанием ООП

1. Это будет сетевой сервис
2. Консольное приложение
3. Общей буффер для все подключений простое игровое поле
4. И много разных комманд для управления игровым полем

[Source Code](/files/oop_in_5minutes_and_cpp_network_service.zip)

Или

[https://github.com/neosfun/neos_fun_game_service](https://github.com/neosfun/neos_fun_game_service)

### Для начала опишем класс игрового поля (`neos_fun_game.h`):
```
class NeosFunGame {
    public:
        NeosFunGame();
        std::string playingField();
        int width();
        int height();
        void setValue(int nX, int nY, std::string sColor, std::string sCharacter);
    private:
        std::string m_sBGRed;
        std::string m_sBGBlue;
        std::string m_sBGReset;
        int m_nWidth;
        int m_nHeight;
        std::vector<std::string> m_vFields;
};
```
Реализация в файле: `neos_fun_game.cpp`


### Базовый класс будет выглядеть так (`base_handler.h`):

```
class BaseHandler {
    public:
        BaseHandler(NeosFunGame *pGame); // constructor
        virtual std::string command(); // name of command
        virtual std::string usage(); // usage
        virtual std::string description(); // description
        virtual std::string handle(std::vector<std::string> &vArgs); // execute (handle) this command
        NeosFunGame *game();
    private:
        NeosFunGame *m_pGame;
};
```

*Слово `virtual` - означает что дочерний класс может изменить реализацию у себя*

### Пример наследования (`game_handler.h`):

```
#include "base_handler.h"

class GameHandler : public BaseHandler {
    public:
        GameHandler(NeosFunGame *pGame); // constructor
        virtual std::string command(); // name of command
        virtual std::string usage(); // usage
        virtual std::string description(); // description
        virtual std::string handle(std::vector<std::string> &vArgs); // execute (handle) this command
};
```

### Собственно пример реализации (`game_handler.cpp`):

```
#include "game_handler.h"

GameHandler::GameHandler(NeosFunGame *pGame) : BaseHandler(pGame) {
    std::cout << "GameHandler created " << std::endl;
}

std::string GameHandler::command() {
    return "game";
}

std::string GameHandler::usage() {
    return "";
}

std::string GameHandler::description() {
    return "print game fields";
}

std::string GameHandler::handle(std::vector<std::string> &vArgs) {
    return game()->playingField();
}

```

*Так как конструктор родительского класса имеет аргументы на входе значит мы должны в любом конструкторе дочернего класса сделать вызов конструктора родительского класса: ` : BaseHandler(pGame)`*

*В методе `GameHandler::handle` можно обратить внимание на вызов метода `game()` родительского класса (пример инкапсуляции)*


Пример `main.cpp`:

```
#include "tcp_ip_server.h"
#include "time_handler.h"
#include "game_handler.h"
#include "set_handler.h"

int main() {
    NeosFunGame *pGame = new NeosFunGame();

    TCPIPServer *pServer = new TCPIPServer();
    pServer->registerHandler(new TimeHandler(pGame));
    pServer->registerHandler(new GameHandler(pGame));
    pServer->registerHandler(new SetHandler(pGame));
    
    int nPort = 3333;
    pServer->start(nPort); // will wait finish
}
```

При вызове `pServer->registerHandler(new GameHandler(pGame));` происходит следующее:

* `new GameHandler(pGame)` - создается экземпляр класса `GameHandler` (на вход подается указатель на ранее соззданный экземпляр класса `NeosFunGame`)
* на вход метода `registerHandler` подается указатель на экземпляр класса`GameHandler` хотя тот в свою очередь принимает указатель на `BaseHandler` - в этом случае происходит автоматическое приведение типов так как `GameHandler` наследован от `BaseHandler` и соответсвенно ошибок не возникает

### Немного про приведение типов

Впринципе строку `pServer->registerHandler(new GameHandler(pGame));` можно расписать примерно так:

```
// создаем экземпдяр класса GameHandler
GameHandler *pGameHandler = new GameHandler(pGame);

// приводим его к родительскому типу (кастим или cast)
BaseHandler *pGameLikeBaseHandler = static_cast<BaseHandler *>(pGameHandler);

// регистрируем в списке команд
pServer->registerHandler(pGameLikeBaseHandler);

```
При этом если сделать вызов `pGameLikeBaseHandler->command()` то нам вернется строка `"game"`


### Как регистриуются обработчики команд на сервере

*См. файл `tcp_ip_server.h` и `tcp_ip_server.cpp`*

Но если вкратце то достаточно просто - испольуем map (ассоциированный массив):

Где то в members класса можно найти определение:

`std::map<std::string, BaseHandler *> m_mapHandlers;`

А уже в реализации метода `registerHandler`
```
void TCPIPServer::registerHandler(BaseHandler *pHandler) {
    ...
    m_mapHandlers[sName] = pHandler;
    ...
}
```

То есть по сути у нас каждой команде соответвует свой обработчик.

### Как вызывается обработчик

В сервеном класса есть метод `findHandler` он ищет `m_mapHandlers` по имени команды если не находит то возвращает NULL иначе указатель на экземпляр класса обработчика.

```
BaseHandler *TCPIPServer::findHandler(const std::string &sCommand) {
	std::map<std::string, BaseHandler *>::iterator it = m_mapHandlers.find(sCommand);
	if (it != m_mapHandlers.end()) {
		return it->second;
	}
	return NULL;
}
```

Где то в отдельном треде:

```
BaseHandler *pHandler = pInfo->server()->findHandler(sCommand);
if (pHandler != NULL) {
    sResponse = pHandler->handle(vArgs);
} else {
    sResponse = "Not found command '" + sCommand + "', please try 'help'";
}
```

Собственно ищем обработчик - если нашли вызываем у него метод `handle` если нет такого то "Not found..."

Например если была команда `"game"` вызовится вот этот вот обработчик (`game_handler.cpp`):

```
std::string GameHandler::handle(std::vector<std::string> &vArgs) {
    return game()->playingField();
}
```

### Архив с исходниками

[Source Code](/files/oop_in_5minutes_and_cpp_network_service.zip)

Или

[https://github.com/neosfun/neos_fun_game_service](https://github.com/neosfun/neos_fun_game_service)

* Для сборки вам потребуется g++
* Внутри проекта есть `build.sh` скрипт для сборки (А такие штуки как Makefile, CMakeLists.txt - в другой раз)

Для гуру сборщиков из командной строки продублирую команду для сборки:

```
g++ -std=c++0x \
    -pthread \
    -I src/ \
    src/main.cpp \
    src/neos_fun_game.cpp \
    src/base_handler.cpp \
    src/time_handler.cpp \
    src/game_handler.cpp \
    src/set_handler.cpp \
    src/tcp_ip_server.cpp \
    -o neos_fun_game_service # ouput file
```

Нуу и подключаемся через с помощью `nc`:

```
$ nc localhost 3333
```

### Заключение

Используя принципы наследовани, полимормизма и инкапсуляции была написан небольшой сетевой сервис.

В чем приимущества подхода ООП:

1. можно добавлять команды отдельно друг от друга (ну и поручить разными разработчиками это сделать)
2. Если правильно подготовить арзхитектуру то в разы ускоряется разработка любого проекта
3. Переиспользвоание/Модульность кода - если вам вдруг понадобиться выполнять команды без сервера (например при чтении из файла) - не проблема убирем tcp_ip_server и пишем транслятор команд из файла
4. Если вы решили что нужно прикрутить web то тоже не проблема - меняем tcp_ip_server на http server
5. Ненравиться концепт игры? - можно менять тестировать его отдельно от остального.

*По поводу остальных плюшек - это уже другая история*

### Индивидуальные задания 

Все исходники здесь [https://github.com/neosfun/neos_fun_game_service](https://github.com/neosfun/neos_fun_game_service)

* Добавить конмаду `clean` - зануление поля
* Добавить команду `text` - вывод текста (а не только один символ)
* Добавить команду `rect` - заполнение прямоугольника
* Добавить команду `circle` - заполнение круга
* Добавить команду `line_x` - прорисовка горизонтальной линии
* Добавить команду `line_y` - прорисовка вертикальной линии

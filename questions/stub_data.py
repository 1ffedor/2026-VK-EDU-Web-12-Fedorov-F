def _answers_label(count):
    n = count % 100
    if 11 <= n <= 14:
        word = 'ответов'
    else:
        m = count % 10
        if m == 1:
            word = 'ответ'
        elif 2 <= m <= 4:
            word = 'ответа'
        else:
            word = 'ответов'
    return f'{count} {word}'


def votes_noun(n):
    n = abs(int(n)) % 100
    if 11 <= n <= 14:
        return 'голосов'
    m = n % 10
    if m == 1:
        return 'голос'
    if 2 <= m <= 4:
        return 'голоса'
    return 'голосов'


_RAW_QUESTIONS = [
    {
        'title': 'Yii2, как обработать с формы POST массив данных для сохранения в БД?',
        'text': 'Модель ActiveRecord, в правилах указал safe для полей-массива, но после submit приходит не то, что ожидаю. Как правильно биндить и валидировать?',
        'tags': ['php', 'yii2'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 2 минуты назад',
        'answers_bold': False,
    },
    {
        'title': 'Компоновка виджетов Qt Designer',
        'text': 'На форме несколько QGroupBox и кнопки «плывут» при ресайзе. Как зафиксировать раскладку через layout-ы, чтобы в рантайме всё выглядело как в дизайнере?',
        'tags': ['cpp', 'qt', 'qt-designer'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '65 показов',
        'author': '0xdb',
        'author_rep': '52.2k',
        'time_ago': 'изменён 7 минут назад',
        'answers_bold': False,
    },
    {
        'title': 'Как заставить бота отвечать на неизвестную команду?',
        'text': 'Aiogram 3: хендлеры на команды есть, но если пользователь ввёл что-то лишнее, бот молчит. Нужен fallback и понятное сообщение.',
        'tags': ['python', 'aiogram'],
        'votes': 0,
        'answers_count': 2,
        'views_label': '1k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 1 час назад',
        'answers_bold': True,
    },
    {
        'title': 'Python: добавить элемент в список как insert, без встроенных list.insert и срезов',
        'text': 'Задача олимпиадная: реализовать вставку по индексу вручную за O(n). Границы индекса и пустой список — как оформить краевые случаи?',
        'tags': ['python', 'list', 'olympiad', 'insert'],
        'votes': 2,
        'answers_count': 1,
        'views_label': '134 показа',
        'author': 'Vitalizzare',
        'author_rep': '4,160',
        'time_ago': 'изменён 1 час назад',
        'answers_bold': False,
    },
    {
        'title': 'Качество кода и архитектуры: Service and Repository pattern в PHP и Laravel',
        'text': 'Где проводить границу между сервисом и репозиторием, что оставить в контроллере, и как не раздуть слои на типовом CRUD?',
        'tags': ['php', 'laravel', 'code-style'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '922 показа',
        'author': 'Confireus',
        'author_rep': '530',
        'time_ago': 'ответ дан 1 час назад',
        'answers_bold': False,
    },
    {
        'title': 'Ошибка при git push -u: failed to push some refs to…',
        'text': 'Первый push в новый репозиторий, ветка main. Удалённая история не совпадает с локальной. Что безопасно сделать: pull --rebase или force?',
        'tags': ['git', 'github', 'version-control'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '921 показ',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 2 часа назад',
        'answers_bold': False,
    },
    {
        'title': 'Установщики (Minecraft, .NET Framework) не видят интернет, хотя браузер работает',
        'text': 'Windows 10, прокси отключён, антивирус пробовал выключать. Часть программ качает обновления, установщики — «нет соединения».',
        'tags': ['windows', 'install', 'minecraft'],
        'votes': 0,
        'answers_count': 0,
        'views_label': '18 показов',
        'author': 'Dev18',
        'author_rep': '3,144',
        'time_ago': 'изменён 2 часа назад',
        'answers_bold': False,
    },
    {
        'title': 'MODX API MiniShop2: создать категории и товары из кода',
        'text': 'Нужен скрипт/сниппет: массовое создание категорий и привязка товаров. Документация разрозненная — с чего начать в ms2?',
        'tags': ['api', 'modx', 'minishop2'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '920 показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 3 часа назад',
        'answers_bold': False,
    },
    {
        'title': 'Laravel: валидация — хотя бы одно из полей обязательно должно быть заполнено',
        'text': 'Два optional-поля, но нельзя отправить форму, если оба пустые. Как правило в FormRequest или кастомное after-правило?',
        'tags': ['php', 'laravel'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 4 часа назад',
        'answers_bold': False,
    },
    {
        'title': '1С 8.3 (управляемое): цвет строки товара в табличной части при изменении количества',
        'text': 'Нужно подсветить строку условным оформлением или программно в модуле формы. Производительность при большом списке не должна просесть.',
        'tags': ['1c'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 5 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Клавиатура в боте VK (Python, vk_api)',
        'text': 'Отправляю keyboard JSON, в приложении VK кнопки не появляются или не нажимаются. Версия API и peer_id проверил.',
        'tags': ['python', 'vk-api', 'vk'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '3k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 6 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Как сделать автовоспроизведение видео со звуком (без muted) в HTML?',
        'text': 'Браузеры блокируют autoplay со звуком. Есть ли легальные обходы для пользовательского клика или только muted + кнопка unmute?',
        'tags': ['javascript', 'html', 'css', 'video'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '921 показ',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 7 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Как использовать сессии в Django?',
        'text': 'SESSION_ENGINE, cookies, CSRF и redirect после логина — базовый чеклист для начинающих. Где хранить cart для гостя?',
        'tags': ['python', 'django', 'cookie', 'session'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 9 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Дергается элемент с position: fixed в Safari',
        'text': 'При скролле с адресной строкой, скрывающейся на iOS, fixed-хедер подпрыгивает. Есть ли стабильный фикс в 2025–2026?',
        'tags': ['html', 'css', 'safari'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 9 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'После create-react-app в консоли: [HMR] Waiting for update signal from WDS',
        'text': 'Сообщение не ошибка, но хочу понять, нормально ли это и как отключить лишний шум в dev.',
        'tags': ['webpack', 'react', 'javascript'],
        'votes': 0,
        'answers_count': 2,
        'views_label': '21k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 11 часов назад',
        'answers_bold': True,
    },
    {
        'title': 'При подключении к AmneziaVPN пропадает интернет',
        'text': 'Маршрут по умолчанию уезжает, split tunneling не очевиден. Как диагностировать на Windows и что проверить в логах OpenVPN?',
        'tags': ['openvpn', 'vpn', 'windows'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '980 показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 12 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Телеграм-бот: создавать задачи в Битрикс24',
        'text': 'Нужен OAuth или входящий вебхук, какие права у приложения и как не светить токен в коде бота?',
        'tags': ['telegram-bot', 'bitrix', 'bitrix24'],
        'votes': 1,
        'answers_count': 2,
        'views_label': '28 показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 13 часов назад',
        'answers_bold': True,
    },
    {
        'title': 'Почему Stream.max() возвращает Optional и как получить Stream<MyClass>?',
        'text': 'Терминальная операция и пустой стрим — понятно, но как дальше продолжить цепочку без лишних if везде?',
        'tags': ['java', 'java-stream', 'optional'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '4k показов',
        'author': 'Nowhere Man',
        'author_rep': '18.9k',
        'time_ago': 'изменён 13 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Вылетает из всех сессий Telethon (Python, Telegram)',
        'text': 'После перезапуска скрипта сессия инвалидируется, 2FA не трогал. session файл и api_id/api_hash проверены.',
        'tags': ['python', 'telegram', 'telethon'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '1k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 14 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Как получить id или тег пользователя в aiogram?',
        'text': 'Нужно в хендлере ответить mention-ом и сохранить user.id в БД. Версия aiogram 3.x.',
        'tags': ['aiogram', 'python'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '1k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 14 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Неверен реляционный оператор в цикле (Oracle / SQL)',
        'text': 'Перенос запроса с MySQL, в PL/SQL цикле сравнение даёт неожиданный результат. NULL и сравнения — подозреваю ловушку.',
        'tags': ['oracle', 'sql', 'mysql', 'plsql'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '87 показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 16 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Console.Clear() в C# очищает консоль не полностью / странно ведёт себя',
        'text': 'Windows Terminal vs классическая консоль — артефакты и «хвост» строк. Есть ли кроссплатформенный паттерн?',
        'tags': ['csharp', 'console', 'dotnet'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '2k показов',
        'author': '0xdb',
        'author_rep': '52.2k',
        'time_ago': 'изменён 16 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Как в Rider настроить перенос длинных строк автоматически?',
        'text': 'Soft wrap для всех файлов по умолчанию, а не только View → Active Editor → Use Soft Wraps.',
        'tags': ['ide', 'jetbrains', 'rider'],
        'votes': 2,
        'answers_count': 1,
        'views_label': '4k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 17 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Как достать данные из JSON-файла в React?',
        'text': 'fetch в useEffect, состояние и обработка ошибок. Нужен минимальный рабочий пример без лишних библиотек.',
        'tags': ['javascript', 'react', 'json', 'html'],
        'votes': 0,
        'answers_count': 0,
        'views_label': '22 показа',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 18 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'SetDlgItemInt: как поменять число в диалоге WinAPI',
        'text': 'Диалог из ресурса RC, нужно обновить счётчик из кода. IDC_STATIC vs отдельный control id.',
        'tags': ['winapi', 'visual-cpp', 'windows-api'],
        'votes': 0,
        'answers_count': 2,
        'views_label': '7k показов',
        'author': 'Максим Гаврилов',
        'author_rep': '43',
        'time_ago': 'изменён 18 часов назад',
        'answers_bold': True,
    },
    {
        'title': 'Как выровнять label и input в одну линию?',
        'text': 'Вёрстка формы: label слева, поле справа, на мобиле в столбик. Flex или grid — что проще поддерживать?',
        'tags': ['html', 'css'],
        'votes': 1,
        'answers_count': 1,
        'views_label': '5k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 19 часов назад',
        'answers_bold': False,
    },
    {
        'title': 'Не запускается служба PostgreSQL 14, не могу подключиться к БД',
        'text': 'Служба падает сразу после старта, логи event viewer и pg_log — с чего начать разбор на Windows?',
        'tags': ['postgresql', 'windows'],
        'votes': 6,
        'answers_count': 3,
        'views_label': '64k показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 19 часов назад',
        'answers_bold': True,
    },
    {
        'title': "Python: 'charmap' codec can't decode byte 0x98",
        'text': 'Чтение файла в Windows-консоли, encoding по умолчанию ломает кириллицу. open(..., encoding=\'utf-8\') и PYTHONUTF8=1.',
        'tags': ['python', 'windows', 'python-3-x', 'console', 'unicode'],
        'votes': 0,
        'answers_count': 2,
        'views_label': '1k показов',
        'author': 'Вадим Александрович',
        'author_rep': '1',
        'time_ago': 'изменён 20 часов назад',
        'answers_bold': True,
    },
    {
        'title': 'Как сделать круглую кнопку с картинкой в Android?',
        'text': 'ImageButton, фон shape oval, ripple и отступы иконки — нужен чистый XML без костылей.',
        'tags': ['java', 'android', 'android-button'],
        'votes': 0,
        'answers_count': 1,
        'views_label': '890 показов',
        'author': 'Дух сообщества',
        'author_rep': 'Бот',
        'time_ago': 'изменён 21 час назад',
        'answers_bold': False,
    },
]


def get_all_questions():
    out = []
    for i, q in enumerate(_RAW_QUESTIONS, start=1):
        ac = q['answers_count']
        v = q['votes']
        item = {
            'id': i,
            'title': q['title'],
            'text': q['text'],
            'tags': list(q['tags']),
            'author': q['author'],
            'author_rep': q.get('author_rep', ''),
            'votes': v,
            'votes_noun': votes_noun(v),
            'answers_count': ac,
            'answers_label': _answers_label(ac),
            'answers_bold': q['answers_bold'],
            'views_label': q['views_label'],
            'time_ago': q['time_ago'],
        }
        out.append(item)
    return out


def get_new_questions():
    return sorted(get_all_questions(), key=lambda x: x['id'], reverse=True)


def get_hot_questions():
    return sorted(get_all_questions(), key=lambda x: (x['votes'], x['id']), reverse=True)


def get_questions_for_tag(tag_slug):
    t = (tag_slug or '').lower()
    return [q for q in get_all_questions() if any(x.lower() == t for x in q['tags'])]


def get_question_by_id(pk):
    for q in get_all_questions():
        if q['id'] == pk:
            return dict(q)
    return None

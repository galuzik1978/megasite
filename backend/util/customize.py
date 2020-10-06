import copy

COMPANY = "Запсиб-Экспертиза"
LOGO = "Penrose-dreieck.svg"
TITLE = "ИКЦ Запсиб-Экспертиза"
Company_INN = "2540167061"
Company_Phone = "79122700658"

inbox = {
    'name': 'inbox',
    'url': 'api/inbox/',
    'title': 'Входящие',
    'ident': ['num', 'sender', 'title', 'date'],
    'headers': [
        {
            'text': 'Номер',
            'align': 'center',
            'sortable': True,
            'value': 'num',
        },
        {
            'text': 'Дата',
            'align': 'center',
            'sortable': True,
            'value': 'date',
        },
        {
            'text': 'Отправитель',
            'align': 'center',
            'sortable': True,
            'value': 'sender.first_name',
        },
        {
            'text': 'Тема',
            'align': 'center',
            'sortable': True,
            'value': 'title',
        },
        {
            'text': 'Содержание',
            'align': 'center',
            'sortable': True,
            'value': 'content',
        },
        {
            'text': 'Приложение',
            'align': 'center',
            'sortable': True,
            'value': 'link',
        },
        {
            'text': 'Статус',
            'align': 'center',
            'sortable': True,
            'value': 'send_status.name',
        },
        {
            'text': 'Тип работы',
            'align': 'center',
            'sortable': True,
            'value': 'type_work.name',
        },
        {
            'text': 'Действия',
            'align': 'center',
            'sortable': False,
            'value': 'actions',
        }
    ],
    'edit': {
        'title': 'Новый входящий',
        'fields': {
            'id': {
                'type': 'hidden',
                'name': 'id'
            },
            "date": {
                'type': 'date',
                'text': 'Дата',
                'width': 6,
                'icon': 'mdi-calendar',
                'name': "date",
                'value': ""
            },
            'sender': {
                'type': 'select',
                'text': 'Отправитель',
                'width': 6,
                'icon': 'fa fa-user',
                'name': "first_name+last_name",
                'value': "",
                'subtable': 'sender',
            },
            "title": {
                'type': 'text',
                'text': 'Тема',
                'width': 12,
                'icon': 'mdi-tag-text-outline',
                'name': "title",
                'value': ""
            },
            "content": {
                'type': 'textarea',
                'text': 'Содержание',
                'width': 12,
                'icon': 'mdi-clipboard-text',
                'name': "content",
                'value': ""
            },
            "annex": {
                'type': 'file',
                'text': 'Приложение',
                'width': 12,
                'name': "annex",
                'value': None
            },
            'send_status': {
                'type': 'select',
                'text': 'Статус',
                'width': 6,
                'icon': 'mdi-flag-checkered',
                'name': "name",
                'value': "",
                'subtable': 'send_status',
            },
            'type_work': {
                'type': 'select',
                'text': 'Тип работы',
                'width': 6,
                'icon': 'mdi-clipboard-check',
                'name': "name",
                'value': "",
                'subtable': 'type_work',
            },
            'type_letter': {
                'type': 'select',
                'text': 'Тип документа',
                'width': 6,
                'icon': 'fa fa-check-square-o',
                'name': "name",
                'value': "",
                'subtable': 'type_letter',
            }
        },
    },
}

new_inbox = copy.deepcopy(inbox)
new_inbox['actions'] = {
    'accept': {
        'text': "Принять в работу",
        'color': 'green',
        'icon': 'mdi-account-multiple-plus',
        'url': 'inbox/accept/',
    },
    'decline': {
        'text': "Отклонить",
        'color': 'red',
        'icon': 'mdi-account-multiple-remove',
        'url': 'inbox/decline/',
    },
    'Cancel': {
        'text': "Закрыть",
        'icon': 'mdi-close-circle-outline',
    },
}
new_inbox['filters'] = [
    {
        'field': 'send_status__name',
        'value': 'Получено'
    }
]
new_inbox['title'] = "Новая заявка"
new_inbox['name'] = 'new_inbox'
new_inbox['headers'].pop()

in_work_inbox = copy.deepcopy(inbox)
in_work_inbox['filters'] = [
    {
        'field': 'send_status__name',
        'value': 'В работе'
    }
]
in_work_inbox['title'] = "Заявки в работе"
in_work_inbox['name'] = 'in_work_inbox'
in_work_inbox['actions'] = {
    'accept': {
        'text': "Оформить договор",
        'color': 'green',
        'icon': 'mdi-grease-pencil',
    },
    'Cancel': {
        'text': "Закрыть",
        'icon': 'mdi-close-circle-outline',
    },
}

# Конфигурация таблиц и доступа к ним, в зависимости от контекста
tables = {
    'inbox': inbox,
    'new_inbox': new_inbox,
    'in_work_inbox': in_work_inbox,
    'outbox': {
        'name': 'outbox',
        'url': 'api/outbox/',
        'title': 'Исходящие',
        'ident': ['num', 'customer', 'title', 'date'],
        'headers': [
            {
                'text': 'Номер',
                'align': 'center',
                'sortable': True,
                'value': 'num',
            },
            {
                'text': 'Дата',
                'align': 'center',
                'sortable': True,
                'value': 'date',
            },
            {
                'text': 'Адресат',
                'align': 'center',
                'sortable': True,
                'value': 'customer.name',
            },
            {
                'text': 'Приложение',
                'align': 'center',
                'sortable': True,
                'value': 'annex',
            },
            {
                'text': 'Примечание',
                'align': 'center',
                'sortable': True,
                'value': 'notice',
            },
            {
                'text': 'Действия',
                'align': 'center',
                'sortable': True,
                'value': 'actions',
            },
        ],
        'edit': {
            'title': 'Отправить письмо',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "date": {
                    'type': 'date',
                    'text': 'Дата',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date",
                    'value': ""
                },
                'customer': {
                    'type': 'select',
                    'text': 'Адресат',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                    'subtable': 'customer',
                },
                "title": {
                    'type': 'text',
                    'text': 'Тема',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "title",
                    'value': ""
                },
                "content": {
                    'type': 'textarea',
                    'text': 'Содержание',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "content",
                    'value': ""
                },
                'type_letter': {
                    'type': 'select',
                    'text': 'Тип письма',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_letter',
                },
            },
        },
    },
    'sender': {
        'name': 'sender',
        'url': 'api/sender/',
        'title': 'Отправитель',
        'ident': ['name'],
        'headers': [
            {
                'text': 'Имя',
                'align': 'center',
                'sortable': True,
                'value': 'first_name',
            },
            {
                'text': 'Отчество',
                'align': 'center',
                'sortable': True,
                'value': 'profile.surname',
            },
            {
                'text': 'Фамилия',
                'align': 'center',
                'sortable': True,
                'value': 'last_name',
            },
            {
                'text': 'Должность',
                'align': 'center',
                'sortable': True,
                'value': 'profile.role.name',
            },
        ],
        'edit': {
            'title': 'Новый отправитель',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "first_name": {
                    'type': 'text',
                    'text': 'Фамилия',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name",
                    'value': ""
                },
                "name": {
                    'type': 'text',
                    'text': 'Имя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
                "profile.surname": {
                    'type': 'text',
                    'text': 'Отчество',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "profile.surname",
                    'value': ""
                },
                'customer': {
                    'type': 'select',
                    'text': 'Организация',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                    'subtable': 'customer',
                },
                "role": {
                    'type': 'select',
                    'text': 'Должность',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'role'
                },
                "profile.phone": {
                    'type': 'text',
                    'text': 'Номер телефона',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "phone",
                    'value': "",
                },
                "email": {
                    'type': 'text',
                    'text': 'электронная почта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "email",
                    'value': "",
                },
            },
        },
    },
    'manager': {
        'name': 'manager',
        'url': 'api/manager/',
        'title': 'Менеджер',
        'ident': ['name'],
        'headers': [
            {
                'text': 'Имя',
                'align': 'center',
                'sortable': True,
                'value': 'first_name',
            },
            {
                'text': 'Отчество',
                'align': 'center',
                'sortable': True,
                'value': 'profile.surname',
            },
            {
                'text': 'Фамилия',
                'align': 'center',
                'sortable': True,
                'value': 'last_name',
            },
            {
                'text': 'Должность',
                'align': 'center',
                'sortable': True,
                'value': 'role.name',
            },
        ],
        'edit': {
            'title': 'Новый менеджер',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "username": {
                    'type': 'text',
                    'text': 'Логин',
                    'width': 6,
                    'icon': 'fa fa-user',
                    'name': "username",
                    'value': ""
                },
                "first_name": {
                    'type': 'text',
                    'text': 'Фамилия',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name",
                    'value': ""
                },
                "name": {
                    'type': 'text',
                    'text': 'Имя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
                "profile.surname": {
                    'type': 'text',
                    'text': 'Отчество',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "surname",
                    'value': ""
                },
            },
        },
    },
    'expert': {
        'name': 'expert',
        'url': 'api/sender/',
        'title': 'Эксперт',
        'ident': ['name'],
        'headers': [
            {
                'text': 'Имя',
                'align': 'center',
                'sortable': True,
                'value': 'first_name',
            },
            {
                'text': 'Отчество',
                'align': 'center',
                'sortable': True,
                'value': 'profile.surname',
            },
            {
                'text': 'Фамилия',
                'align': 'center',
                'sortable': True,
                'value': 'last_name',
            },
            {
                'text': 'Должность',
                'align': 'center',
                'sortable': True,
                'value': 'role.name',
            },
        ],
        'edit': {
            'title': 'Новый эксперт',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "first_name": {
                    'type': 'text',
                    'text': 'Фамилия',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name",
                    'value': ""
                },
                "name": {
                    'type': 'text',
                    'text': 'Имя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
                "profile.surname": {
                    'type': 'text',
                    'text': 'Отчество',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "profile.surname",
                    'value': ""
                },
                'customer': {
                    'type': 'select',
                    'text': 'Организация',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "fullname",
                    'value': "",
                    'subtable': 'customer',
                },
                "profile.phone": {
                    'type': 'text',
                    'text': 'Телефон',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "profile.phone",
                    'value': ""
                },
            },
        },
    },
    'accountant': {
        'name': 'manager',
        'url': 'api/sender/',
        'title': 'Куратор',
        'ident': ['name'],
        'headers': [
            {
                'text': 'Имя',
                'align': 'center',
                'sortable': True,
                'value': 'first_name',
            },
            {
                'text': 'Отчество',
                'align': 'center',
                'sortable': True,
                'value': 'profile.surname',
            },
            {
                'text': 'Фамилия',
                'align': 'center',
                'sortable': True,
                'value': 'last_name',
            },
            {
                'text': 'Должность',
                'align': 'center',
                'sortable': True,
                'value': 'role.name',
            },
        ],
        'edit': {
            'title': 'Новый куратор',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "first_name": {
                    'type': 'text',
                    'text': 'Фамилия',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name",
                    'value': ""
                },
                "name": {
                    'type': 'text',
                    'text': 'Имя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
                "profile.surname": {
                    'type': 'text',
                    'text': 'Отчество',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "profile.surname",
                    'value': ""
                },
                'customer': {
                    'type': 'select',
                    'text': 'Организация',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "fullname",
                    'value': "",
                    'subtable': 'customer',
                },
            },
        },
    },
    'role': {
        'name': 'role',
        'url': 'api/role/', 
        'title': 'Должность',
        'ident': ['name'],
        'headers': [
            {
                'text': 'Должность',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новая должность',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Должность',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                },
            },
        },
    },
    'customer': {
        'name': 'customer',
        'url': 'api/customer/',
        'ident': ['full_name'],
        'title': 'Контрагент',
        'headers': [
            {
                'text': 'ИНН',
                'align': 'center',
                'sortable': True,
                'value': 'inn',
            },
            {
                'text': 'Полное наименование',
                'align': 'center',
                'sortable': True,
                'value': 'inn_filial',
            },
            {
                'text': 'Тип организации',
                'align': 'center',
                'sortable': True,
                'value': 'type_customer',
            },
            {
                'text': 'Руководитель',
                'align': 'center',
                'sortable': True,
                'value': 'head_last_name + head_name + head_surname',
            },
            {
                'text': 'Телефон',
                'align': 'center',
                'sortable': True,
                'value': 'phone',
            },
        ],
        'edit': {
            'title': 'Новый контрагент',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "full_name": {
                    'type': 'text',
                    'text': 'Полное наименование',
                    'width': 12,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                },
                "inn": {
                    'type': 'text',
                    'text': 'ИНН',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "inn",
                    'value': "",
                    'event': "change",
                    'callback': "inn_request"
                },
                "inn-filial": {
                    'type': 'text',
                    'text': 'ИНН филиала',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "inn-filial",
                    'value': ""
                },
                "kpp": {
                    'type': 'text',
                    'text': 'КПП',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "kpp",
                    'value': ""
                },
                "ogrn": {
                    'type': 'text',
                    'text': 'ОГРН',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "ogrn",
                    'value': ""
                },
                "head": {
                    'type': 'text',
                    'text': 'Должность руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head",
                    'value': ""
                },
                "head_name": {
                    'type': 'text',
                    'text': 'Имя руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_name",
                    'value': ""
                },
                "head_surname": {
                    'type': 'text',
                    'text': 'Отчество руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_surname",
                    'value': ""
                },
                "head_last_name": {
                    'type': 'text',
                    'text': 'Фамилия руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_last_name",
                    'value': ""
                },
                "type_customer": {
                    'type': 'select',
                    'text': 'Тип контрагента',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_customer'
                },
                "phone": {
                    'type': 'text',
                    'text': 'Телефон',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "phone",
                    'value': ""
                },
            }
        },
    },
    'organisation': {
        'name': 'organisation',
        'url': 'api/organisation/',
        'ident': ['full_name'],
        'title': 'Организация',
        'headers': [
            {
                'text': 'ИНН',
                'align': 'center',
                'sortable': True,
                'value': 'inn',
            },
            {
                'text': 'ИНН Филиала',
                'align': 'center',
                'sortable': True,
                'value': 'inn_filial',
            },
            {
                'text': 'Полное наименование',
                'align': 'center',
                'sortable': True,
                'value': 'inn_filial',
            },
            {
                'text': 'Тип организации',
                'align': 'center',
                'sortable': True,
                'value': 'type_customer',
            },
            {
                'text': 'Тип организации',
                'align': 'center',
                'sortable': True,
                'value': 'type_customer',
            },
            {
                'text': 'Руководитель',
                'align': 'center',
                'sortable': True,
                'value': 'head_last_name + head_name + head_surname',
            },
            {
                'text': 'Телефон',
                'align': 'center',
                'sortable': True,
                'value': 'phone',
            },
            {
                'text': 'Факс',
                'align': 'center',
                'sortable': True,
                'value': 'fax',
            },
        ],
        'edit': {
            'title': 'Новый контрагент',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "full_name": {
                    'type': 'text',
                    'text': 'Полное наименование',
                    'width': 12,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                },
                "inn": {
                    'type': 'text',
                    'text': 'ИНН',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "inn",
                    'value': "",
                    'event': "change",
                    'callback': "inn_request"
                },
                "inn-filial": {
                    'type': 'text',
                    'text': 'ИНН филиала',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "inn-filial",
                    'value': ""
                },
                "kpp": {
                    'type': 'text',
                    'text': 'КПП',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "kpp",
                    'value': ""
                },
                "ogrn": {
                    'type': 'text',
                    'text': 'ОГРН',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "ogrn",
                    'value': ""
                },
                "head": {
                    'type': 'text',
                    'text': 'Должность руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head",
                    'value': ""
                },
                "head_name": {
                    'type': 'text',
                    'text': 'Имя руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_name",
                    'value': ""
                },
                "head_surname": {
                    'type': 'text',
                    'text': 'Отчество руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_surname",
                    'value': ""
                },
                "head_last_name": {
                    'type': 'text',
                    'text': 'Фамилия руководителя',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "head_last_name",
                    'value': ""
                },
                "type_customer": {
                    'type': 'select',
                    'text': 'Тип контрагента',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_customer'
                },
                "bank": {
                    'type': 'text',
                    'text': 'Банк',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "bank",
                    'value': ""
                },
                "account": {
                    'type': 'text',
                    'text': 'Счет',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "account",
                    'value': ""
                },
                "cor_account": {
                    'type': 'text',
                    'text': 'Корр.Счет',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "cor_account",
                    'value': ""
                },
                "bic": {
                    'type': 'text',
                    'text': 'БИК',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "bic",
                    'value': ""
                },
                "phone": {
                    'type': 'text',
                    'text': 'Телефон',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "phone",
                    'value': ""
                },
                "add_phone": {
                    'type': 'text',
                    'text': 'Дополнительный телефон',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "add_phone",
                    'value': ""
                },
                "fax": {
                    'type': 'text',
                    'text': 'Факс',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "fax",
                    'value': ""
                },
                "filial_count": {
                    'type': 'text',
                    'text': 'Кол-во филиалов',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "filial_count",
                    'value': ""
                },
            }
        },
    },
    'type_letter': {
        'name': 'type_letter',
        'url': '/api/type_letter/',
        'ident': ['name'],
        'title': 'Тип письма',
        'headers': [
            {
                'text': 'Тип письма',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип письма',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип письма',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                },
            },
        },
    },
    'send_status': {
        'name': 'send_status',
        'url': 'api/send_status/',
        'ident': ['name'],
        'title': 'Статус отправки',
        'headers': [
            {
                'text': 'Статус',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый статус',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Статус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'type_work': {
        'name': 'type_work',
        'url': 'api/type_work/',
        'ident': ['name'],
        'title': 'Тип работы',
        'headers': [
            {
                'text': 'Тип работы',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип работы',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип работы',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'contract': {
        'name': 'contract',
        'url': 'api/contract/',
        'ident': ['name'],
        'title': 'Договоры',
        'headers': [
            {
                'text': 'Номер',
                'align': 'center',
                'sortable': True,
                'value': 'num',
            },
            {
                'text': 'Дата заключения',
                'align': 'center',
                'sortable': True,
                'value': 'date',
            },
            {
                'text': 'Дата окончания',
                'align': 'center',
                'sortable': True,
                'value': 'end_date',
            },
            {
                'text': 'Тип работы',
                'align': 'center',
                'sortable': True,
                'value': 'type_work.name',
            }, {
                'text': 'Основание',
                'align': 'center',
                'sortable': True,
                'value': 'inbox',
            }, {
                'text': 'Заказчик',
                'align': 'center',
                'sortable': True,
                'value': 'customer.fullname',
            },
        ],
        'edit': {
            'title': 'Новый контракт',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "date": {
                    'type': 'date',
                    'text': 'Дата заключения',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date",
                    'value': ""
                },
                "end_date": {
                    'type': 'date',
                    'text': 'Дата окончания',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "end_date",
                    'value': ""
                },
                'type_work': {
                    'type': 'select',
                    'text': 'Тип работы',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_work'
                },
                "cost": {
                    'type': 'text',
                    'text': 'Стоимость договора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "cost",
                    'value': ""
                },
                "external_num": {
                    'type': 'text',
                    'text': 'Внешний номер договора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "external_num",
                    'value': ""
                },
                'inbox': {
                    'type': 'date',
                    'text': 'Дата заключения',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date",
                    'value': "",
                    'subtable': 'inbox'
                },
                'customer': {
                    'type': 'select',
                    'text': 'Заказчик',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                    'subtable': 'customer'
                },
            },
        },
    },
    'status': {
        'name': 'status',
        'url': 'api/status/',
        'ident': ['name'],
        'title': 'Статусы',
        'headers': [
            {
                'text': 'Статус',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый статус',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Статус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'task_status': {
        'name': 'task_status',
        'url': 'api/task_status/',
        'ident': ['name'],
        'title': 'Статус задачи',
        'headers': [
            {
                'text': 'Статус',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый статус',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'статус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'event_type': {
        'name': 'event_type',
        'url': 'api/event_type/',
        'ident': ['name'],
        'title': 'Типы событий',
        'headers': [
            {
                'text': 'Тип события',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип события',
            'fields': [
                {
                    'type': 'text',
                    'text': 'Тип события',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            ],
        },
    },
    'main_work': {
        'name': 'main_work',
        'url': 'api/main_work/',
        'ident': ['name'],
        'title': 'Все работы',
        'headers': [
            {
                'text': 'Заявка',
                'align': 'center',
                'sortable': True,
                'value': 'inbox.title',
            },
            {
                'text': 'manager',
                'align': 'center',
                'sortable': True,
                'value': 'manager.first_name + manager.last_name',
            },
            {
                'text': 'expert',
                'align': 'center',
                'sortable': True,
                'value': 'expert.first_name + expert.last_name',
            },
            {
                'text': 'Статус',
                'align': 'center',
                'sortable': True,
                'value': 'status.name',
            },
            {
                'text': 'Стоимость',
                'align': 'center',
                'sortable': True,
                'value': 'cost',
            },
            {
                'text': 'Оплачено',
                'align': 'center',
                'sortable': True,
                'value': 'payed',
            },
            {
                'text': 'contract',
                'align': 'center',
                'sortable': True,
                'value': 'contract.num',
            },
            {
                'text': 'Куратор от заказчика',
                'align': 'center',
                'sortable': True,
                'value': 'accountant.first_name + accountant.last_name',
            }
        ],
        'edit': {
            'title': 'Новая работа',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                'inbox': {
                    'type': 'select',
                    'text': 'Заявка',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "title",
                    'value': "",
                    'subtable': 'inbox'
                },
                'manager': {
                    'type': 'select',
                    'text': 'Менеджер',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + last_name + profile.surname",
                    'value': "",
                    'subtable': 'manager'
                },
                'expert': {
                    'type': 'select',
                    'text': 'Эксперт',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + last_name",
                    'value': "",
                    'subtable': 'expert'
                },
                'status': {
                    'type': 'select',
                    'text': 'Статус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'status'
                },
                "cost": {
                    'type': 'number',
                    'text': 'Стоимость',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "cost",
                    'value': ""
                },
                "payed": {
                    'type': 'number',
                    'text': 'Оплачено',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "payed",
                    'value': ""
                },
                'contract': {
                    'type': 'select',
                    'text': 'Контракт',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "num",
                    'value': "",
                    'subtable': 'contract'
                },
                'accountant': {
                    'type': 'select',
                    'text': 'Куратор проекта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + last_name",
                    'value': "",
                    'subtable': 'accountant'
                },
            },
        },
    },
    'task': {
        'name': 'task',
        'url': 'api/task/',
        'ident': ['name'],
        'title': 'Задачи',
        'headers': [
            {
                'text': 'Наименование',
                'align': 'center',
                'sortable': True,
                'value': 'work_flow.inbox.title',
            },
            {
                'text': 'Инициатор',
                'align': 'center',
                'sortable': True,
                'value': 'initiator.first_name + initiator.last_name',
            },
            {
                'text': 'Исполнитель',
                'align': 'center',
                'sortable': True,
                'value': 'executor.first_name + executor.last_name',
            },
            {
                'text': 'Потребитель',
                'align': 'center',
                'sortable': True,
                'value': 'subscriber.first_name + subscriber.last_name',
            },
            {
                'text': 'Тема задачи',
                'align': 'center',
                'sortable': True,
                'value': 'title',
            },
            {
                'text': 'Содержание задачи',
                'align': 'center',
                'sortable': True,
                'value': 'title',
            },
            {
                'text': 'Статус',
                'align': 'center',
                'sortable': True,
                'value': 'status',
            },
            {
                'text': 'Оценка',
                'align': 'center',
                'sortable': True,
                'value': 'estimate',
            },
        ],
        'edit': {
            'title': 'Новая задача',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "work_flow": {
                    'type': 'text',
                    'text': 'Наименование работы',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "tilte",
                    'value': ""
                },
                'initiator': {
                    'type': 'select',
                    'text': 'Инициатор задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + last_name",
                    'value': "",
                    'subtable': 'sender'
                },
                'executor': {
                    'type': 'select',
                    'text': 'Исполнитель задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + last_name",
                    'value': "",
                    'subtable': 'sender'
                },
                'subscriber': {
                    'type': 'select',
                    'text': 'Потребитель задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name+last_name",
                    'value': "",
                    'subtable': 'sender'
                },
                "title": {
                    'type': 'text',
                    'text': 'Тема задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "title",
                    'value': "",
                },
                "content": {
                    'type': 'textarea',
                    'text': 'Содержимое задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "content",
                    'value': "",
                },
                'status': {
                    'type': 'select',
                    'text': 'Статус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'status'
                },
                "estimate": {
                    'type': 'text',
                    'text': 'Оценка качесва выполнения задачи',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "estimate",
                    'value': "",
                },
            },
        },
    },
    'message': {
        'name': 'message',
        'url': '/api/message/',
        'ident': ['name'],
        'title': 'Сообщения',
        'headers': [
            {
                'text': 'Задача',
                'align': 'center',
                'sortable': True,
                'value': 'task',
            },
            {
                'text': 'Отправитель',
                'align': 'center',
                'sortable': True,
                'value': 'sender',
            },
            {
                'text': 'Получатель',
                'align': 'center',
                'sortable': True,
                'value': 'recipients',
            },
            {
                'text': 'Заголовок',
                'align': 'center',
                'sortable': True,
                'value': 'recipients',
            },
            {
                'text': 'Сообщение',
                'align': 'center',
                'sortable': True,
                'value': 'content',
            },
            {
                'text': 'Приложение',
                'align': 'center',
                'sortable': True,
                'value': 'annex',
            },
        ],
        'edit': {
            'title': 'Новая задача',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                'task': {
                    'type': 'select',
                    'text': 'Задача',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "task",
                    'value': "",
                    'subtable': 'task'
                },
                'sender': {
                    'type': 'select',
                    'text': 'Отправитель',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "sender",
                    'value': "",
                    'subtable': 'sender'
                },
                'recipients': {
                    'type': 'select',
                    'text': 'Получатель',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "sender",
                    'value': "",
                    'subtable': 'recipients'
                },
                "title": {
                    'type': 'text',
                    'text': 'Заголовок',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "title",
                    'value': "",
                },
                "content": {
                    'type': 'textarea',
                    'text': 'Сообщение',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "content",
                    'value': "",
                },
                "annex": {
                    'type': 'file',
                    'text': 'Приложение',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "annex",
                    'value': "",
                },
            },
        },
    },
    'type_customer': {
        'name': 'type_customer',
        'url': '/api/type_customer/',
        'ident': ['name'],
        'title': 'Тип контрагента',
        'headers': [
            {
                'text': 'Тип клиента',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип клиента',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип клиента',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'city_type': {
        'name': 'city_type',
        'url': '/api/city_type/',
        'ident': ['name'],
        'title': 'Тип населенного пункта',
        'headers': [
            {
                'text': 'Тип города',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип города',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип города',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'street_type': {
        'name': 'street_type',
        'url': '/api/street_type/',
        'ident': ['name'],
        'title': 'Тип улицы',
        'headers': [
            {
                'text': 'Тип улцы',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип улицы',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип улицы',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'type_lift': {
        'name': 'type_lift',
        'url': '/api/type_lift/',
        'ident': ['name'],
        'title': 'Тип лифта',
        'headers': [
            {
                'text': 'Тип лифта',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип лифта',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип лифта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'lift_design': {
        'name': 'lift_design',
        'url': '/api/lift_design/',
        'ident': ['name'],
        'title': 'Конструкция лифта',
        'headers': [
            {
                'text': 'Дизайн лифта',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый дизайн лифта',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Дизайн лифта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'type_protocol': {
        'name': 'type_protocol',
        'url': '/api/type_protocol/',
        'ident': ['name'],
        'title': 'Типы протоколов',
        'headers': [
            {
                'text': 'Тип протокола',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип протокола',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип протокола',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'device_set': {
        'name': 'device_set',
        'url': '/api/device_set/',
        'ident': ['name'],
        'title': 'Наборы инструментов',
        'headers': [
            {
                'text': 'Набор приборов',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый набор приборов',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Набор приборов',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'status_device': {
        'name': 'status_device',
        'url': '/api/status_device/',
        'ident': ['name'],
        'title': 'Статусы инструментов',
        'headers': [
            {
                'text': 'Статус прибора',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый статус прибора',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Статус прибора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'type_device': {
        'name': 'type_device',
        'url': '/api/type_device/',
        'ident': ['name'],
        'title': 'Типы инструментов',
        'headers': [
            {
                'text': 'Тип прибора',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый тип прибора',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Тип прибора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'range_measure': {
        'name': 'range_measure',
        'url': '/api/range_measure/',
        'ident': ['name'],
        'title': 'Диапазоны измерений',
        'headers': [
            {
                'text': 'Диапазон измерений',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый диапазон измерений',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Диапазон измерений',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'accuracy': {
        'name': 'accuracy',
        'url': '/api/accuracy/',
        'ident': ['name'],
        'title': 'Классы точности',
        'headers': [
            {
                'text': 'Класс точности',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
        ],
        'edit': {
            'title': 'Новый класс точности',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Класс точности',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
            },
        },
    },
    'object': {
        'name': 'object',
        'url': '/api/object/',
        'ident': ['name'],
        'title': 'Объекты',
        'headers': [
            {
                'text': 'Индекс',
                'align': 'center',
                'sortable': True,
                'value': 'postcode',
            },
            {
                'text': 'Регион',
                'align': 'center',
                'sortable': True,
                'value': 'region',
            },
            {
                'text': 'Адрес',
                'align': 'center',
                'sortable': True,
                'value': 'city_type + city + street_type + street + building + entrance + office',
            },
            {
                'text': 'Скорость лифта',
                'align': 'center',
                'sortable': True,
                'value': 'speed',
            },
            {
                'text': 'Дата поверки',
                'align': 'center',
                'sortable': True,
                'value': 'date_exam',
            },
            {
                'text': 'Заказчик',
                'align': 'center',
                'sortable': True,
                'value': 'customer.fullname',
            },
        ],
        'edit': {
            'title': 'Новая объект',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "postcode": {
                    'type': 'text',
                    'text': 'Индекс',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "postcode",
                    'value': ""
                },
                "region": {
                    'type': 'text',
                    'text': 'Регион',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "region",
                    'value': ""
                },
                'city_type': {
                    'type': 'select',
                    'text': 'Тип населенного пункта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'city_type'
                },
                "city": {
                    'type': 'text',
                    'text': 'Город',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "city",
                    'value': ""
                },
                'street_type': {
                    'type': 'select',
                    'text': 'Тип улицы',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'street_type'
                },
                "street": {
                    'type': 'text',
                    'text': 'Улица',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "street",
                    'value': ""
                },
                "building": {
                    'type': 'text',
                    'text': 'Корпус',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "building",
                    'value': ""
                },
                "entrance": {
                    'type': 'text',
                    'text': 'Номер подъезда',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "entrance",
                    'value': ""
                },
                "office": {
                    'type': 'text',
                    'text': 'Номер офиса',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "office",
                    'value': ""
                },
                "lifts_count": {
                    'type': 'number',
                    'text': 'Кол-во лифтов',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "lifts_count",
                    'value': ""
                },
                "reg_num": {
                    'type': 'text',
                    'text': 'Регистрационный номер',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "reg_num",
                    'value': ""
                },
                "mf_year": {
                    'type': 'date',
                    'text': 'Год выпуска',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "mf_year",
                    'value': ""
                },
                'type_lift': {
                    'type': 'select',
                    'text': 'Дизайн лифта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_lift'
                },
                "capacity": {
                    'type': 'number',
                    'text': 'Грузоподъемность',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "capacity",
                    'value': ""
                },
                "floors": {
                    'type': 'number',
                    'text': 'Кол-во этажей',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "floors",
                    'value': ""
                },
                "speed": {
                    'type': 'number',
                    'text': 'Скорость лифта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "speed",
                    'value': ""
                },
                "maker": {
                    'type': 'text',
                    'text': 'Производитель',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "maker",
                    'value': ""
                },
                "serial_number": {
                    'type': 'text',
                    'text': 'Серийный номер',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "serial_number",
                    'value': ""
                },
                "date_exam": {
                    'type': 'date',
                    'text': 'Дата поверки',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date_exam",
                    'value': ""
                },
                'lift_design': {
                    'type': 'select',
                    'text': 'Дизайн лифта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'lift_design'
                },
                "freq": {
                    'type': 'text',
                    'text': 'Частота',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "freq",
                    'value': ""
                },
                "auto_door": {
                    'type': 'checkbox',
                    'text': 'Автоватические двери',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                },
                "num_lines": {
                    'type': 'text',
                    'text': 'Кол-во линий',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "num_lines",
                    'value': ""
                },
                'customer': {
                    'type': 'select',
                    'text': 'Заказчик',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "fullname",
                    'value': "",
                    'subtable': 'customer'
                },
            },
        },
    },
    'protocol': {
        'name': 'protocol',
        'url': '/api/protocol/',
        'ident': ['name'],
        'title': 'Протоколы',
        'headers': [
            {
                'text': 'Тип протокола',
                'align': 'center',
                'sortable': True,
                'value': 'type_protocol',
            },
            {
                'text': 'Номер протокола',
                'align': 'center',
                'sortable': True,
                'value': 'num',
            },
            {
                'text': 'Дата акта',
                'align': 'center',
                'sortable': True,
                'value': 'date_act',
            },
            {
                'text': 'Дата протокола',
                'align': 'center',
                'sortable': True,
                'value': 'date_protocol',
            },
            {
                'text': 'Обследуемый объект',
                'align': 'center',
                'sortable': True,
                'value': 'object_exam',
            },
            {
                'text': 'Заказчик',
                'align': 'center',
                'sortable': True,
                'value': 'customer.full_name',
            },
            {
                'text': 'Исполнитель',
                'align': 'center',
                'sortable': True,
                'value': 'customer.first_name + customer.last_name',
            },
        ],
        'edit': {
            'title': 'Новый протокол',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                'type_protocol': {
                    'type': 'select',
                    'text': 'Тип протокола',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_protocol'
                },
                "date_act": {
                    'type': 'date',
                    'text': 'Дата подписания акта',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date_act",
                    'value': ""
                },
                "date_protocol": {
                    'type': 'date',
                    'text': 'Дата обследования',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "date_protocol",
                    'value': ""
                },
                'object_exam': {
                    'type': 'select',
                    'text': 'Объект',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'object_exam'
                },
                'customer': {
                    'type': 'select',
                    'text': 'Заказчик',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                    'subtable': 'customer'
                },
                'owner': {
                    'type': 'select',
                    'text': 'Собственник',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "full_name",
                    'value': "",
                    'subtable': 'owner'
                },
                'worker': {
                    'type': 'select',
                    'text': 'Исполнитель',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + larst_name",
                    'value': "",
                    'subtable': 'worker'
                },
                'device_set': {
                    'type': 'select',
                    'text': 'Набор инструментов',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'device_set'
                },
                'customer_person': {
                    'type': 'select',
                    'text': 'Контактное лицо заказчика',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + larst_name",
                    'value': "",
                    'subtable': 'customer_person'
                },
                'owner_person': {
                    'type': 'select',
                    'text': 'Контактное лицо собственника',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "first_name + larst_name",
                    'value': "",
                    'subtable': 'owner_person'
                },
                "electric_template": {
                    'type': 'text',
                    'text': 'шаблон протокола',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "electric_template",
                    'value': ""
                },
                "enabled_measure": {
                    'type': 'text',
                    'text': 'шаблон измерений',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "enabled_measure",
                    'value': ""
                },
                "electric_measure": {
                    'type': 'text',
                    'text': 'шаблон электрических измерений',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "electric_measure",
                    'value': ""
                },
                "num_control_not_use": {
                    'type': 'textarea',
                    'text': 'Не проведенные замеры',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "num_control_not_use",
                    'value': ""
                },
                "unit_protection_valid": {
                    'type': 'checkbox',
                    'text': 'Защита исправна',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "unit_protection_valid",
                    'value': ""
                },
                "safe_exploitation": {
                    'type': 'checkbox',
                    'text': 'Эксплуатация безопасна',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "safe_exploitation",
                    'value': ""
                },
                "visual_inspection": {
                    'type': 'checkbox',
                    'text': 'Внешний осмотр',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "visual_inspection",
                    'value': ""
                },
                "manual": {
                    'type': 'checkbox',
                    'text': 'Ручной режим',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "manual",
                    'value': ""
                },
                "safety_device": {
                    'type': 'checkbox',
                    'text': 'Безопасность устройства',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "safety_device",
                    'value': ""
                },
                "ropes_brake": {
                    'type': 'checkbox',
                    'text': 'Канаты исправны',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "ropes_brake",
                    'value': ""
                },
            },
        },
    },
    'device': {
        'name': 'device',
        'url': '/api/device/',
        'ident': ['name'],
        'title': 'Инструменты',
        'headers': [
            {
                'text': 'Наименование прибора',
                'align': 'center',
                'sortable': True,
                'value': 'name',
            },
            {
                'text': 'Тип прибора',
                'align': 'center',
                'sortable': True,
                'value': 'type_device',
            },
            {
                'text': 'Заводской номер',
                'align': 'center',
                'sortable': True,
                'value': 'type_device',
            },
            {
                'text': 'Дата последней поверки',
                'align': 'center',
                'sortable': True,
                'value': 'verify_date',
            },
            {
                'text': 'Дата следующей поверки',
                'align': 'center',
                'sortable': True,
                'value': 'next_verify',
            },
            {
                'text': 'Набор приборов',
                'align': 'center',
                'sortable': True,
                'value': 'device_set',
            },
            {
                'text': 'Производитель',
                'align': 'center',
                'sortable': True,
                'value': 'maker',
            },
            {
                'text': 'Статус устройства',
                'align': 'center',
                'sortable': True,
                'value': 'status.name',
            },
        ],
        'edit': {
            'title': 'Новый прибор',
            'fields': {
                'id': {
                    'type': 'hidden',
                    'name': 'id'
                },
                "name": {
                    'type': 'text',
                    'text': 'Наименование прибора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': ""
                },
                'type_device': {
                    'type': 'select',
                    'text': 'Тип прибора',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'type_device'
                },
                "serial_number": {
                    'type': 'text',
                    'text': 'Серийный номер',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "serial_number",
                    'value': ""
                },
                "state_reg": {
                    'type': 'text',
                    'text': 'Статус поверки',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "state_reg",
                    'value': ""
                },
                'range_measure': {
                    'type': 'select',
                    'text': 'Диапазон измерений',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'range_measure'
                },
                'accuracy_class': {
                    'type': 'select',
                    'text': 'Класс точности',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'accuracy_class'
                },
                "verify_number": {
                    'type': 'text',
                    'text': 'Номер свидетельства о поверке',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "verify_number",
                    'value': ""
                },
                "verify_date": {
                    'type': 'date',
                    'text': 'Дата последней поверки',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "verify_date",
                    'value': "",
                },
                "next_verify": {
                    'type': 'date',
                    'text': 'Дата следующей поверки',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "next_verify",
                    'value': "",
                },
                "period_verify": {
                    'type': 'text',
                    'text': 'Период поверки',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "period_verify",
                    'value': "",
                },
                "certification_center": {
                    'type': 'text',
                    'text': 'Ответственный',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "certification_center",
                    'value': "",
                },
                'user': {
                    'type': 'select',
                    'text': 'Ответственный',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'user'
                },
                'device_set': {
                    'type': 'select',
                    'text': 'Набор',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'device_set'
                },
                "maker": {
                    'type': 'text',
                    'text': 'Производитель',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "maker",
                    'value': ""
                },
                'status': {
                    'type': 'select',
                    'text': 'Статус устройства',
                    'width': 6,
                    'icon': 'fa fa-hashtag',
                    'name': "name",
                    'value': "",
                    'subtable': 'status'
                },
            },
        },
    },
}

# Конфигурация рабочего стола пользователя в зависимости от роли

# Верхнее меню (типовое)
top_menu = [
    {
        'name': 'ДОМОЙ',
        'url': 'postoffice:main',
    },
    {
        'name': 'КОНТАКТЫ',
        'url': 'postoffice:inbox',
    }
]

desk_config = {
    'manager': {
        'sections': [
            {
                'text': 'Задачи',
                'table': tables['task'],
                'icon': 'far fa-handshake',
                'menu': top_menu,
                'is_active': True,
                'color': 'yellow'
            },
            {
                'text': 'Зарегистрировать',
                'table': tables['inbox'],
                'buttons': '',
                'icon': 'far fa-plus-square',
                'menu': top_menu,
                'is_active': False,
                'color': 'red'
            },
            {
                'text': 'Новые заявки',
                'table': tables['new_inbox'],
                'buttons': '',
                'icon': 'mdi-file-question-outline',
                'menu': top_menu,
                'is_active': False,
                'color': 'red'
            },
            {
                'text': 'Заявки в работе',
                'table': tables['in_work_inbox'],
                'buttons': '',
                'icon': 'mdi-account-hard-hat',
                'menu': top_menu,
                'is_active': False,
                'color': 'red'
            },
            {
                'text': 'Исходящие',
                'icon': 'fas fa-tasks',
                'table': tables['outbox'],
                'menu': top_menu,
                'is_active': False,
                'color': 'blue'
            },
            {
                'text': 'Оформить договор',
                'icon': 'mdi-grease-pencil',
                'table': tables['contract'],
                'menu': top_menu,
                'is_active': False,
                'color': 'blue'
            },
            {
                'text': 'Протоколы',
                'table': tables['protocol'],
                'icon': 'far fa-envelope',
                'menu': top_menu,
                'is_active': False,
                'color': 'red'
            },
        ]
    }
}

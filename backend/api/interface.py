import copy


class Align:
    center = 'center'
    right = 'right'
    left = 'left'


class FieldTypes:
    hidden = 'hidden'
    date = 'date'
    select = 'select'
    text = 'text'
    textarea = 'textarea'
    file = 'file'


class Edit:
    fields = []

    def __init__(self, title):
        self.title = title


class Header:

    def __init__(self, text='', align=Align.center, sortable=True, value=''):
        self.text = text
        self.align = align
        self.sortable = sortable
        self.value = value


class Action:
    def __init__(self, text='', name='', color=None, icon=None, url=None):
        self.text = text
        self.name = name
        self.color = color
        self.icon = icon
        self.url = url


class Filter:
    def __init__(self, field='', value=''):
        self.field = field
        self.value = value


class Field:

    def __init__(self, type='', text='', width=6, icon='', name='', value='', subtable=None):
        self.type = type
        self.text = text
        self.width = width
        self.icon = icon
        self.name = name
        self.value = value
        if type == FieldTypes.select:
            if subtable:
                self.subtable = subtable
            else:
                raise ValueError('Для поля типа select необходимо указать параметр subtable')


class Interface:
    name: str
    headers = []
    edit = None
    actions = []
    filters = []

    def __init__(self, url, name='', title='', icon=''):
        self.url = url
        self.name = name
        self.title = title
        self.icon = icon


number = Header(text='Номер', value='num')
date = Header(text='Дата', value='date')
date_field = Field(type=FieldTypes.date, name='date', text='Дата', icon='mdi-calendar')
id_field = Field(type=FieldTypes.hidden, name='id', width=None)

sender = Interface('api/sender/', name='sender', title='Отправитель')
sender.headers = [
    Header(text='Имя', value='first_name'),
    Header(text='Отчество', value='profile.surname'),
    Header(text='Фамилия', value='last_name'),
    Header(text='Должность', value='profile.role.name')
]
sender.edit = Edit('Новый отправитель')
sender.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Фамилия', icon='fa fa-hashtag', name='last_name'),
    Field(type=FieldTypes.text, text='Имя', icon='fa fa-hashtag', name='first_name'),
    Field(type=FieldTypes.text, text='Отчество', icon='fa fa-hashtag', name='surname'),
    Field(type=FieldTypes.select, text='Организация', icon='fa fa-hashtag', name='full_name', subtable='customer'),
    Field(type=FieldTypes.select, text='Должность', icon='fa fa-hashtag', name='name', subtable='role'),
    Field(type=FieldTypes.text, text='Номер телефона', icon='fa fa-hashtag', name='phone'),
    Field(type=FieldTypes.text, text='Электронная почта', icon='fa fa-hashtag', name='email')
]

send_status = Interface('api/send_status/', name='send_status', title='Статус отправки')
send_status.headers = [
    Header(text='Статус', value='name')
]
send_status.edit = Edit('Новый статус')
send_status.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Статус', name='name')
]

type_work = Interface('api/type_work/', name='type_work', title='Тип работы')
type_work.headers = [
    Header(text='Тип работы', value='name')
]
type_work.edit = Edit('Новый тип работы')
type_work.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Тип работы', name='name', icon='fa fa-hashtag')
]

type_letter = Interface('/api/type_letter/', name='type_letter', title='Тип письма')
type_letter.headers = [
    Header(text='Тип письма', value='name')
]
type_letter.edit = Edit('Новый тип письма')
type_letter.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Тип письма', name='name', icon='fa fa-hashtag')
]

inbox = Interface('api/inbox/', name='inbox', title='Входящие', icon='fas fa-tasks')
inbox.headers = [
    number,
    date,
    Header(text='Отправитель', value='sender.first_name'),
    Header(text='Тема', value='title'),
    Header(text='Содержание', value='content'),
    Header(text='Приложение', value='link'),
    Header(text='Статус', value='send_status.name'),
    Header(text='Тип работы', value='type_work.name'),
    Header(text='Действия', value='actions')
]
inbox.edit = Edit('Новый входящий')
inbox.edit.fields = [
    id_field,
    date_field,
    Field(
        type=FieldTypes.select,
        text='Отправитель',
        icon='fa fa-user',
        name="first_name+last_name",
        subtable=sender.name
    ),
    Field(
        type=FieldTypes.text,
        text='Тема',
        icon='mdi-tag-text-outline',
        name='title',
        width=12
    ),
    Field(
        type=FieldTypes.textarea,
        text='Содержание',
        icon='mdi-clipboard-text',
        name='content',
        width=12
    ),
    Field(
        type=FieldTypes.file,
        text='Приложение',
        name='annex',
        width=12
    ),
    Field(
        type=FieldTypes.select,
        text='Статус',
        icon='mdi-flag-checkered',
        name='name',
        subtable=send_status.name,
    ),
    Field(
        type=FieldTypes.select,
        text='Тип работы',
        icon='mdi-clipboard-check',
        name='name',
        subtable=type_work.name,
    ),
    Field(
        type=FieldTypes.select,
        text='Тип документа',
        icon='fa fa-check-square-o',
        name='name',
        subtable=type_letter.name,
    ),
]

new_inbox = copy.deepcopy(inbox)
new_inbox.actions = [
    Action(text='Принять в работу', name='accept', color='green', icon='mdi-account-multiple-plus', url='inbox/accept/'),
    Action(text='Отклонить', name='decline', color='red', icon='mdi-account-multiple-remove', url='inbox/decline/'),
    Action(text='Закрыть', name='cancel', icon='mdi-close-circle-outline')
]
new_inbox.filters = [
    Filter(field='send_status__name', value='Получено')
]
new_inbox.title = 'Новая заявка'
new_inbox.name = 'new_inbox'
new_inbox.headers.pop()

type_organisation = Interface('api/type_customer/', name='type_organisation', title='Тип организации')
type_organisation.headers = [
    Header(text='Тип организации', value='name')
]
type_organisation.edit = Edit('Новый тип организации')
type_organisation.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Тип организации', name='name', icon='fa fa-hashtag')
]

organisation = Interface('api/organisation/', name='organisation', title='Организация', icon='mdi-account-hard-hat')
organisation.headers = [
    number,
    Header(text='ИНН', value='inn'),
    Header(text='Полное наименование', value='full_name'),
    Header(text='Руководитель', value='head_last_name + head_name + head_surname'),
    Header(text='Телефон', value='phone')
]
organisation.edit = Edit('Новая организация')
organisation.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='ИНН', name='inn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='ИНН филиала', name='inn_filial', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Полное наименование', name='full_name', icon='fa fa-hashtag'),
    Field(
        type=FieldTypes.select,
        text='Тип организации',
        name='type_customer',
        icon='fa fa-hashtag',
        subtable=type_organisation.name
    ),
    Field(type=FieldTypes.text, text='Должность руководителя', name='head', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Имя руководителя', name='head_name', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Отчество руководителя', name='head_surname', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Фамилия руководителя', name='head_last_name', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='КПП', name='kpp', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='ОГРН', name='ogrn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Банк', name='bank', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Расчетный счет', name='account', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Кор. счет', name='cor_account', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='БИК', name='bic', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Телефон', name='phone', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Доп. телефон', name='add_phone', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='факс', name='fax', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Количество филиалов', name='filial_count', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Юридический адрес', name='legal_address', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Почтовый адрес', name='post_address', icon='fa fa-hashtag'),
]

lead = Interface('api/lead/', name='lead', title='Необработанные заявки', icon='far fa-plus-square')
lead.headers = [
    number,
    Header(text='Заказчик', value='customer_full_name'),
    Header(text='Вид работы', value='work.name'),
    Header(text='Контактное лицо', value='customer_contact_name'),
    Header(text='Телефон', value='customer_phone'),
    Header(text='email', value='customer_email'),
    Header(text='Время регистрации', value='sent')
]
lead.edit = Edit('Новая заявка')
lead.edit.fields = [
    id_field,
    Field(type=FieldTypes.text, text='Заказчик', name='customer_full_name', icon='fa fa-hashtag'),
    Field(
        type=FieldTypes.select,
        text='Тип организации',
        name='name',
        icon='fa fa-hashtag',
        subtable=type_organisation.name
    ),
    Field(type=FieldTypes.text, text='Должноть главы организации', name='customer_head', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Имя главы организации', name='customer_name', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Отчество', name='customer_surname', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Фамилия', name='customer_lastname', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='ИНН', name='customer_inn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='КПП', name='customer_kpp', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='ОГРН', name='customer_ogrn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Контактное лицо', name='customer_contact_name', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Эл. почта', name='customer_email', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Телефон', name='customer_phone', icon='fa fa-hashtag'),
    Field(
        type=FieldTypes.text,
        text='Юридический адрес',
        name='customer_legal_address',
        icon='fa fa-hashtag',
        width=12
    ),
    Field(type=FieldTypes.text, text='Почтовый адрес', name='customer_post_address', icon='fa fa-hashtag', width=12),
    Field(
        type=FieldTypes.select,
        text='Организация',
        name='full_name',
        icon='fa fa-hashtag',
        subtable=organisation.name
    ),
    Field(type=FieldTypes.text, text='Банк', name='bank_name', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='БИК', name='bank_bic', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='КПП банка', name='bank_inn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='ИНН банка', name='bank_inn', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Кор.счет', name='bank_correspondent_account', icon='fa fa-hashtag'),
    Field(type=FieldTypes.text, text='Рассчетный счет', name='bank_payment_account', icon='fa fa-hashtag'),
    Field(type=FieldTypes.select, text='Вид работы', name='name', icon='fa fa-hashtag', subtable=type_work.name)
]
lead.actions = [
    Action(text='Отправить заявку', name='send_request', color='green', icon='mdi-account-multiple-plus', url='lead/send_request/'),
    Action(text='Отправить договор', name='send_contract', color='red', icon='mdi-account-multiple-remove', url='lead/send_contract/'),
    Action(text='Обновить', name='updateItem', color='blue', icon='mdi-close-circle-outline'),
    Action(text='Закрыть', name='cancel', icon='mdi-close-circle-outline')
]
tables = {
    'sender': sender,
    'send_status': send_status,
    'type_work': type_work,
    'type_letter': type_letter,
    'inbox': inbox,
    'new_inbox': new_inbox,
    'type_organisation': type_organisation,
    'organisation': organisation,
    'lead': lead
}
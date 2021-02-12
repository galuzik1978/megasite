from decimal import Decimal, InvalidOperation


def capacity_text_to_decimal(cap: str):
    """
    Преобразовываем грузоподъемность лифта из текста в Decimal
    Если строка содержит подстроку кг - грузоподъемность в кг
    Если строка содержит подстроку т - грузоподъемность в т
    Если строка не содержит вышеуказанных подстрок - грузоподъемность в кг
    Разделителем целой и десятичной частей может быть и точка и запятая
    Если строку не удается привести к чилу - возвращается None
    """
    factor = 1000 if cap.find("т") >=0 else 1
    cap = cap.strip().replace(',', '.').split()[0]
    try:
        return Decimal(cap) * factor
    except InvalidOperation as err:
        return None


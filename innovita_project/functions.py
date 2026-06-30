def gaugemeter(data_list):
    """
    Gelen tüm verileri aralarına '|' işareti koyarak birleştirir.
    Main kodu bu işareti görerek verileri kadranda sırayla oynatacaktır.
    """
    if not data_list or len(data_list) == 0:
        return "0"
    
    # Tüm elemanları temizleyip birleştiriyoruz. Örn: ['500', '800', '1050'] -> "500|800|1050"
    return "|".join([v.strip() for v in data_list])


def speedometer(data_list):
    """
    ProfessionalSpeedometer için verileri hazırlar.
    """
    if not data_list or len(data_list) == 0:
        return "0"
    return "|".join([v.strip() for v in data_list])


def altitudebar(data_list):
    """
    VerticalAltitudeBar için verileri hazırlar.
    """
    if not data_list or len(data_list) == 0:
        return "0"
    return "|".join([v.strip() for v in data_list])


def thermometer(data_list):
    """
    VerticalThermometer için verileri hazırlar.
    """
    if not data_list or len(data_list) == 0:
        return "0"
    return "|".join([v.strip() for v in data_list])
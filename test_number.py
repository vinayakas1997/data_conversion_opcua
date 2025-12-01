from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES, get_bit_number,get_register_and_bit


numbers = [488, 306, 488, 404, 296, 404, 486, 304, 486, 576, 239, 224, 576, 488, 306, 488, 576, 239, 224, 576, 576, 239, 224, 576, 576, 239, 224, 576, 404, 296, 404, 576, 239, 224, 576, 485, 303, 485]

for number in numbers:
    reg, bit, reg_type, error_code = get_register_and_bit(number, 'pattern_2')
    print(f" Number {number} Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1


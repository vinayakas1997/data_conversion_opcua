from Tables_config_codes import ERROR_TABLE, ERROR_PATTERN_TYPES, get_bit_number,get_register_and_bit


numbers_AM323 = [488, 306, 488, 404, 296, 404, 486, 304, 486,  488, 306, 488,  404, 296, 404,  485, 303, 485]
numbers_AM322 =[576, 239, 224, 576,576, 239, 224, 576, 576, 239, 224, 576, 576, 239, 224, 576,576, 239, 224, 576,]

print("\n\nThe time between the 14:15:27  to the 14:39:49 \n\n")

for number in set(numbers_AM323):
    reg, bit, reg_type, error_code = get_register_and_bit(number, 'pattern_2')
    print(f" AM323 -  Number {number} ==> Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

print ("\n=============###############==================\n")
for number in set(numbers_AM322):
    reg, bit, reg_type, error_code = get_register_and_bit(number, 'pattern_1')
    print(f" AM322 -  Number {number} ==> Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

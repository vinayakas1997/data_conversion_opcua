# plc_error_pattern_config.py

# ============================================================================
# Error Pattern Configuration (Nested: Pattern -> Type -> Config)
# ============================================================================

ERROR_PATTERN_TYPES = {
        'pattern_1': {
        '起動時異常': {
            'code':'1',
            'register_start': 550,
            'register_end': 564,
            'bit_number_start': 0,
            'bits_per_register': 16,
            'description': 'Pattern 1 Type 1 registers with bit mapping 0-319'
        },
        '運転中異常': {
            'code':'2',
            'register_start': 565,
            'register_end': 589,
            'bit_number_start': 320,
            'bits_per_register': 16,
            'description': 'Pattern 1 Type 2 registers with bit mapping 320-639'
        }
    },
    'pattern_2': {
        '起動時異常': {
            'code':'1',
            'register_start': 550,
            'register_end': 569,
            'bit_number_start': 0,
            'bits_per_register': 16,
            'description': 'Pattern 1 Type 1 registers with bit mapping 0-319'
        },
        '運転中異常': {
            'code':'2',
            'register_start': 570,
            'register_end': 589,
            'bit_number_start': 320,
            'bits_per_register': 16,
            'description': 'Pattern 1 Type 2 registers with bit mapping 320-639'
        }
    },
}


# ============================================================================
# Helper Functions (Updated to include pattern parameter)
# ============================================================================

def get_bit_number(register: int, bit_position: int, pattern: str = 'pattern_1', register_type: str = None) -> tuple[int, str]:
    """
    Calculate the absolute bit number from register and bit position.
    
    Args:
        register: Register number (e.g., 550, 570)
        bit_position: Bit position within register (0-15)
        pattern: Error pattern name (e.g., 'pattern_1', 'pattern_2')
        register_type: Optional, 'type1' or 'type2' (auto-detected if None)
    
    Returns:
        Tuple of (bit_number, register_type, error_code)
    
    Example:
        >>> get_bit_number(550, 0, 'pattern_1')
        (0, 'type1')
        >>> get_bit_number(550, 15, 'pattern_1')
        (15, 'type1')
        >>> get_bit_number(569, 15, 'pattern_1')
        (319, 'type1')
        >>> get_bit_number(570, 0, 'pattern_1')
        (320, 'type2')
    """
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found in ERROR_PATTERN_TYPES")
    
    if not 0 <= bit_position < 16:
        raise ValueError("Bit position must be between 0 and 15")
    
    pattern_config = ERROR_PATTERN_TYPES[pattern]
    
    # error_code 
    error_code = None
    # Auto-detect type if not provided
    if register_type is None:
        for rtype, config in pattern_config.items():
            if config['register_start'] <= register <= config['register_end']:
                register_type = rtype
                error_code = config['code']
                break
        else:
            raise ValueError(f"Register {register} not found in pattern '{pattern}'")
    
    if register_type not in pattern_config:
        raise ValueError(f"Register type '{register_type}' not found in pattern '{pattern}'")
    
    config = pattern_config[register_type]
    
    # Validate register is in range
    if not config['register_start'] <= register <= config['register_end']:
        raise ValueError(f"Register {register} not in range for {pattern}/{register_type}")
    
    # Calculate: offset from start * bits per register + bit position + base offset
    register_offset = register - config['register_start']
    bit_number = (register_offset * config['bits_per_register']) + bit_position + config['bit_number_start']
    
    return (bit_number, register_type, error_code)


def get_register_and_bit(bit_number: int, pattern: str = 'pattern_1') -> tuple[int, int, str]:
    """
    Reverse calculation: Get register, bit position, and type from bit number.
    
    Args:
        bit_number: Absolute bit number (0-639)
        pattern: Error pattern name
    
    Returns:
        Tuple of (register, bit_position, register_type, error_code)
    
    Example:
        >>> get_register_and_bit(0, 'pattern_1')
        (550, 0, 'type1')
        >>> get_register_and_bit(319, 'pattern_1')
        (569, 15, 'type1')
        >>> get_register_and_bit(320, 'pattern_1')
        (570, 0, 'type2')
    """
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found")
    
    pattern_config = ERROR_PATTERN_TYPES[pattern]
    error_code = None
    for reg_type, config in pattern_config.items():
        error_code = config['code']
        start_bit = config['bit_number_start']
        total_registers = config['register_end'] - config['register_start'] + 1
        end_bit = start_bit + (total_registers * config['bits_per_register']) - 1
        
        if start_bit <= bit_number <= end_bit:
            offset_from_start = bit_number - start_bit
            register_offset = offset_from_start // config['bits_per_register']
            bit_position = offset_from_start % config['bits_per_register']
            register = config['register_start'] + register_offset
            
            return (register, bit_position, reg_type,error_code)
    
    raise ValueError(f"Bit number {bit_number} not in valid range for pattern '{pattern}'")


def get_register_range(pattern: str, register_type: str) -> list[int]:
    """Get all register numbers for a pattern and type."""
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found")
    
    config = ERROR_PATTERN_TYPES[pattern][register_type]
    return list(range(config['register_start'], config['register_end'] + 1))


def get_bit_range(pattern: str, register_type: str) -> tuple[int, int]:
    """Get the bit number range for a pattern and register type."""
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found")
    
    config = ERROR_PATTERN_TYPES[pattern][register_type]
    start_bit = config['bit_number_start']
    total_registers = config['register_end'] - config['register_start'] + 1
    end_bit = start_bit + (total_registers * config['bits_per_register']) - 1
    return (start_bit, end_bit)


def generate_full_mapping(pattern: str, register_type: str) -> dict[str, int]:
    """
    Generate complete mapping for a pattern and register type.
    Returns dict with keys like "550.0", "550.1", etc.
    
    WARNING: Only use this if you need the full mapping for display/export.
    For normal operations, use get_bit_number() instead.
    """
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found")
    
    config = ERROR_PATTERN_TYPES[pattern][register_type]
    mapping = {}
    
    for register in range(config['register_start'], config['register_end'] + 1):
        for bit in range(16):
            key = f"{register}.{bit}"
            bit_number = get_bit_number(register, bit, pattern, register_type)
            mapping[key] = bit_number
    
    return mapping


def get_all_patterns() -> list[str]:
    """Get list of all available error patterns."""
    return list(ERROR_PATTERN_TYPES.keys())


def get_pattern_types(pattern: str) -> list[str]:
    """Get all register types for a given pattern."""
    if pattern not in ERROR_PATTERN_TYPES:
        raise ValueError(f"Pattern '{pattern}' not found")
    return list(ERROR_PATTERN_TYPES[pattern].keys())


def validate_register_access(register: int, bit_position: int, pattern: str = 'pattern_1') -> bool:
    """Check if a register.bit combination is valid for a pattern."""
    try:
        get_bit_number(register, bit_position, pattern)
        return True
    except ValueError:
        return False


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    # Example 1: Get bit number for pattern_1
    # bit_num, reg_type, error_code = get_bit_number(550, 0, 'pattern_1')
    # print(f"Pattern 1: Register 550, bit 0 -> Bit number: {bit_num}, Type: {reg_type},Error Code: {error_code}")  # 0, type1
    
    # bit_num, reg_type, error_code = get_bit_number(569, 15, 'pattern_1')
    # print(f"Pattern 1: Register 569, bit 15 -> Bit number: {bit_num}, Type: {reg_type},Error Code: {error_code}")  # 319, type1
    
    # bit_num, reg_type, error_code = get_bit_number(570, 0, 'pattern_1')
    # print(f"Pattern 1: Register 570, bit 0 -> Bit number: {bit_num}, Type: {reg_type}, Error Code: {error_code}")  # 320, type2
    
    # # Example 2: Reverse lookup
    # reg, bit, reg_type, error_code = get_register_and_bit(319, 'pattern_1')
    # print(f"Pattern 1: Bit 319 -> Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1
    
    # # Example 3: Get ranges
    # type1_bits = get_bit_range('pattern_1', '起動時異常')
    # print(f"Pattern 1, Type1 bit range: {type1_bits}")  # (0, 319)
    
    # type2_bits = get_bit_range('pattern_1', '運転中異常')
    # print(f"Pattern 1, Type2 bit range: {type2_bits}")  # (320, 639)
    
    # # Example 4: Get all patterns
    # patterns = get_all_patterns()
    # print(f"Available patterns: {patterns}")
    
    # # Example 5: Get types for a pattern
    # types = get_pattern_types('pattern_1')
    # print(f"Pattern 1 types: {types}")
    
    # Example 6: Only generate full mapping if needed for export/display
    # full_map = generate_full_mapping('pattern_1', 'type1')
    # print(f"Total mappings: {len(full_map)}")  # 320

    # # Example 2: Reverse lookup
    reg, bit, reg_type, error_code = get_register_and_bit(306, 'pattern_2')
    print(f" Number 306 Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

    reg, bit, reg_type, error_code = get_register_and_bit(296, 'pattern_2')
    print(f" Number 296 Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

    reg, bit, reg_type, error_code = get_register_and_bit(404, 'pattern_2')
    print(f" Number 404 Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

    reg, bit, reg_type, error_code = get_register_and_bit(239, 'pattern_2')
    print(f" Number 239 Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

    reg, bit, reg_type, error_code = get_register_and_bit(656, 'pattern_1')
    print(f" Number 656 Register: {reg}, Bit: {bit}, Type: {reg_type} error_code: {error_code}")  # 569, 15, type1

    bit_num, reg_type, error_code = get_bit_number(569, 2, 'pattern_2')
    print(f"Pattern 2:  Bit number: {bit_num}, Type: {reg_type},Error Code: {error_code}")  # 0, type1
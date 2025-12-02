import struct

class PLCDataConverter:
    """
    A data converter for PLC/FINS protocol hex data.
    Uses clear, explicit naming convention for all data types.
    
    Input: Array of hex strings like ["1234", "5678", "ABCD"]
    Supports: INT16, UINT16, INT32, UINT32, INT64, UINT64, REAL16, REAL32, REAL64, BOOL
    
    Naming Convention:
    - INT16/UINT16: 16-bit integer (1 word)
    - INT32/UINT32: 32-bit integer (2 words)
    - INT64/UINT64: 64-bit integer (4 words)
    - REAL16: 16-bit scaled float (1 word, requires scale_factor)
    - REAL32: 32-bit IEEE 754 float (2 words)
    - REAL64: 64-bit IEEE 754 double (4 words)
    - BOOL: Single bit extraction
    """
    
    def __init__(self):
        """Initialize the converter"""
        pass
    
    def _apply_swaps(self, data_array, word_swap=False, byte_swap=False):
        """
        Apply word and/or byte swapping to the data array.
        
        Args:
            data_array: List of hex strings
            word_swap: If True, reverse the order of words in array
            byte_swap: If True, reverse byte pairs within each word
            
        Returns:
            Modified list of hex strings
        """
        result = data_array.copy()
        
        # Apply byte swap (reverse characters in pairs within each word)
        if byte_swap:
            swapped = []
            for word in result:
                # "1234" -> "3412" (swap byte pairs)
                if len(word) == 4:
                    swapped.append(word[2:4] + word[0:2])
                else:
                    swapped.append(word)
            result = swapped
        
        # Apply word swap (reverse array order)
        if word_swap:
            result = result[::-1]
        
        return result
    
    def extract_bit(self, hex_string, bit_position):
        """
        Extract a specific bit from a 16-bit hex word.
        
        Args:
            hex_string: 16-bit hex string like "F567"
            bit_position: Bit position (0-15, where 0 is LSB)
            
        Returns:
            bool: True if bit is set, False otherwise
        """
        if not (0 <= bit_position <= 15):
            raise ValueError("Bit position must be between 0 and 15")
        
        value = int(hex_string, 16)
        return bool((value >> bit_position) & 1)
    
    def to_int16(self, hex_string):
        """
        Convert 16-bit hex string to signed 16-bit integer.
        
        Args:
            hex_string: 16-bit hex string like "F567"
            
        Returns:
            int: Signed 16-bit integer (-32768 to 32767)
        """
        value = int(hex_string, 16)
        # Convert to signed
        if value >= 0x8000:
            value -= 0x10000
        return value
    
    def to_uint16(self, hex_string):
        """
        Convert 16-bit hex string to unsigned 16-bit integer.
        
        Args:
            hex_string: 16-bit hex string like "F567"
            
        Returns:
            int: Unsigned 16-bit integer (0 to 65535)
        """
        return int(hex_string, 16)
    
    def to_real16(self, hex_array, scale_factor=10):
        """
        Convert 16-bit hex string to scaled float using fixed-point representation.
        This is for PLCs that store decimal values as scaled integers in a single word.
        
        Args:
            hex_array: List with 1 hex string like ["0042"]
            scale_factor: Divisor to convert to decimal (default: 10)
                         - scale=10: 1 decimal place (6.6)
                         - scale=100: 2 decimal places (6.60)
                         - scale=1000: 3 decimal places (6.600)
            
        Returns:
            float: Scaled decimal value
            
        Examples:
            >>> converter.to_real16(["0042"], scale_factor=10)
            6.6
            >>> converter.to_real16(["002E"], scale_factor=10)
            4.6
            >>> converter.to_real16(["0294"], scale_factor=100)
            6.6
        """
        if len(hex_array) < 1:
            raise ValueError("REAL16 requires 1 hex word")
        
        int_value = int(hex_array[0], 16)
        return int_value / scale_factor
    
    def to_int32(self, hex_array):
        """
        Convert two 16-bit hex strings to signed 32-bit integer.
        
        Args:
            hex_array: List of 2 hex strings like ["1234", "5678"]
            
        Returns:
            int: Signed 32-bit integer (-2147483648 to 2147483647)
        """
        if len(hex_array) < 2:
            raise ValueError("INT32 requires 2 hex words")
        
        # Combine two 16-bit words into 32-bit
        high = int(hex_array[0], 16)
        low = int(hex_array[1], 16)
        value = (high << 16) | low
        
        # Convert to signed
        if value >= 0x80000000:
            value -= 0x100000000
        return value
    
    def to_uint32(self, hex_array):
        """
        Convert two 16-bit hex strings to unsigned 32-bit integer.
        
        Args:
            hex_array: List of 2 hex strings like ["1234", "5678"]
            
        Returns:
            int: Unsigned 32-bit integer (0 to 4294967295)
        """
        if len(hex_array) < 2:
            raise ValueError("UINT32 requires 2 hex words")
        
        high = int(hex_array[0], 16)
        low = int(hex_array[1], 16)
        return (high << 16) | low
    
    def to_real32(self, hex_array):
        """
        Convert two 16-bit hex strings to 32-bit IEEE 754 float.
        
        Args:
            hex_array: List of 2 hex strings like ["40D3", "3333"]
            
        Returns:
            float: 32-bit IEEE 754 floating point number
        """
        if len(hex_array) < 2:
            raise ValueError("REAL32 requires 2 hex words")
        
        # Combine into 32-bit integer
        high = int(hex_array[0], 16)
        low = int(hex_array[1], 16)
        int_value = (high << 16) | low
        
        # Convert to float using struct
        bytes_value = int_value.to_bytes(4, byteorder='big')
        return struct.unpack('>f', bytes_value)[0]
    
    def to_int64(self, hex_array):
        """
        Convert four 16-bit hex strings to signed 64-bit integer.
        
        Args:
            hex_array: List of 4 hex strings
            
        Returns:
            int: Signed 64-bit integer
        """
        if len(hex_array) < 4:
            raise ValueError("INT64 requires 4 hex words")
        
        value = 0
        for i, hex_str in enumerate(hex_array[:4]):
            word = int(hex_str, 16)
            value |= (word << (48 - i * 16))
        
        # Convert to signed
        if value >= 0x8000000000000000:
            value -= 0x10000000000000000
        return value
    
    def to_uint64(self, hex_array):
        """
        Convert four 16-bit hex strings to unsigned 64-bit integer.
        
        Args:
            hex_array: List of 4 hex strings
            
        Returns:
            int: Unsigned 64-bit integer
        """
        if len(hex_array) < 4:
            raise ValueError("UINT64 requires 4 hex words")
        
        value = 0
        for i, hex_str in enumerate(hex_array[:4]):
            word = int(hex_str, 16)
            value |= (word << (48 - i * 16))
        return value
    
    def to_real64(self, hex_array):
        """
        Convert four 16-bit hex strings to 64-bit IEEE 754 double.
        
        Args:
            hex_array: List of 4 hex strings
            
        Returns:
            float: 64-bit IEEE 754 double precision floating point number
        """
        if len(hex_array) < 4:
            raise ValueError("REAL64 requires 4 hex words")
        
        # Combine into 64-bit integer
        value = 0
        for i, hex_str in enumerate(hex_array[:4]):
            word = int(hex_str, 16)
            value |= (word << (48 - i * 16))
        
        # Convert to double using struct
        bytes_value = value.to_bytes(8, byteorder='big')
        return struct.unpack('>d', bytes_value)[0]
    
    def convert(self, data_array, data_type, start_index=0, word_swap=False, byte_swap=False, bit_position=None, scale_factor=10):
        """
        Master conversion function. Automatically handles multi-word types.
        
        Args:
            data_array: List of hex strings like ["1234", "5678", "ABCD"]
            data_type: Type string - "INT16", "UINT16", "INT32", "UINT32", "INT64", "UINT64",
                      "REAL16", "REAL32", "REAL64", "BOOL"
            start_index: Starting position in the array (default: 0)
            word_swap: Reverse the order of words (default: False)
            byte_swap: Swap byte pairs within each word (default: False)
            bit_position: Required for BOOL type (0-15)
            scale_factor: Required for REAL16 type (default: 10)
            
        Returns:
            Converted value (int, float, or bool depending on type)
            
        Examples:
            >>> converter = PLCDataConverter()
            >>> converter.convert(["1234"], "INT16")
            4660
            >>> converter.convert(["1234", "5678"], "INT32")
            305419896
            >>> converter.convert(["1234", "5678"], "INT32", word_swap=True)
            1450744404
            >>> converter.convert(["F567"], "BOOL", bit_position=0)
            True
            >>> converter.convert(["0042"], "REAL16", scale_factor=10)
            6.6
        """
        # Normalize type to uppercase
        data_type = data_type.upper()
        
        # Define word requirements for each type
        type_map = {
            'INT16': (1, self.to_int16),
            'UINT16': (1, self.to_uint16),
            'INT32': (2, self.to_int32),
            'UINT32': (2, self.to_uint32),
            'REAL32': (2, self.to_real32),
            'INT64': (4, self.to_int64),
            'UINT64': (4, self.to_uint64),
            'REAL64': (4, self.to_real64),
        }
        
        # Special handling for BOOL
        if data_type == 'BOOL':
            if bit_position is None:
                raise ValueError("BOOL type requires bit_position parameter")
            if start_index >= len(data_array):
                raise ValueError(f"start_index {start_index} out of range")
            
            # Apply swaps to the word containing the bit
            swapped = self._apply_swaps([data_array[start_index]], word_swap, byte_swap)
            return self.extract_bit(swapped[0], bit_position)
        
        # Special handling for REAL16
        if data_type == 'REAL16':
            if start_index >= len(data_array):
                raise ValueError(f"start_index {start_index} out of range")
            
            # Apply swaps to the single word
            words = self._apply_swaps([data_array[start_index]], word_swap, byte_swap)
            return self.to_real16(words, scale_factor)
        
        # Validate type
        if data_type not in type_map:
            raise ValueError(f"Unsupported data type: {data_type}. Supported types: {', '.join(type_map.keys())}, REAL16, BOOL")
        
        # Get word count and conversion function
        word_count, convert_func = type_map[data_type]
        
        # Validate array length
        if start_index + word_count > len(data_array):
            raise ValueError(f"{data_type} requires {word_count} word(s), but only {len(data_array) - start_index} available from index {start_index}")
        
        # Extract required words
        words = data_array[start_index:start_index + word_count]
        
        # Apply swaps
        words = self._apply_swaps(words, word_swap, byte_swap)
        
        # Convert based on word count
        if word_count == 1:
            return convert_func(words[0])
        else:
            return convert_func(words)


# Example usage and testing
if __name__ == "__main__":
    converter = PLCDataConverter()
    
    # print("=== PLC Data Converter - Clear Naming Convention ===\n")
    
    # print("--- 16-bit Integers (1 word) ---")
    # print(f"INT16  ['1234']: {converter.convert(['1234'], 'INT16')}")
    # print(f"UINT16 ['FFFF']: {converter.convert(['FFFF'], 'UINT16')}")
    
    # print("\n--- 32-bit Integers (2 words) ---")
    # print(f"INT32  ['1234', '5678']: {converter.convert(['1234', '5678'], 'INT32')}")
    # print(f"UINT32 ['FFFF', 'FFFF']: {converter.convert(['FFFF', 'FFFF'], 'UINT32')}")
    
    # print("\n--- 64-bit Integers (4 words) ---")
    # print(f"INT64  ['0000', '0000', '0000', '0001']: {converter.convert(['0000', '0000', '0000', '0001'], 'INT64')}")
    # print(f"UINT64 ['0000', '0000', '0000', '00FF']: {converter.convert(['0000', '0000', '0000', '00FF'], 'UINT64')}")
    
    # print("\n--- Floating Point Numbers ---")
    # print(f"REAL16 ['0042'] (scale=10):  {converter.convert(['0042'], 'REAL16', scale_factor=10)}")  # 6.6
    # print(f"REAL16 ['002E'] (scale=10):  {converter.convert(['002E'], 'REAL16', scale_factor=10)}")  # 4.6
    # print(f"REAL16 ['0294'] (scale=100): {converter.convert(['0294'], 'REAL16', scale_factor=100)}")  # 6.6
    # print(f"REAL32 ['40D3', '3333']:     {converter.convert(['40D3', '3333'], 'REAL32')}")  # ~6.6
    
    # print("\n--- Boolean Bit Extraction ---")
    # print(f"BOOL ['F567'] bit 0: {converter.convert(['F567'], 'BOOL', bit_position=0)}")
    # print(f"BOOL ['F567'] bit 1: {converter.convert(['F567'], 'BOOL', bit_position=1)}")
    
    # print("\n--- With Byte Swap ---")
    # print(f"INT16 ['1234'] byte_swap=True: {converter.convert(['1234'], 'INT16', byte_swap=True)}")
    
    # print("\n--- With Word Swap ---")
    # print(f"INT32 ['1234', '5678'] word_swap=True: {converter.convert(['1234', '5678'], 'INT32', word_swap=True)}")

    print(f"REAL16 ['0254'] (scale=100): {converter.convert(['0254'], 'REAL16', scale_factor=100)}")
    print(f"REAL16 ['024F'] (scale=100): {converter.convert(['024F'], 'REAL16', scale_factor=100)}")

    print(f"REAL16 ['024D'] (scale=100): {converter.convert(['024D'], 'REAL16', scale_factor=100)}")
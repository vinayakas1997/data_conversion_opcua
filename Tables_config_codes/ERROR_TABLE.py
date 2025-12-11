"""
DATE_CREATED: 2025-12-01
AUTHOR: Vinayaka S
MANAGER: YAMADA, AKITA
DESCRIPTION:

Error Table Configuration

This table stores error information from the PLC and sequencer. It includes details about the error mode, error code, and error pattern.

The table has a dynamic number of columns based on whether the PLC is used or not. If the PLC is used, there are 50 columns, otherwise there are 10 columns.

The naming convention for the columns is as follows:
- For bit addresses: (meme_area)_(machine_no)_(reg_address_no).Bit[bit_position]
- For word addresses: (meme_area)_(machine_no)_(reg_address_no) or (meme_area)_(machine_no)_[index_no]

The work mode can be one of the following:
- 502.12-自動 (Automatic)
- 502.13-手動 (Manual)
- 502.14払出 (Payment)

The error mode can be one of the following:
- 1:起動時異常 (Startup Error)
- 2:運転中異常 (Operation Error)

The error code is calculated using a special calculation.

The error pattern is pattern_1.
"""

ERROR_TABLE = {
    "table_name": "ERROR_TABLE",
    "iot_info": {
        "no_of_columns": 60,
        "naming_convention": {1:"PLC<->sequencer"},
        "no_of_columns_depends_on_PLC":{"YES":50, "NO":10},
        "iot_naming_columns": {"bit_addr":"(meme_area)_(machine_no)_(reg_address_no).Bit[bit_position]",
                               "word_addr":"(meme_area)_(machine_no)_(reg_address_no) or (meme_area)_(machine_no)_[index_no]"},
        "V_work_mode":"[502.12-自動,502.13-手動,502.14払出]",
        "Error_Mode":"[1:起動時異常 2:運転中異常]",
        "Error_Code": "special_calculation",
        "error_patterns":"pattern_1"
    },
    "columns": {
        "日付": {
            "English_Name": "INSERT_DATE",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "勤務日付軸": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "昼夜勤": {
            "English_Name": "AB_SECTION_DAY",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "ユニットコード": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "工程順番": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "機番": {
            "English_Name": "Machine_No",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "時間帯": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "作業者": {
            "English_Name": "",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "[DM31600,DM31601]",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "運転モード": {
            "English_Name": "V_work_mode",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "[502.12,502.13,502.14]",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": "[502.12-自動,502.13-手動,502.14払出]"
        },
        "異常種類": {
            "English_Name": "Error_Mode",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": "[1:起動時異常 2:運転中異常] special - calculation module needed to find thetype"
        },
        "異常№": {
            "English_Name": "ErrorCode",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": "special - calculation module needed to find the and the number"
        },
        "異常内容": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "ON/OFF": {
            "English_Name": "",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "comment": ""
        },
        "起動時異常停止時間(s)": {
            "English_Name": "WarningTime",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "LINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "運転中異常停止時間(s)": {
            "English_Name": "AlarmTime",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "LINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST1": {
            "English_Name": "Work_No_ST1",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31651",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST2": {
            "English_Name": "Work_No_ST2",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31652",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST3": {
            "English_Name": "Work_No_ST3",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31653",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST4": {
            "English_Name": "Work_No_ST4",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31654",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST5": {
            "English_Name": "Work_No_ST5",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31655",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST6": {
            "English_Name": "Work_No_ST6",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31656",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST7": {
            "English_Name": "Work_No_ST7",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31657",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST8": {
            "English_Name": "Work_No_ST8",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31658",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST9": {
            "English_Name": "Work_No_ST9",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31659",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST10": {
            "English_Name": "Work_No_ST10",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31660",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST11": {
            "English_Name": "Work_No_ST11",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31661",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST12": {
            "English_Name": "Work_No_ST12",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31662",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST13": {
            "English_Name": "Work_No_ST13",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31663",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST14": {
            "English_Name": "Work_No_ST14",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31664",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ﾜｰｸ№ST15": {
            "English_Name": "Work_No_ST15",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31665",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST1": {
            "English_Name": "SERIAL_No_ST1",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31701",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST2": {
            "English_Name": "SERIAL_No_ST2",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31702",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST3": {
            "English_Name": "SERIAL_No_ST3",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31703",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST4": {
            "English_Name": "SERIAL_No_ST4",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31704",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST5": {
            "English_Name": "SERIAL_No_ST5",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31705",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST6": {
            "English_Name": "SERIAL_No_ST6",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31706",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST7": {
            "English_Name": "SERIAL_No_ST7",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31707",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST8": {
            "English_Name": "SERIAL_No_ST8",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31708",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST9": {
            "English_Name": "SERIAL_No_ST9",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31709",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST10": {
            "English_Name": "SERIAL_No_ST10",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31710",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST11": {
            "English_Name": "SERIAL_No_ST11",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31711",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST12": {
            "English_Name": "SERIAL_No_ST12",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31712",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST13": {
            "English_Name": "SERIAL_No_ST13",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31713",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST14": {
            "English_Name": "SERIAL_No_ST14",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31714",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｼﾘｱﾙ№ST15": {
            "English_Name": "SERIAL_No_ST15",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31715",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "STRING[21]",
            "Sql_Data_Type": "varchar(20)",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST1": {
            "English_Name": "Index_No_ST1",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST2": {
            "English_Name": "Index_No_ST2",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST3": {
            "English_Name": "Index_No_ST3",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST4": {
            "English_Name": "Index_No_ST4",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST5": {
            "English_Name": "Index_No_ST5",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST6": {
            "English_Name": "Index_No_ST6",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST7": {
            "English_Name": "Index_No_ST7",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST8": {
            "English_Name": "Index_No_ST8",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST9": {
            "English_Name": "Index_No_ST9",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST10": {
            "English_Name": "Index_No_ST10",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST11": {
            "English_Name": "Index_No_ST11",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST12": {
            "English_Name": "Index_No_ST12",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST13": {
            "English_Name": "Index_No_ST13",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST14": {
            "English_Name": "Index_No_ST14",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        },
        "ｲﾝﾃﾞｯｸｽ№ST15": {
            "English_Name": "Index_No_ST15",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "comment": ""
        }
    }

}

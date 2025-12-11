"""
DATE_CREATED: 2025-12-01
AUTHOR: Vinayaka S
MANAGER: YAMADA, AKITA
DESCRIPTION:

Error Table Configuration

This table stores error information from the PLC and sequencer. It includes details about the production info and work station pattern.

The table has a dynamic number of columns based on whether the PLC is used or not. If the PLC is used, there are 50 columns, otherwise there are 10 columns.

The naming convention for the columns is as follows:
- For bit addresses: (meme_area)_(machine_no)_(reg_address_no).Bit[bit_position]
- For word addresses: (meme_area)_(machine_no)_(reg_address_no) or (meme_area)_(machine_no)_[index_no]

The work mode can be one of the following:
- 502.12-自動 (Automatic)
- 502.13-手動 (Manual)
- 502.14払出 (Payment)

"""
WORK_STATION_TABLE = {
    "Working_bit_reg":510,
    "OK_bit_reg" : 511,
    "NG_bit_reg" :512,
    "table" : {
        {"id" :"1", "DM_reg":"DM31651", "work_bit":"510.01", "OK_bit":"511.01", "NG_bit":"512.01"},
        {"id" :"2", "DM_reg":"DM31652", "work_bit":"510.02", "OK_bit":"511.02", "NG_bit":"512.02"},
        {"id" :"3", "DM_reg":"DM31653", "work_bit":"510.03", "OK_bit":"511.03", "NG_bit":"512.03"},
        {"id" :"4", "DM_reg":"DM31654", "work_bit":"510.04", "OK_bit":"511.04", "NG_bit":"512.04"},
        {"id" :"5", "DM_reg":"DM31655", "work_bit":"510.05", "OK_bit":"511.05", "NG_bit":"512.05"},
        {"id" :"6", "DM_reg":"DM31656", "work_bit":"510.06", "OK_bit":"511.06", "NG_bit":"512.06"},
        {"id" :"7", "DM_reg":"DM31657", "work_bit":"510.07", "OK_bit":"511.07", "NG_bit":"512.07"},
        {"id" :"8", "DM_reg":"DM31658", "work_bit":"510.08", "OK_bit":"511.08", "NG_bit":"512.08"},
        {"id" :"9", "DM_reg":"DM31659", "work_bit":"510.09", "OK_bit":"511.09", "NG_bit":"512.09"},
        {"id" :"10", "DM_reg":"DM31660", "work_bit":"510.10", "OK_bit":"511.10", "NG_bit":"512.10"},
        {"id" :"11", "DM_reg":"DM31661", "work_bit":"510.11", "OK_bit":"511.11", "NG_bit":"512.11"},
        {"id" :"12", "DM_reg":"DM31662", "work_bit":"510.12", "OK_bit":"511.12", "NG_bit":"512.12"},
        {"id" :"13", "DM_reg":"DM31663", "work_bit":"510.13", "OK_bit":"511.13", "NG_bit":"512.13"},
        {"id" :"14", "DM_reg":"DM31664", "work_bit":"510.14", "OK_bit":"511.14", "NG_bit":"512.14"},
        {"id" :"15", "DM_reg":"DM31665", "work_bit":"510.15", "OK_bit":"511.15", "NG_bit":"512.15"},  
    }
}
PRODUCTION_INFO_TABLE = {
    "table_name": "PRODUCTION_TABLE",
    "iot_info": {
        "no_of_columns": 63,
        "naming_convention": {1:"PLC<->sequencer"},
        "no_of_columns_depends_on_PLC":{"YES":53, "NO":10},
        "iot_naming_columns": {"bit_addr":"(meme_area)_(machine_no)_(reg_address_no).Bit[bit_position]",
                               "word_addr":"(meme_area)_(machine_no)_(reg_address_no) or (meme_area)_(machine_no)_[index_no]"},
        "V_work_mode":"[502.12-自動,502.13-手動,502.14払出]",
        "Work_station_pattern": WORK_STATION_TABLE,
    },
    "columns": {
        "日付": {
            "English_Name": "INSERT_DATE",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "勤務日付軸": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "昼夜勤": {
            "English_Name": "AB_SECTION_DAY",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "ユニットコード": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "工程順番": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "機番": {
            "English_Name": "Machine_No",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "時間帯": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "№": {
            "English_Name": "",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "numeric(10,0)",
            "Scale": "",
            "comment": "depends on reg index [DM31651: 1,..,DM31665:15]"
        },
        "ST": {
            "English_Name": "",
            "PLC_Depends": "NO",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "None"
        },
        "作業者": {
            "English_Name": "",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "[DM31601,DM31600]",
            "PLC_Data_Type": "DWORD",
            "Normal_Data_Type": "UDINT",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": ""
        },
        "機種": {
            "English_Name": "",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "depends on value in reg  [DM31651,..,DM31665]"
        },
        "背番号": {
            "English_Name": "",
            "PLC_Depends": "",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "translation of reg - as of now none"
        },
        "シリアル番号": {
            "English_Name": "",
            "PLC_Depends": "",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "ask once again"
        },
        "運転モード": {
            "English_Name": "V_work_mode",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "[502.12,502.13,502.14]",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "[502.12-自動,502.13-手動,502.14払出]"
        },
        "IN/OUT": {
            "English_Name": "",
            "PLC_Depends": "",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "Depends on bits of reg 510, [1:IN,0:OUT]"
        },
        "判定": {
            "English_Name": "",
            "PLC_Depends": "",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "Depends on 511 and 512 bits, if 511 bit active -OK, if 512 bit active NG"
        },
        "MT": {
            "English_Name": "MT_Timer",
            "PLC_Depends": "",
            "PLC_Memory_Address": "",
            "PLC_Data_Type": "",
            "Normal_Data_Type": "",
            "Sql_Data_Type": "",
            "Scale": "",
            "comment": "IN and OUT , the time taken"
        },
        "インデックス番号": {
            "English_Name": "Index_No",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31700",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "USINT",
            "Sql_Data_Type": "tinyint",
            "Scale": "",
            "comment": ""
        },
        "ﾄﾙｸ上限値": {
            "English_Name": "Torque_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31606",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "ﾄﾙｸ下限値": {
            "English_Name": "Torque_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31607",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "ﾄﾙｸﾎｰﾙﾄﾞ値": {
            "English_Name": "Torque_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31605",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "左低圧ﾎﾞﾙﾄ圧入高さﾎｰﾙﾄﾞ": {
            "English_Name": "L_Low_Bolt_Press_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31602",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "左低圧ﾎﾞﾙﾄ圧入高さ上限値": {
            "English_Name": "L_Low_Bolt_Press_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31603",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "左低圧ﾎﾞﾙﾄ圧入高さ下限値": {
            "English_Name": "L_Low_Bolt_Press_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31604",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "左高圧ﾎﾞﾙﾄ圧入高さﾎｰﾙﾄﾞ": {
            "English_Name": "L_High_Bolt_Press_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31605",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "左高圧ﾎﾞﾙﾄ圧入高さ上限値": {
            "English_Name": "L_High_Bolt_Press_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31606",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "左高圧ﾎﾞﾙﾄ圧入高さ下限値": {
            "English_Name": "L_High_Bolt_Press_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31607",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右低圧ﾎﾞﾙﾄ圧入高さﾎｰﾙﾄﾞ": {
            "English_Name": "R_Low_Bolt_Press_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31608",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右低圧ﾎﾞﾙﾄ圧入高さ上限値": {
            "English_Name": "R_Low_Bolt_Press_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31609",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右低圧ﾎﾞﾙﾄ圧入高さ下限値": {
            "English_Name": "R_Low_Bolt_Press_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31610",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右高圧ﾎﾞﾙﾄ圧入高さﾎｰﾙﾄﾞ": {
            "English_Name": "R_High_Bolt_Press_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31611",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右高圧ﾎﾞﾙﾄ圧入高さ上限値": {
            "English_Name": "R_High_Bolt_Press_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31612",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "右高圧ﾎﾞﾙﾄ圧入高さ下限値": {
            "English_Name": "R_High_Bolt_Press_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31613",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "3点ﾋﾟｯﾁ測定ﾎｰﾙﾄﾞ": {
            "English_Name": "Three_Points_Pitch_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31614",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.0]",
            "comment": "AM322"
        },
        "3点ﾋﾟｯﾁ測定上限値": {
            "English_Name": "Three_Points_Pitch_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31615",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.0]",
            "comment": "AM322"
        },
        "3点ﾋﾟｯﾁ測定下限値": {
            "English_Name": "Three_Points_Pitch_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31616",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.0]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ径ﾎｰﾙﾄﾞ": {
            "English_Name": "Plug_Dia_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31617",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ径上限値": {
            "English_Name": "Plug_Dia_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31618",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ径下限値": {
            "English_Name": "Plug_Dia_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31619",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ押えﾎｰﾙﾄﾞ": {
            "English_Name": "Plug_Push_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31620",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ押え上限値": {
            "English_Name": "Plug_Push_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31621",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "ﾌﾟﾗｸﾞ押え下限値": {
            "English_Name": "Plug_Push_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31622",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM322"
        },
        "割ﾋﾟﾝ孔位置ﾎｰﾙﾄﾞ": {
            "English_Name": "Split_Pin_Hole_Posi_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31602",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "割ﾋﾟﾝ孔位置上限値": {
            "English_Name": "Split_Pin_Hole_Posi_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31603",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "割ﾋﾟﾝ孔位置下限値": {
            "English_Name": "Split_Pin_Hole_Posi_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31604",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "ｶｼﾒ高さﾎｰﾙﾄﾞ値": {
            "English_Name": "RollFitting_Hight_Hold",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31608",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "ｶｼﾒ高さ上限値": {
            "English_Name": "RollFitting_Hight_UpLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31609",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "ｶｼﾒ高さ下限値": {
            "English_Name": "RollFitting_Hight_LoLimit",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31610",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "刻印振動検出回数": {
            "English_Name": "Stamp_Vibrate_Detect_Count",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31611",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        },
        "刻印振動回数設定": {
            "English_Name": "Stamp_Vibrate_Detect_Set_Count",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31612",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        },
        "完成品ｼﾘｱﾙ№": {
            "English_Name": "FinishProd_SERIAL_No",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31613",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        },
        "完成品ﾜｰｸ№": {
            "English_Name": "FinishProd_Work_No",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31614",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        },
        "完成品左低圧ﾎﾞﾙﾄ圧入高さ": {
            "English_Name": "FinishProd_L_Low_Bolt_Press_Hight",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31615",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品左高圧ﾎﾞﾙﾄ圧入高さ": {
            "English_Name": "FinishProd_L_High_Bolt_Press_Hight",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31616",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品右低圧ﾎﾞﾙﾄ圧入高さ": {
            "English_Name": "FinishProd_R_Low_Bolt_Press_Hight",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31617",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品右高圧ﾎﾞﾙﾄ圧入高さ": {
            "English_Name": "FinishProd_R_High_Bolt_Press_Hight",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31618",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品3点ﾋﾟｯﾁ測定": {
            "English_Name": "FinishProd_Three_Points_Pitch",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31619",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.0]",
            "comment": "AM323"
        },
        "完成品ﾌﾟﾗｸﾞ径": {
            "English_Name": "FinishProd_Plug_Dia",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31620",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品割ﾋﾟﾝ孔位置": {
            "English_Name": "FinishProd_Split_Pin_Hole_Posi",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31621",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        },
        "完成品ﾄﾙｸ": {
            "English_Name": "FinishProd_Torque",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31622",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品ｶｼﾒ高さ": {
            "English_Name": "FinishProd_RollFitting_Hight",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31623",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[.00]",
            "comment": "AM323"
        },
        "完成品刻印振動検出回数": {
            "English_Name": "FinishProd_Stamp_Vibrate_Detect_Count",
            "PLC_Depends": "YES",
            "PLC_Memory_Address": "DM31624",
            "PLC_Data_Type": "WORD",
            "Normal_Data_Type": "REAL",
            "Sql_Data_Type": "real",
            "Scale": "[0]",
            "comment": "AM323"
        }
    }
}
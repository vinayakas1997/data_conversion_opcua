from typing import List, Dict, Any, Optional
from .ACTUAL_TABLE import ACTUAL_TABLE
from .ERROR_TABLE import ERROR_TABLE
from .PRODUCTION_INFO_TABLE import PRODUCTION_INFO_TABLE
from .QTY_TABLE import QTY_TABLE


# ---------- Registry of Tables ----------
ALL_TABLES={
    "ACTUAL_TABLE": ACTUAL_TABLE,
    "ERROR_TABLE": ERROR_TABLE,
    "PRODUCTION_INFO_TABLE": PRODUCTION_INFO_TABLE,
    "QTY_TABLE": QTY_TABLE,
}

def get_table_config(table_name: str) -> Optional[Dict[str, Any]]:
    """Get complete configuration for a table."""
    return ALL_TABLES.get(table_name)


def get_column_names(table_name: str) -> List[str]:
    """Get list of column names for a table."""
    table = ALL_TABLES.get(table_name)
    return list(table['columns'].keys()) if table else []
from utils.checkers_utils.pma_utils.connection_utils import check_connection
from utils.file_utils.file_utils import save_json_line_by_line

def check_pma_connections(entries):
    success_results = []
    error_results = []

    for entry in entries:
        entry_result, error_result = check_connection(entry)
        if entry_result:
            success_results.append(entry_result)
            save_json_line_by_line([entry_result], "success.json")
        if error_result:
            error_results.append({"entry": entry, "error": error_result})
            save_json_line_by_line([{"entry": entry, "error": error_result}], "errors.json")
    
    return success_results, error_results

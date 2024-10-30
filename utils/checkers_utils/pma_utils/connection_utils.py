import requests
from urllib.parse import quote
from utils.output_formated.country_flags import get_flag

def check_connection(entry):
    url = entry["URL"]
    user = entry["DB_USERNAME"]
    password = entry["DB_PASSWORD"]
    country = entry["DBS_COUNTRY"]
    host = entry["DB_HOST"]
    database = entry["DB_DATABASE"]

    login_url = f"{url}?pma_username={quote(user)}&pma_password={quote(password)}"

    try:
        session = requests.Session()
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            token = extract_token(response.text)
            if not token:
                raise Exception("Token not found")
        else:
            raise Exception(f"Failed (Status Code: {response.status_code})")
    except requests.exceptions.SSLError:
        try:
            url = url.replace("https://", "http://")
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                token = extract_token(response.text)
                if not token:
                    raise Exception("Token not found")
            else:
                raise Exception(f"Failed (Status Code: {response.status_code})")
        except Exception as e:
            return None, f"{url} - {host} - {database} - ❌ {str(e)} {get_flag(country)}"
    except Exception as e:
        return None, f"{url} - {host} - {database} - ❌ {str(e)} {get_flag(country)}"

    try:
        auto_login_url = f"{url}?pma_username={quote(user)}&pma_password={quote(password)}&token={token}"
        entry["Result"] = "✅ Success"
        entry["Auto_Login_Link"] = auto_login_url
        entry["CountryFlag"] = get_flag(country)
        return entry, None
    except Exception as e:
        return None, f"{url} - {host} - {database} - ❌ {str(e)} {get_flag(country)}"

def extract_token(response_text):
    token_keyword = 'name="token" value="'
    start_index = response_text.find(token_keyword)
    if start_index != -1:
        start_index += len(token_keyword)
        end_index = response_text.find('"', start_index)
        if end_index != -1:
            return response_text[start_index:end_index]
    return None


""" Implementer uen fonction nde traitement dui token +"""
# codm_bot.py
import re
import json
from Utilities.until import load_accounts
from Api.Account import get_garena_token, get_major_login
from Api.InGame import get_player_personal_show, get_player_stats, search_account_by_keyword

# Load accounts once
accounts = load_accounts()

def get_search_account_by_keyword_command(region, search_term):
    try:
        region = region.upper()
        
        # Validate keyword parameter
        if not search_term:
            return json.dumps({"error": "Keyword parameter is required"}, indent=2, ensure_ascii=False)
        
        # Enforce minimum keyword length
        if len(search_term.strip()) < 3:
            return json.dumps({"error": "Keyword must be at least 3 characters long"}, indent=2, ensure_ascii=False)
        
        # Validate server exists in accounts
        if region not in accounts:
            return json.dumps({"error": f"Invalid server: {region}"}, indent=2, ensure_ascii=False)
        
        # Authenticate with Garena
        auth_response = get_garena_token(accounts[region]['uid'], accounts[region]['password'])
        if not auth_response or 'access_token' not in auth_response:
            return json.dumps({"error": "Authentication failed"}, indent=2, ensure_ascii=False)
        
        # Get major login credentials
        login_response = get_major_login(auth_response["access_token"], auth_response["open_id"])
        if not login_response or 'token' not in login_response:
            return json.dumps({"error": "Major login failed"}, indent=2, ensure_ascii=False)
        
        # Search for accounts
        search_results = search_account_by_keyword(login_response["serverUrl"], login_response["token"], search_term)
        
        # Return formatted response
        formatted_response = json.dumps(search_results, indent=2, ensure_ascii=False)
        return formatted_response
        
    except KeyError as e:
        return json.dumps({"error": f"Missing configuration: {str(e)}"}, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Internal server error: {str(e)}"}, indent=2, ensure_ascii=False)

def get_player_stats_command(server, uid, gamemode='br', matchmode='CAREER'):
    try:
        server = server.upper()
        gamemode = gamemode.lower()
        matchmode = matchmode.upper()

        # Validate required parameters
        if not uid:
            return json.dumps({
                "success": False,
                "error": "Missing required parameter",
                "message": "UID parameter is required"
            }, indent=2, ensure_ascii=False)

        if not uid.isdigit():
            return json.dumps({
                "success": False,
                "error": "Invalid UID",
                "message": "UID must be a numeric value"
            }, indent=2, ensure_ascii=False)

        # Validate server
        if server not in accounts:
            return json.dumps({
                "success": False,
                "error": "Invalid server",
                "message": f"Server '{server}' not found. Available servers: {list(accounts.keys())}"
            }, indent=2, ensure_ascii=False)

        # Validate gamemode
        if gamemode not in ['br', 'cs']:
            return json.dumps({
                "success": False,
                "error": "Invalid gamemode",
                "message": "Gamemode must be 'br' or 'cs'"
            }, indent=2, ensure_ascii=False)

        # Validate matchmode
        if matchmode not in ['CAREER', 'NORMAL', 'RANKED']:
            return json.dumps({
                "success": False,
                "error": "Invalid matchmode",
                "message": "Matchmode must be 'CAREER', 'NORMAL', or 'RANKED'"
            }, indent=2, ensure_ascii=False)

        # Step 1: Get Garena token
        try:
            garena_token_result = get_garena_token(accounts[server]['uid'], accounts[server]['password'])
            
            if not garena_token_result or 'access_token' not in garena_token_result:
                return json.dumps({
                    "success": False,
                    "error": "Garena authentication failed",
                    "message": "Failed to obtain Garena access token"
                }, indent=2, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": "Garena authentication error",
                "message": f"Failed to authenticate with Garena: {str(e)}"
            }, indent=2, ensure_ascii=False)

        # Step 2: Get Major login
        try:
            major_login_result = get_major_login(garena_token_result["access_token"], garena_token_result["open_id"])
            
            if not major_login_result or 'token' not in major_login_result:
                return json.dumps({
                    "success": False,
                    "error": "Major login failed",
                    "message": "Failed to obtain Major login token"
                }, indent=2, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": "Major login error",
                "message": f"Failed to login to Major: {str(e)}"
            }, indent=2, ensure_ascii=False)

        # Step 3: Get player stats
        try:
            player_stats = get_player_stats(
                major_login_result["token"], 
                major_login_result["serverUrl"], 
                gamemode, 
                uid, 
                matchmode
            )
            
            if not player_stats:
                return json.dumps({
                    "success": False,
                    "error": "No stats data",
                    "message": "No player statistics found for the given parameters"
                }, indent=2, ensure_ascii=False)

            # Return formatted JSON response
            return json.dumps({
                "success": True,
                "data": player_stats,
                "metadata": {
                    "server": server,
                    "uid": uid,
                    "gamemode": gamemode,
                    "matchmode": matchmode
                }
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": "Stats retrieval error",
                "message": f"Failed to retrieve player stats: {str(e)}"
            }, indent=2, ensure_ascii=False)

    except Exception as e:
        # Catch any unexpected errors
        return json.dumps({
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }, indent=2, ensure_ascii=False)

def get_player_personal_show_command(server, uid, need_gallery_info=False, call_sign_src=7):
    try:
        server = server.upper()
        
        # Validate UID parameter - must be integer
        if not uid:
            response = {
                "status": "error",
                "error": "Missing UID",
                "message": "Empty 'uid' parameter. Please provide a valid 'uid'.",
                "code": "MISSING_UID"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Check if UID is a valid integer
        try:
            uid_int = int(uid)
            # Additional validation for UID range if needed
            if uid_int <= 0:
                response = {
                    "status": "error",
                    "error": "Invalid UID",
                    "message": "UID must be a positive integer.",
                    "code": "INVALID_UID_RANGE"
                }
                return json.dumps(response, indent=2, ensure_ascii=False)
        except (ValueError, TypeError):
            response = {
                "status": "error",
                "error": "Invalid UID",
                "message": "UID must be a valid integer.",
                "code": "INVALID_UID_FORMAT"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Validate server parameter
        if server not in accounts:
            response = {
                "status": "error",
                "error": "Invalid Server",
                "message": f"Server '{server}' not found. Available servers: {list(accounts.keys())}",
                "available_servers": list(accounts.keys()),
                "code": "SERVER_NOT_FOUND"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Validate need_gallery_info parameter
        try:
            if isinstance(need_gallery_info, str):
                if need_gallery_info.lower() in ['true', '1', 'yes']:
                    need_gallery_info = True
                elif need_gallery_info.lower() in ['false', '0', 'no']:
                    need_gallery_info = False
                else:
                    raise ValueError("Invalid boolean value")
            need_gallery_info = bool(need_gallery_info)
        except (ValueError, TypeError):
            response = {
                "status": "error",
                "error": "Invalid Parameter",
                "message": "need_gallery_info must be a boolean value (true/false, 1/0).",
                "code": "INVALID_GALLERY_PARAM"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Validate call_sign_src parameter
        try:
            call_sign_src_int = int(call_sign_src)
            if call_sign_src_int < 0:
                response = {
                    "status": "error",
                    "error": "Invalid Parameter",
                    "message": "call_sign_src must be a non-negative integer.",
                    "code": "INVALID_CALL_SIGN_SRC"
                }
                return json.dumps(response, indent=2, ensure_ascii=False)
        except (ValueError, TypeError):
            response = {
                "status": "error",
                "error": "Invalid Parameter",
                "message": "call_sign_src must be a valid integer.",
                "code": "INVALID_CALL_SIGN_FORMAT"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Check if server account credentials exist
        if 'uid' not in accounts[server] or 'password' not in accounts[server]:
            response = {
                "status": "error",
                "error": "Server Configuration Error",
                "message": f"Server '{server}' is missing required credentials.",
                "code": "SERVER_CONFIG_ERROR"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Step 1: Get Garena token
        garena_token_result = get_garena_token(accounts[server]['uid'], accounts[server]['password'])
        if not garena_token_result or 'access_token' not in garena_token_result or 'open_id' not in garena_token_result:
            response = {
                "status": "error",
                "error": "Authentication Failed",
                "message": "Failed to obtain Garena token. Invalid credentials or service unavailable.",
                "code": "GARENA_AUTH_FAILED"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Step 2: Get major login
        major_login_result = get_major_login(garena_token_result["access_token"], garena_token_result["open_id"])
        if not major_login_result or 'serverUrl' not in major_login_result or 'token' not in major_login_result:
            response = {
                "status": "error",
                "error": "Login Failed",
                "message": "Failed to perform major login. Service unavailable.",
                "code": "MAJOR_LOGIN_FAILED"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Step 3: Get player personal show data
        player_personal_show_result = get_player_personal_show(
            major_login_result["serverUrl"], 
            major_login_result["token"], 
            uid_int, 
            need_gallery_info, 
            call_sign_src_int
        )

        if not player_personal_show_result:
            response = {
                "status": "error",
                "error": "Data Not Found",
                "message": f"No player data found for UID: {uid_int}",
                "code": "PLAYER_DATA_NOT_FOUND"
            }
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Success response
        formatted_json = json.dumps(player_personal_show_result, indent=2, ensure_ascii=False)
        return formatted_json
    
    except Exception as e:
        response = {
            "status": "error",
            "error": "Internal Server Error",
            "message": "An unexpected error occurred while processing your request.",
            "code": "INTERNAL_SERVER_ERROR"
        }
        return json.dumps(response, indent=2, ensure_ascii=False)

# Command processor for bot
def process_command(command_text):
    """
    Process bot commands in format:
    /info bd 3999072239          # Get profile
    /info bd 3999072239 br       # Get stats with gamemode
    /info bd (name)=HelloWorld   # Search player
    """
    
    command_text = command_text.strip()
    
    # Remove /info prefix if present
    if command_text.startswith('/info '):
        command_text = command_text[6:]
    
    # Split command into parts
    parts = command_text.split()
    
    if len(parts) < 2:
        return json.dumps({"error": "Invalid command format. Use: /info server uid [gamemode] or /info server (name)=keyword"}, indent=2, ensure_ascii=False)
    
    # Server mapping
    server_mapping = {
        'bd': 'IND', 'id': 'ID', 'sg': 'SG', 'ru': 'RU',
        'tw': 'TW', 'us': 'US', 'vn': 'VN', 'th': 'TH',
        'me': 'ME', 'pk': 'PK', 'cis': 'CIS', 'br': 'BR',
        'na': 'NA', 'sac': 'SAC', 'eu': 'EU'
    }
    
    # Get server
    input_server = parts[0].lower()
    if input_server not in server_mapping:
        return json.dumps({"error": f"Invalid server: {input_server}"}, indent=2, ensure_ascii=False)
    
    actual_server = server_mapping[input_server]
    
    # Check if it's a search command (name)=value
    if '(' in parts[1] and ')' in parts[1]:
        # Join all parts after server for keyword extraction
        remaining_text = ' '.join(parts[1:])
        match = re.search(r'\(name\)=(.+)', remaining_text)
        if match:
            keyword = match.group(1)
            return get_search_account_by_keyword_command(actual_server, keyword)
        else:
            return json.dumps({"error": "Invalid search format. Use: (name)=keyword"}, indent=2, ensure_ascii=False)
    
    # Get UID
    uid = parts[1]
    
    # Check if gamemode provided
    if len(parts) > 2:
        gamemode = parts[2].lower()
        if gamemode not in ['br', 'cs']:
            return json.dumps({"error": "Invalid gamemode. Must be 'br' or 'cs'"}, indent=2, ensure_ascii=False)
        return get_player_stats_command(actual_server, uid, gamemode)
    else:
        # No gamemode = get profile
        return get_player_personal_show_command(actual_server, uid)

# Main function to be called from bot
def handle_bot_command(command_text):
    result = process_command(command_text)
    return result

# For local testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        result = handle_bot_command(command)
        print(result)
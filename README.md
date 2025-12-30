<div align="center">
  <img src="https://raw.githubusercontent.com/0xMe/FreeFire-Api/refs/heads/main/API.png" alt="API Screenshot">
</div>

# FreeFire-Api

FreeFire-Api is a lightweight Python project that interacts with internal Free Fire APIs using compiled Protocol Buffers. It enables structured API communication, making it easier to parse, encode, and serve game-related data such as player profiles, regions, and server details.

## Features

- Interacts directly with Free Fire's internal game APIs.
- Uses Protocol Buffers for serialization and deserialization of network messages.
- Provides endpoints for player statistics, personal show data, and more.
- Implements encryption for secure API communication.
- Built with Flask for easy RESTful API deployment.

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/0xMe/FreeFire-Api.git
   cd FreeFire-Api
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Add your account credentials to `./Configuration/AccountConfiguration.json` for each supported server.
   - Make sure your protobuf files are compiled and available in `Proto/compiled/`.

4. **Run the API server**
   ```sh
   python app.py
   ```
   The API will run on `http://0.0.0.0:5000`.

## Usage

### REST Endpoints

#### Get Player Stats

`GET /get_player_stats`

Query Parameters:
- `server` (default: "IND") — The server region.
- `uid` — The player UID.
- `gamemode` (default: "br") — Game mode (`br`, `cs`).
- `matchmode` (default: "CAREER") — Match mode. (`CAREER`, `NORMAL`, `RANKED`)

Example:
    https://ff-info-api-1.onrender.com/get_player_stats?server=ind&uid=11959685790&matchmode=RANKED&gamemode=br

#### Get Player Personal Show

`GET /get_player_personal_show`

Query Parameters:
- `server` (default: "IND") — The server region.
- `uid` — The player UID.
- `need_gallery_info` (optional) — Whether to include gallery info.
- `call_sign_src` (default: 7) — Call sign source.

Example:
    https://ff-info-api-1.onrender.com/get_player_personal_show?server=ind&uid=1633864660

#### Search Account By Keyword

`GET /get_search_account_by_keyword`

Query Parameters:
- `server` (default: "IND") — The server region.
- `keyword` — The Keyword.

Example:
    https://ff-info-api-1.onrender.com/get_search_account_by_keyword?server=ind&keyword=Hello

### API Responses

Responses are in JSON format. Example error messages are provided for invalid parameters, authentication failures, and data not found.

## Project Structure

- `app.py` — Flask application with REST endpoints.
- `Api/Account.py` — Garena authentication and login functions.
- `Api/InGame.py` — Game data retrieval functions.
- `Utilities/until.py` — Utility functions for encryption and protocol buffer handling.
- `Configuration/` — Contains configuration files, including AES keys and API version.

## Requirements

- Python
- Flask
- pycryptodome
- protobuf

Refer to `requirements.txt` for additional dependencies.
1. **IND** → ভারত সার্ভার  
2. **BR** → ব্রাজিল সার্ভার  
3. **SG** → সিঙ্গাপুর সার্ভার  
4. **RU** → রাশিয়া সার্ভার  
5. **ID** → ইন্দোনেশিয়া সার্ভার  
6. **TW** → তাইওয়ান সার্ভার  
7. **US** → মার্কিন যুক্তরাষ্ট্র সার্ভার  
8. **VN** → ভিয়েতনাম সার্ভার  
9. **TH** → থাইল্যান্ড সার্ভার  
10. **ME** → মধ্যপ্রাচ্য সার্ভার  
11. **PK** → পাকিস্তান সার্ভার  
12. **CIS** → রাশিয়া ও পার্শ্ববর্তী দেশ সার্ভার  
13. **BD** → বাংলাদেশ সার্ভার  
14. **NA** → উত্তর আমেরিকা সার্ভার  
15. **SAC** → দক্ষিণ আমেরিকা/ল্যাটিন আমেরিকা সার্ভার  
16. **EU** → ইউরোপ সার্ভার
## Deployment

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F0xMe%2FFreeFire-Api)

## Contributing

Feel free to fork and submit pull requests. Open issues for bug reports and feature requests.

## Author

[0xMe](https://github.com/0xMe)

import requests
import json 
import base64

# TODO: move these into a file/environment variable external to the code
client_ID = "e4e9b57363d9471e9ffdf7ebf70818bf"
client_secret = "2d1efcd217104009b91d263f7458ac67"

auth_endpoint = "https://accounts.spotify.com/api/token"
search_API_endpoint = "https://api.spotify.com/v1/search"

# get access token to use for authentication with search api
def get_access_token():
    # from Spotify docs:
    # Required: Base 64 encoded string that contains the client ID and client secret key. 
    # The field must have the format: 
    # Authorization: Basic *<base64 encoded client_id:client_secret>*
    message = client_ID + ":" + client_secret
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    encoded_client_details = base64_bytes.decode("ascii")
    
    headers = {"Authorization": "Basic " + encoded_client_details}              
    body = {"grant_type": "client_credentials"}
    response = requests.post(url=auth_endpoint, headers=headers, data=body)
    json_object = json.loads(response.text)
    return json_object["access_token"]
    
# make the request using requests module
# need to send the access token via request headers
def make_request(access_token, full_url):
    headers = {"Accept": "application/json", 
               "Content-Type": "application/json", 
               "Authorization": "Bearer " + access_token}

    response = requests.get(url=full_url, headers=headers)
    json_object = json.loads(response.text)

    return json_object

# create request url, make request, return JSON response
def search_request(access_token, search_term, search_type):
    search_term = requests.utils.quote(search_term)
    search_type = requests.utils.quote(search_type)
    url = search_API_endpoint + "?q=" + search_term
    url += "&type=" + search_type
    url += "&limit=1"
    json_obj = make_request(access_token, url)
    return json_obj

def get_id(track_name):
    json_obj = search_request(access_token, track_name, "track")
    return json_obj['tracks']['items'][0]['id']
    
def get_features(track_name):
    try:
        access_token = get_access_token()
        song_id = get_id(track_name)
        url = "https://api.spotify.com/v1/audio-features/" + song_id
        json_obj = make_request(access_token, url)
        return json_obj
    except:
        return None
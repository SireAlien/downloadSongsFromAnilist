import requests
import re
from mutagen.easyid3 import EasyID3
from mutagen import File

url = "https://anisongdb.com/api/"
songTypes = {
    "ALL": "ALL",
    "OP": "Opening",
    "ED": "Ending",
    "IN": "Insert"
}

def getSongListFromTitle(title):
    while True:
        response = requests.post(f"{url}search_request", 
                                headers={"Accept": "application/json", "content-type": "application/json"},
                                json={"anime_search_filter": {
                                    "search": title, 
                                    "partial_match": True,
                                    "chanting": False,
                                    "instrumental": False,
                                    "rebroadcast": False,
                                    "dub": False}})
        if response.json() or not title:
            break
        else:
            title = title[:-1]
    print(f"Found {len(response.json())} songs for {title}.")
    return response.json()

def getSongsFromTitle_SongType(title, songType):
    entries = getSongListFromTitle(title)
    if songType == "ALL":
        return entries
    result = []
    for entry in entries:
        if entry['songType'].split(' ')[0] == songType:
            result.append(entry)
    return result

def filterSongsByID(songList, idList):
    result = []
    for entry in songList:
        print(f"Checking {entry['linked_ids']['anilist']} against {idList}")
        if entry["linked_ids"]["anilist"] in idList:
            result.append(entry)

    return result

def getMp3ListFromSongList(list, language):
    mp3List = []
    print( f"Filtering songs for unique song IDs of {len(list)}")
    songIdList = set()
    for entry in list:
        print(entry[language])
        if entry["amqSongId"] not in songIdList:
            songIdList.add(entry["amqSongId"])
            mp3List.append({"songId" : entry["amqSongId"], 
                            "id": entry["linked_ids"]["anilist"],
                            "name" : entry["songName"],
                            "artist": entry["songArtist"], 
                            "title": entry[language],  #can use animeENName 
                            "type": entry['songType'], 
                            "link": f"https://naedist.animemusicquiz.com/{entry['audio']}"})
    return mp3List

def downloadMp3FromLinkList(linklist, path = "./"):
    success = False
    for entry in linklist:
        print(f"Attempting to download {entry['name']}...")
        success = downloadMp3FromLink(entry, path) or success
    return success

def downloadMp3FromLink(entry, path = "./"):
    response = requests.get(entry['link'])
    if response.status_code != 200:
        print(f"Failed to download {entry['name']}. Status code: {response.status_code}")
        return False 
    filename = f"{re.sub(r'[^a-zA-Z0-9!\s-]', '',entry['title'])} - {entry['type']} - {entry['songId']}.mp3"
    print(f"Downloading {filename}...")
    with open(f"{path}/{filename}", "wb") as f:
        f.write(response.content)
        if (f.tell() < 0): return False
    try:
        audio = EasyID3(f"{path}/{filename}")
    except:
        audio = File(f"{path}/{filename}", easy=True)
        audio.add_tags()
    print(f"Setting metadata...")
    audio["title"] = entry['name']
    audio["artist"] = entry['artist']
    audio.save()
    return True

def downloadMp3FromTitle_SongType(title, songType, language, path):    
    return downloadMp3FromLinkList(
        getMp3ListFromSongList(
            getSongsFromTitle_SongType(title, songType), language), path)

def downloadMp3FromTitle_ID_SongType(title, idList, songType, language, path):    
    if title is None:
        return False
    return downloadMp3FromLinkList(
        getMp3ListFromSongList(
            filterSongsByID(
                getSongsFromTitle_SongType(title, songType),
                    idList), language), path)

def downloadMp3FromTitles_ID_SongType(title1, title2, idList, songType, language, path):  
    print(f"Trying to download songs for {title1}...")
    success = downloadMp3FromTitle_ID_SongType(title1, idList, songType, language, path)
    if not success:
        success = downloadMp3FromTitle_ID_SongType(title2, idList, songType, language, path)
    return success
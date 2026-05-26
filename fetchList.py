import requests

# Here we define our query as a multi-line string
query_getListCollection_fromUserName= '''
query ($userName: String!) { # Define which variables will be used in the query (id)
  MediaListCollection (type: ANIME, userName: $userName) { # Insert our variables into the query arguments (id)
    lists {
      name
      entries {
        id
        media {
          id
          title {
            romaji
            english
          }
        }
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'


def getListCollectionFromName(name):
    # Make the HTTP Api requests
    response = requests.post(url, json={'query': query_getListCollection_fromUserName, 'variables': {'userName': name}})
    return response.json()['data']['MediaListCollection']

def getListFromListCollection(collection, listName):
    for alist in collection['lists']:
        if alist['name'].lower() == listName.lower():
            return alist
    print(f"List '{listName}' not found.")
    return None

def getTitlesFromList(list, language):
    if language == "JP":
        language = "romaji"
    elif language == "EN":
        language = "english"
    titles = []
    for entry in list['entries']:
        titles.append(entry['media']['title'][language])
    return titles

def getTitlesFromUsername_List_Language(username, listName, language):
    collection = getListCollectionFromName(username)
    if collection:
        alist = getListFromListCollection(collection, listName)
        if alist:
            return getTitlesFromList(alist, language)
    return None

def getIDsFromList(list):
    ids = []
    for entry in list['entries']:
        ids.append(entry['media']['id'])
    return ids

def getIDsFromUsername_List(username, listName):
    collection = getListCollectionFromName(username)
    if collection:
        alist = getListFromListCollection(collection, listName)
        if alist:
            return getIDsFromList(alist)
    return None

def getAnimeFromUsername_List(username, listName):
    titlesEN = getTitlesFromUsername_List_Language(username, listName, "EN")
    titlesJP = getTitlesFromUsername_List_Language(username, listName, "JP")
    ids = getIDsFromUsername_List(username, listName)
    anime = []
    for i in range(len(titlesEN)):
        anime.append((titlesEN[i], titlesJP[i], ids[i]))
    return anime
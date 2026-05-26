import fetchList as fl
import fetchSongs as fs


def downloadMp3FromUsername_List_SongType_Language(username, listName, songType, language, path):
    anime = fl.getAnimeFromUsername_List(username, listName)
    language = f'anime{language}Name'
    for titleEN, titleJP, id in anime:
        fs.downloadMp3FromTitles_ID_SongType(titleJP, titleEN, [id], fs.songTypes[songType], language, path)

if __name__ == "__main__":
    name = input("AniList username: ")
    listName = input("List you want to fetch: ")
    songType = input("Song type (ALL, OP, ED, IN): ") 
    filepath = input("File path to save songs (default is current directory): ") or "./"
    language = input("Language for filename (JP, EN): ")
    language = f'anime{language}Name'

    downloadMp3FromUsername_List_SongType_Language(name, listName, songType, language, filepath)
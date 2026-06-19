import fetchList as fl
import fetchSongs as fs


def downloadMp3FromUsername_List_SongTypes_Language(username, listName, songTypes, language, path):
    anime = fl.getAnimeFromUsername_List(username, listName)
    language = f'anime{language}Name'
    for titleEN, titleJP, id in anime:
        fs.downloadMp3FromTitles_ID_SongTypes(titleJP, titleEN, [id], songTypes, language, path)

if __name__ == "__main__":
    name = input("AniList username: ")
    listName = input("List you want to fetch: ")
    songTypes = [fs.songTypes[x] for x in input("Song type (OP, ED, IN): ").split(",")]
    filepath = input("File path to save songs (default is current directory): ") or "./"
    language = input("Language for filename (JP, EN): ")
    language = f'anime{language}Name'

    downloadMp3FromUsername_List_SongTypes_Language(name, listName, songTypes, language, filepath)

import re
import sys
import pathlib
import shutil

def handle_image(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'images'
    target_folder.mkdir(exit_ok = True)
    path.replace(target_folder/path.name)

def handle_video(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'videos'
    target_folder.mkdir(exit_ok = True)
    path.replace(target_folder/path.name)

def handle_documents(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'documents'
    target_folder.mkdir(exit_ok = True)
    path.replace(target_folder/path.name)

def handle_audio(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'audio'
    target_folder.mkdir(exit_ok = True)
    path.replace(target_folder/path.name)

def handle_archive(path: pathlib.Path, root_folder: pathlib.Path):
    target_folder = root_folder / 'archives'
    name, _ = split_extension(path.name)
    target_folder.mkdir(exit_ok = True)
    archive_folder = target_folder / name
    archive_folder.mkdir(exit_ok = True)
    try:
        shutil.unpack_archive(str(path.absolute())), str(archive_folder.absolute())
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    path.unlink()


def handle_folder(path: pathlib.Path):
    try:
        path.rmdir()
    except OSError:
        pass

#define folders names and extensions of the files   
Images = []
Audio = []
Video = []
Documents = [] 
Archives = []
Folders = []
#Extensions to loop through in the folder and associate with the file type
Extensions = {
'jpeg': Images, 
'png': Images, 
'jpg': Images, 
'svg': Images,
'avi': Video, 
'mp4': Video, 
'mov': Video,
'mkv': Video,
'doc': Documents, 
'docx': Documents, 
'txt': Documents, 
'pdf': Documents, 
'xlsx': Documents, 
'pptx': Documents,
'mp3': Audio, 
'ogg': Audio, 
'wav': Audio, 
'amr': Audio,
'zip': Archives, 
'gz': Archives, 
'tar': Archives,
}

#Clean the files names and rename to english alphabet
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъьыэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c,l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

#function to translate names to english symbols
def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name
  
def split_extension(file_name: str):
    ext_start = 0
    for idx, char in enumerate(file_name):
        if char == '.':
            ext_start = idx
    name = file_name[:ext_start]
    extension = file_name[ext_start+1:].upper()
    if not ext_start:
        return file_name, ''
    return name, extension

#check if item is folder, rename folder, create folder if does not exist
def scan(folder: pathlib.Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('images', 'videos', 'documents', 'archives'):
                Folders.append(item)
                scan(item)
            continue
        name, extension = split_extension(file_name=item.name)
        new_name = normalize(name)
        new_item = folder / '.'.join([new_name, extension.lower()])
        item.rename(new_item)
        if extension:
            try:
                container = Extensions[extension]
                container.append(new_item)
            except KeyError:
                continue

#sort files to folders by extension
def main() -> None:
    path = sys.argv[1]
    print(f'Start in {path}')
    folder = pathlib.Path(path)
    scan(folder)

    for file in Images:
        handle_image(file, folder)
    
    for file in Video:
        handle_video(file, folder)
    
    for file in Audio:
        handle_audio(file, folder)
    
    for file in Documents:
        handle_documents(file, folder)
    
    for file in Archives:
        handle_archive(file, folder)

    for f in Folders[::-1]:
        handle_folder(f)


if __name__ == '__main__':
    main()




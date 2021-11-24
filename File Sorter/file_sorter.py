extensions = set()
unknown_extensions = set()

#Folders to sort:
folders = ('images', 'audio', 'video', 'documents', 'archives')

images = ('.jpeg', '.png', '.jpg', '.svg')
video = ('avi', 'mp4', 'mov', 'mkv')
docs = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
audio = ('mp3', 'ogg', 'wav', 'amr')
archive = ('zip', 'gz', 'tar')

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъьыэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}

def normalize(filename):
  for c,l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

  new_name = ''

  for ch in filename:
      new_ch = TRANS.hget(ord(ch))
      if new_ch:
          new_name += new_ch
      elif 97 <= ord(ch) <= 122 or 65 <= ord(ch) <= 90 or 49 <= ord(ch) <= 57:
          new_name = ch
      else:
          new_name += '_'
  return new_name


def sort_folders(p:Path):
    for item in p.iterdir():
        if item.is_dir():
            if item.name in folders:
                continue
            elif len(os.iterdir(item)) == 0 and item.name not in folders:
                shutil.rmtree(item)
            else:
                new_name = normalize(item.name)
                new_file = Path(f'{item.parent}/{new_name}')
                os.rename(item, new_file)
                
                sort_folders(new_file)
        elif item.is_file():
            sort_folders(item)

def rename_file(p, new_name, extension):
    p.rename(Path(p.parent, new_name + extension))
    new_file = Path(new_name + extension)
    return new_file

def file_to_list(new_name, extension = ''):
    if extension in images:
        images.append(new_name + extension)
        extensions.add(extension)
        return 'images'
    elif extension in video:
        files_video.append(new_name + extension)
        extensions.add(extension)
        return 'video'
        
    elif extension in docs:
        files_docs.append(new_name + extension)
        extensions.add(extension)
        return 'docs'
        
    elif extension in audio:
        files_audio.append(new_name + extension)
        extensions.add(extension)
        return 'audio'
                
    elif extension in archive:
        files_archives.append(new_name + extension)
        extensions.add(extension)
        return 'archive'
    else:
        file_unknown.append(new_name + extension)
        if extension:
            unknown_extensions.add(extension)
            

def file_sorter(p:Path):
    extension = p.suffix
    name = p.stem
    
    new_name = normalize(name)
    new_file = rename_file(p, new_name, extension)
    folder = file_to_list(new_name, extension)
    
    if extension in images or extension in video or extension in docs or extension in audio:
        shutil.move(f'{p.parent}/{new_file}'), f'{MAIN_FOLDER}/{folder}/{new_file}')
        
    elif extension in archive:
        shutil.unpack_archive((f'{p.parent}/{new_file}'), f'{MAIN_FOLDER}/archives/{new_file}')
        os.remove(f'{p.parent}/{new_file}')
        
if __name__ == '__main__':
    try:
        p = Path(sys.argv[1])
    except:
        print('No path has been specified - enter an argument')
    
    MAIN_FOLDER = p
        
     


    
import re, os, stat
import json

separator = '\\'
class MovieName:
    def __init__(self):
        self.name = ''
        self.year = ''
        self.encoding = ''
        self.rip = ''
        self.resolution = ''


class MovieDir:
    def __init__(self):
        self.full_name = ''
        self.name = ''
        self.year = ''
        self.resolution = ''

    def write_original_name(self, file_dir):
        fileinfo = dict()
        fileinfo['original_name'] = self.full_name
        files = os.listdir(file_dir)
        for file in files:
            full = file_dir + '/' + file
            if file.endswith('.jpg'):
                print(full)
                os.chmod(full, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                os.unlink(full)
            if file.lower().startswith('rarb'):
                print(full)
                os.chmod(full, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                os.unlink(full)
        fileinfo['files'] = files
        with open(os.path.join(file_dir, 'original.json'), "w") as fp:
            json.dump(fileinfo, fp, indent=4)

    def get_resolution(self):
        for r in ['720p', '1080p']:
            if r in self.full_name:
                self.resolution = r
                return r
        return ''

    def get_year_and_name(self):
        movie_name = re.sub(r'(\s+|\.|_)', ' ', self.full_name)
        g1 = re.search(r'(\(*(19|20)(\d\d)\)*)', movie_name)
        if g1:
            year_split = g1.group(1)
            year = g1.group(2) + g1.group(3)
            movie_name_split = movie_name.split(year_split)
            self.name = movie_name_split[0].strip()
            self.year = '('+year+')'
                # print(self.name, self.year)
            return 1
        return 0

    def get_files_w_extensions(self, file_dir, extensions):
        files = os.listdir(file_dir)
        for file in files:
            name, ext = os.path.splitext(file)
            if not ext in extensions:
                print(file, ext)
                extensions.append(ext)
        return files


class DirectoryWalker:
    def __init__(self, fp, separator='/'):
        self.full_path = fp
        self.separator = '/'
        self.visit_files = True
        self.dir_skip_cb = None
        self.file_skip_cb = None
        self.dir_action_cb = None
        self.file_action_cb = None
        self.dir_action_results = None
        self.file_action_results = None

    def walk(self):
        cnt = 0
        extensions = []
        slashes = self.full_path.count(separator)
        for root, dirs, files in os.walk(self.full_path):
            if separator == '/':
                root = re.sub(r'\\', separator, root)
            if self.dir_skip_cb and self.dir_skip_cb(root, dirs, files, slashes):
                continue

            if self.dir_action_cb:
                self.dir_action_cb(root, dirs, files, slashes)

            for file in files:
                full = root + self.separator + file
                if self.file_skip_cb and self.file_skip_cb(full, file, slashes):
                    continue


def remove_words(name):
    return


def delete_file(full, delete=True):
    if delete:
        os.chmod(full, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.unlink(full)
        if not os.path.exists(full):
            print(f'removed {full}')


def clean_unwanted_files(basedir, delete=True):
    cnt = 0
    extensions = []
    slashes = basedir.count(separator)
    for root, dirs, files in os.walk(basedir):
        if separator == '/':
            root = re.sub(r'\\', separator, root)
        if not root.count(separator) == slashes + 1:
            continue
        print(root)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext not in extensions:
                extensions.append(ext)
            full = root + separator + file
            print(full)
            filelower = file.lower()
            if 'torrentpartfile' in filelower:
                delete_file(full)
            if file.endswith('.nfo'):
                delete_file(full)
            for ext in ['jpg', '.nfo']:
                if file.endswith(ext):
                    print(file)
    print('Extensions:', extensions)
    return


def start(basedir):
    cnt = 0
    extensions = []
    slashes = basedir.count(separator)
    for root, dirs, files in os.walk(basedir):
        if separator == '/':
            root = re.sub(r'\\', separator, root)
        if not root.count(separator) == slashes + 1:
            continue
        movie_name = os.path.basename(root)
        md = MovieDir()
        md.full_name = movie_name
        # md.write_original_name(root)
        resolution = md.get_resolution()
        succ = md.get_year_and_name()
        cnt += succ
        if succ:
            files = md.get_files_w_extensions(root, extensions)
    print('Movies:', cnt)
    print('Extensions:', extensions)
        # else:
        #     print(root, movie_name)

def traverse_directory(dir_name, action_function):
    cnt = 0
    slashes = dir_name.count(separator)
    for root, dirs, files in os.walk(dir_name):
        root = re.sub(r'\\', '/', root)


# start('\\\\RASPBERRYPI\\pi_seagate_4tb_1\\trial')
clean_unwanted_files('\\\\RASPBERRYPI\\pi_seagate_4tb_1\\media\\trial', delete=False)

import os

def construct_file_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", *args)

def construct_assets_path(*args):
        return os.path.join((os.path.dirname(__file__)), "..", "..", "assets", *args)
    
def construct_media_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "assets", "media", *args)

def construct_root_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "..", *args)

def construct_data_path(*args):
    return os.path.join((os.path.dirname(__file__)), "..", "..", "data", *args)
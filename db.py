import glob
from os.path import expanduser, isdir

from todoman.configuration import ConfigurationException, load_config
from todoman.interactive import TodoEditor
from todoman.model import cached_property, Database, Todo


def get_todos():
    config = load_config()
    paths = [
        path for path in glob.iglob(expanduser(config['main']['path']))
        if isdir(path)
    ]

    if not len(paths):
        raise Exception('No todos found!')

    db = Database(paths, config['main']['cache_path'])
    return db.todos(status='ANY')

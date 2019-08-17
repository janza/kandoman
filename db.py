import glob
from os.path import expanduser, isdir

from todoman.configuration import ConfigurationException, load_config
from todoman.interactive import TodoEditor
from todoman.model import cached_property, Database, Todo


class TodoMan():
    def __init__(self):
        config = load_config()
        paths = [
            path for path in glob.iglob(expanduser(config['main']['path']))
            if isdir(path)
        ]

        if not paths:
            raise Exception('No todos found!')

        self.db = Database(paths, config['main']['cache_path'])

    def get_todos(self):
        return self.db.todos(status='ANY')


    def _set_status(self, todo, status):
        todo.status = status
        self.db.save(todo)


    def todo(self, todo):
        todo.completed_at = None
        todo.percent_complete = 0
        self._set_status(todo, 'NEEDS-ACTION')

    def in_progress(self, todo):
        todo.completed_at = None
        self._set_status(todo, 'IN-PROCESS')

    def done(self, todo):
        todo.complete()
        self.db.save(todo)

    def cancel(self, todo):
        todo.cancel()
        self.db.save(todo)

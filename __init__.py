import os
import importlib
import cudatext as app
from cudatext import ed

class Command:
    helpers = {}

    def __init__(self):
        self.h_tree = app.app_proc(app.PROC_GET_CODETREE, '')

        dir = app.app_path(app.APP_DIR_PY)
        dirs = os.listdir(dir)
        dirs = [s for s in dirs if s.startswith('cuda_tree_') and os.path.isdir(os.path.join(dir, s))]
        for dir in dirs:
            try:
                _m = importlib.import_module(dir)
                self.helpers.update(_m.helper)
                #print(self.helpers)
            except ImportError:
                pass

        items = sorted(list(self.helpers.keys()))
        if items:
            print('TreeHelpers: ' + ', '.join(items))


    def update_tree(self, lexer):
        getter = self.helpers.get(lexer)
        if not getter: return

        filename = ed.get_filename()
        lines = ed.get_text_all().split("\n")
        heads = list(getter(filename, lines))

        ed.set_prop(app.PROP_CODETREE, False)
        app.tree_proc(self.h_tree, app.TREE_ITEM_DELETE, 0)
        last_levels = {0: 0}
        for index, (line_number, level, header) in enumerate(heads):
            for test_level in reversed(range(level)):
                parent = last_levels.get(test_level)
                if parent is None:
                    continue
                identity = app.tree_proc(self.h_tree, app.TREE_ITEM_ADD, parent, index=-1, text=header)
                # when adding level K, forget all levels > K
                last_levels = {k: v for k, v in last_levels.items() if k <= level}
                last_levels[level] = identity
                if index == len(heads) - 1:
                    end_y = len(lines) - 1
                    end_x = len(ed.get_text_line(end_y))
                else:
                    end_y = heads[index + 1][0]  # line_index of next header
                    end_x = 0
                rng = (0, line_number, end_x, end_y)
                app.tree_proc(self.h_tree, app.TREE_ITEM_SET_RANGE, identity, index=-1, text=rng)
                break

    def check_and_update(self, ed_self):
        lexer = ed_self.get_prop(app.PROP_LEXER_FILE)
        if lexer and (lexer in self.helpers):
            self.update_tree(lexer)

    def on_change_slow(self, ed_self):
        self.check_and_update(ed_self)

    def on_open(self, ed_self):
        self.check_and_update(ed_self)

    def on_tab_change(self, ed_self):
        self.check_and_update(ed_self)

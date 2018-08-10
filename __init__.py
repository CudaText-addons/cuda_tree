import os
import importlib
import cudatext as app
from cudatext import ed

MAX_SECTIONS = 5

class Command:
    helpers = {}

    def __init__(self):
        self.h_tree = app.app_proc(app.PROC_GET_CODETREE, '')

        dir = app.app_path(app.APP_DIR_PY)
        dirs = os.listdir(dir)
        dirs = [os.path.join(dir, s) for s in dirs if s.startswith('cuda_tree_')]
        for dir in dirs:
            fn_inf = os.path.join(dir, 'install.inf')
            s_module = app.ini_read(fn_inf, 'info', 'subdir', '')
            for index in range(1, MAX_SECTIONS+1):
                section = 'treehelper'+str(index)
                s_method = app.ini_read(fn_inf, section, 'method', '')
                if not s_method: continue
                s_lexers = app.ini_read(fn_inf, section, 'lexers', '')
                if not s_lexers: continue
                for s_lex in s_lexers.split(','):
                    self.helpers[s_lex] = {
                        'module': s_module,
                        'method': s_method,
                        }
                #print('module', s_module, 'lexers', s_lexers, 'method', s_method)

        items = sorted(list(self.helpers.keys()))
        if items:
            print('TreeHelpers: ' + ', '.join(items))


    def get_getter(self, lexer):

        d = self.helpers.get(lexer)
        if not d: return

        getter = d.get('getter')
        if getter: return getter

        module = d['module']
        method = d['method']
        _m = importlib.import_module(module)
        getter = getattr(_m, method)

        d['getter'] = getter
        #print('helpers', self.helpers)
        return getter


    def update_tree(self, lexer):
        getter = self.get_getter(lexer)
        if not getter: return

        filename = ed.get_filename()
        lines = ed.get_text_all().split("\n")
        heads = list(getter(filename, lines))

        ed.set_prop(app.PROP_CODETREE, False)
        app.tree_proc(self.h_tree, app.TREE_LOCK)
        app.tree_proc(self.h_tree, app.TREE_ITEM_DELETE, 0)
        last_levels = {0: 0}
        for index, data in enumerate(heads):
            pos = data[0]
            level = data[1]
            header = data[2]
            icon_index = data[3] if len(data)>3 else -1

            for test_level in reversed(range(level)):
                parent = last_levels.get(test_level)
                if parent is None:
                    continue
                identity = app.tree_proc(self.h_tree, app.TREE_ITEM_ADD, parent, index=-1, text=header, image_index=icon_index)
                # when adding level K, forget all levels > K
                last_levels = {k: v for k, v in last_levels.items() if k <= level}
                last_levels[level] = identity

                if type(pos)==int:
                    if index == len(heads) - 1:
                        end_y = len(lines) - 1
                        end_x = len(ed.get_text_line(end_y))
                    else:
                        end_y = heads[index + 1][0]  # line_index of next header
                        end_x = 0
                    rng = (0, pos, end_x, end_y)
                else:
                    rng = pos

                app.tree_proc(self.h_tree, app.TREE_ITEM_SET_RANGE, identity, index=-1, text=rng)
                break

        app.tree_proc(self.h_tree, app.TREE_UNLOCK)

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

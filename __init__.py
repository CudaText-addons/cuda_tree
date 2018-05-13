import cudatext as cu

class HelperC:
    def get_headers(self, lines):
        return [(1, 1, 'root-c'), (5, 2, 'n1'), (8, 2, 'n2')]

class HelperCS:
    def get_headers(self, lines):
        return [(1, 1, 'root-c#'), (5, 2, 'n1'), (8, 2, 'n2')]


class Command:
    helpers = {
        'C': HelperC, 
        'C#': HelperCS,
        }

    def __init__(self):
        self.h_tree = cu.app_proc(cu.PROC_GET_CODETREE, '')

    def update_tree(self, lexer):
        helper_c = self.helpers.get(lexer)
        if not helper_c: return
        helper = helper_c()
        
        lines = cu.ed.get_text_all().split("\n")
        heads = list(helper.get_headers(lines))
        
        cu.ed.set_prop(cu.PROP_CODETREE, False)
        cu.tree_proc(self.h_tree, cu.TREE_ITEM_DELETE, 0)
        last_levels = {0: 0}
        for index, (line_number, level, header) in enumerate(heads):
            for test_level in reversed(range(level)):
                parent = last_levels.get(test_level)
                if parent is None:
                    continue
                identity = cu.tree_proc(self.h_tree, cu.TREE_ITEM_ADD, parent, index=-1, text=header)
                # when adding level K, forget all levels > K
                last_levels = {k: v for k, v in last_levels.items() if k <= level}
                last_levels[level] = identity
                if index == len(heads) - 1:
                    end_y = len(lines) - 1
                    end_x = len(cu.ed.get_text_line(end_y))
                else:
                    end_y = heads[index + 1][0]  # line_index of next header
                    end_x = 0
                rng = (0, line_number, end_x, end_y)
                cu.tree_proc(self.h_tree, cu.TREE_ITEM_SET_RANGE, identity, index=-1, text=rng)
                break

    def check_and_update(self, ed_self):
        lexer = ed_self.get_prop(cu.PROP_LEXER_FILE)
        if lexer and (lexer in self.helpers):
            self.update_tree(lexer)

    def on_change_slow(self, ed_self):
        self.check_and_update(ed_self)
    
    def on_open(self, ed_self):
        self.check_and_update(ed_self)

    def on_tab_change(self, ed_self):
        self.check_and_update(ed_self)

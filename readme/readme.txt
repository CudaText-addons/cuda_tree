plugin for CudaText.
micro framework to build Code Tree for additional lexers (which cannot build Code Tree by themselves). lexers are supported via sub-plugins, called TreeHelpers. each TreeHelper is a CudaText plugin:

1) install.inf: 
  section [info]:
    - key "subdir" begins with "cuda_tree_"
  section(s) [treehelper1] ... [treehelper5]:
    - key "lexers" is comma-separated lexers list
    - key "method" is name of getter method in __init__.py
    - key "fold" (0/1): also make folding from helper data 
    
2) __init__.py: contains getter method(s), referenced by install.inf.

  getter has signature (with any name):
  def get_headers(filename, lines)
  - param "lines" is editor contents in CudaText
  - param "filename" is to support included files or something

  getter must return list of tuples: 
  (line_index, level, caption, icon)
  - field "line_index": 0-based index of editor line, which has tree node.
  - field "level": 1-based level of node. 
    node of level K+1 is nested into (nearest upper) node of level K.
  - field "caption": caption of node.
  - field "icon": 0-based index of image-list icon, or -1 if icon not used.
        0: folder
        1: parts1
        2: parts2
        3: parts3
        4: box
        5: func
        6: arrow1
        7: arrow2

see examples of TreeHelpers: for Markdown, for MediaWiki.
they are add-ons in the CudaText AddonManager.

authors:
  Alexey T. (CudaText)
  some help by Nikita Melentev (@pohmelie at github)
license: MIT

plugin for CudaText.
micro framework to build Code Tree for additional lexers (which cannot build Code Tree by themselves). lexers are supported via sub-plugins, called TreeHelpers. each TreeHelper is a CudaText plugin with properties:

- install.inf has only section [info]
- install.inf has "subdir" beginning with "cuda_tree_"
- __init__.py contains dict "helper", with 1 or more keys, {'lexername': get_headers}. key name is supported lexer name, key value is getter function. 
  - function has signature (with any name): def get_headers(filename, lines)
  - param "lines" is editor contents in CudaText
  - param "filename" is to support included files or something
- function must return list of tuples: 
  (line_index, header_level, header_text, icon_index)
  - field "line_index": 0-based index of editor line, which has tree node
  - field "header_level": 1-based level of node (node of level K+1 is included in node of level K)
  - field "header_text": caption of tree node
  - field "icon_index": 0-based index of imagelist icon: -1: icon not used; 0: folder; 1: parts1; 2: parts2; 3: parts3; 4: box; 5: func; 6: arrow1; 7: arrow2

see examples of TreeHelpers: for Markdown, for MediaWiki. they are add-ons in the CudaText AddonManager.

authors:
  Alexey T. (CudaText)
  with help of Nikita Melentev (@pohmelie at github)
license: MIT

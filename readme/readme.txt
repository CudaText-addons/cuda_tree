plugin for CudaText.
micro framework to build Code Tree for additional lexers (which cannot build Code Tree by themselves).  lexers must be supported via sub-plugins, called TreeHelpers. each TreeHelper is a CudaText plugin with such properties:

- install.inf has "subdir" beginning with "cuda_tree_"
- install.inf has only section [info]
- __init__.py contains dict "helper", which has 1 or more keys. key name is supported lexer name, key value is getter function. function has such signature (with any name): def get_headers(filename, lines)
- getter function must return list of 3-tuples: (line_index, header_level_from_1, header_text) for given filename, with given lines. param "filename" is to support included files or something.

see examples of TreeHelpers: for Markdown, for MediaWiki. they are add-ons in the CudaText AddonManager.

authors:
  Alexey T. (CudaText)
  with help of Nikita Melentev (@pohmelie at github)
license: MIT

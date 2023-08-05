
from docutils.nodes import literal_block, paragraph, container

from sphinx.directives.code import CodeBlock

from bu.execute import ExecutionQueue
from bu.parsing import Parser

def process_bu_nodes(app, doctree, fromdocname):
    parser = Parser()
    for node in doctree.traverse(literal_block):
        if node.attributes.get('language') == 'bu':
            outputs = []
            try:
                script = parser.parse_string(node.children[0].astext())
                target = node.attributes.get('target', script.children[0].name)
                queue = ExecutionQueue(script, target)
            except Exception, e:
                outputs.append('Error: %s' % e)
                queue = []
            for execnode in queue:
                try:
                    output, code = execnode()
                    outputs.append(output)
                except Exception, e:
                    outputs.append('Error: %s' % e)
            all_output = '\n'.join(outputs)
            para = container()
            para += paragraph('output:', 'output:', classes=['output-caption'])
            block = literal_block(all_output, all_output)
            block.attributes['language'] = 'text'
            block.attributes['linenos'] = True
            para += block
            node.replace_self([node, para])

def setup(app):
    app.connect('doctree-resolved', process_bu_nodes)


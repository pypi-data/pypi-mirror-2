import docutils
import sphinx.util.compat

def setup(app):
    app.add_node(supplement,
                 html=(visit_supplement_node, depart_supplement_node),
                 latex=(visit_supplement_node, depart_supplement_node),
                 text=(visit_supplement_node, depart_supplement_node))
    app.add_directive('supplement', SupplementDirective)

class supplement(docutils.nodes.Admonition, docutils.nodes.Element):
    pass

def visit_supplement_node(self, node):
    self.visit_admonition(node)

def depart_supplement_node(self, node):
    self.depart_admonition(node)

class SupplementDirective(sphinx.util.compat.Directive):
    has_content = True
    optional_arguments = 1
    final_argument_whitespace = True
    def run(self):
        text = 'Supplement'
        if len(self.arguments) > 0:
            text = "For %s" % self.arguments[0]
        return sphinx.util.compat.make_admonition(supplement, self.name, [text], self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)


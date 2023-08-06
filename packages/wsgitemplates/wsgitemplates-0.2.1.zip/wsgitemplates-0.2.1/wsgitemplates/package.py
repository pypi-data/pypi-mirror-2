from paste.script import templates
import os

class Package(templates.Template):
    summary = "A simple package with a buildout"
    _template_dir = "templates/package"

    
    use_cheetah = True
    
    def run(self, command, output_dir, vars):
        templates.Template.run(self, command, output_dir, vars)

    vars = []
    
    def pre(self, command, output_dir, vars):
        vars['segs'] = vars['egg'].split('.')
        namespace =[]
        
        for i in range(len(vars['segs'])-1):
            namespace.append(".".join(vars['segs'][0:i+1]))
        
        vars['namespace'] = namespace
        
        super(Package, self).pre(command, output_dir, vars)
    
    def post(self, command, output_dir, vars):
        cwd = os.getcwd()
        os.chdir(vars['egg'])
        os.mkdir('src')
        os.chdir('src')
        for i in range(len(vars['segs'])):
            segs = vars['segs'][0:i+1]
            try:
                os.mkdir(os.path.join(*vars['segs'][0:i+1]))
            except OSError:
                pass
            segs.append("__init__.py")
            init = open(os.path.join(*segs), "w")
            if i == len(vars['segs'])-1:
                segs[-1] = "README.txt"
                open(os.path.join(*segs), "w").close()
            else:
                init.write("__import__('pkg_resources').declare_namespace(__name__)")
            init.close()
        os.chdir(cwd)
        super(Package, self).post(command, output_dir, vars)
from  xml.dom.minidom import parse

class PackageXML:
    def __init__(self, fn):
        self.tree = parse(fn)
        self.root = self.tree.childNodes[0]

    def get_packages(self, build=True):
        if build:
            key = 'build_depend'
        else:
            key = 'run_depend'

        pkgs = []
        for el in self.root.getElementsByTagName(key):
            pkgs.append( str(el.childNodes[0].nodeValue) )
        return pkgs

    def insert_new_elements(self, name, values, i):
        x = []
        for pkg in values:
            x.append(self.tree.createTextNode('\n  '))
            node = self.tree.createElement(name)
            node.appendChild(self.tree.createTextNode(pkg))
            x.append(node)

        self.root.childNodes = self.root.childNodes[:i-1] + x  + self.root.childNodes[i-1:]

    def add_packages(self, pkgs, build=True):
        state = 0
        i = 0
        while i < len(self.root.childNodes):
            child = self.root.childNodes[i]
            if child.nodeType==child.TEXT_NODE:
                i += 1
                continue

            name = str(child.nodeName)
            if name == 'build_depend':
                state = 1
            elif name == 'run_depend':
                if state == 1 and build:
                    self.insert_new_elements('build_depend', pkgs, i)
                    i += len(pkgs)*2
                state = 2
            elif state == 2:
                if not build:
                    self.insert_new_elements('run_depend', pkgs, i)
                    i += len(pkgs)*2
                state = 3
            i += 1

    def output(self, new_fn):
        f = open(new_fn, 'w')
        s = self.tree.toxml()
        s = s.replace('?><package>', '?>\n<package>')
        f.write(s)
        f.close()
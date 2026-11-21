from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'relatorio_metabolico': self.relatorio_metabolico
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')

    def relatorio_metabolico(self):
        return template('app/views/html/relatorio_metabolico')
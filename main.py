from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from webview import WebView
from os import listdir
from textwrap import fill

class BrowserApp(App):
    def build(self):
        self._create_local_file()
        self.browser = None
        b1 = Button(text='Tap for Google.\nBack button/gesture to return.',
                    on_press=self.view_google)
        b2 = Button(text='Tap for local file.\nBack button/gesture to return.',
                    on_press=self.view_local_file)
        b3 = Button(text='List downloads',
                    on_press=self.view_downloads)
        self.label = Label(text='')
        box = BoxLayout(orientation='vertical')
        box.add_widget(b1)
        box.add_widget(b2)
        box.add_widget(b3)
        box.add_widget(self.label)
        return box
        
    def view_google(self,b):
        self.browser = WebView('https://www.google.com',
                               enable_javascript = True,
                               enable_downloads = True,
                               enable_zoom = True)
        
    def view_local_file(self,b):
        self.browser = WebView('file://'+self.filename)

    def view_downloads(self,b):
        if self.browser:
            d = self.browser.downloads_directory()
            self.label.text = fill(d,40) + '\n'
            l = listdir(d)
            if l:
                for f in l:
                    self.label.text += f + '\n'
            else:
                self.label.text = 'No files downloaded'
        else:
            self.label.text = 'Open a browser first'
                
    def on_pause(self): 
        if self.browser:
            self.browser.pause()
        return True

    def on_resume(self):
        if self.browser:
            self.browser.resume()
        pass

    def _create_local_file(self):
        # Create a file for testing
        from android.storage import app_storage_path
        from jnius import autoclass
        from os.path import join, exists
        from os import mkdir
        
        Environment = autoclass('android.os.Environment')
        path = join(app_storage_path(), Environment.DIRECTORY_DOCUMENTS)
        if not exists(path):
            mkdir(path)
        self.filename = join(path,'from_space.html')
        with open(self.filename, "w") as f:
            f.write("<html>\n")
            f.write(" <head>\n")
            f.write(" </head>\n")
            f.write(" <body>\n")
            f.write("  <h1>Greetings Earthlings<h1>\n")
            f.write(" </body>\n")
            f.write("</html>\n")

BrowserApp().run()




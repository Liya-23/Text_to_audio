import tornado.web
import tornado.ioloop
from gtts import gTTS
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self): 
        self.render("web/index.html")

    def post(self):
        text = self.get_argument("text")
        file_name = self.get_argument("file_name")
        output_directory = "web/audios"  # Use forward slashes for directory path

        if not text or not file_name:
            self.set_status(400)
            self.write("Both text and file_name are required.")
            return

        language = 'en'
        text_to_speech = gTTS(text=text, lang=language)

        # Ensure the file name ends with ".mp3"
        if not file_name.endswith(".mp3"):
            file_name += ".mp3"

        try:
            # Combine the output_directory and file_name to create the full path
            full_path = os.path.join(output_directory, file_name)
            text_to_speech.save(full_path)
            self.write(f"Text saved as {file_name} in {output_directory}")
        except Exception as e:
            self.set_status(500)
            self.write(f"An error occurred: {str(e)}")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/web/static/(.*)", tornado.web.StaticFileHandler, {"path": "web/static"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(4567)
    print("Listening on port 4567")
    tornado.ioloop.IOLoop.current().start()

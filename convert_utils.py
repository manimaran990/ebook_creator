import os

class converter:
    def __init__(self, book_title_in_english, book_title, author, content,cover):
        self.book_title_in_english = book_title_in_english
        self.book_title = book_title
        self.author = author
        self.content = content
        self.cover = cover
        
    def convert_to_epub(self):
        print("Converting to epub")
        print("book title: "+self.book_title_in_english)
        epub_command = "ebook-convert "+ self.content +" ./files/"+ self.book_title_in_english + ".epub" + \
                " --pretty-print   --level1-toc //h:h1  --level2-toc //h:h2  " + \
                " --authors '" + self.author +  "' --language Tamil --publisher FreeTamilEbooks.com " + \
                " --title '" + self.book_title +"' >  epub.log 2>&1"

        os.system(epub_command)
        print("Done.")
    
    def convert_to_mobi(self):
        print("Converting to mobi")
        mobi_command = "ebook-convert " + self.content + " ./files/" + self.book_title_in_english + ".mobi " + \
                " --pretty-print   --level1-toc //h:h1  --level2-toc //h:h2  " + \
                " --authors '" + self.author +  "' --language Tamil --publisher FreeTamilEbooks.com " + \
                " --title '" + self.book_title +"' >  epub.log 2>&1"
        os.system(mobi_command)
        print("Done.")
        print("Convertion Completed. Check the Books now")
        
        
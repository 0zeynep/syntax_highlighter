import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class Lexer:
    def __init__(self):
        self.keywords = {"if", "else", "while", "for", "return","switch","case","do","int","float","string","double","long","short"}
        self.operators = {"+", "-", "*", "/", "=", "<", ">", "!", "&", "|"}
        self.preprocessor = {"include", "define"}  
    def tokenize(self, text):
        tokens = []
        i = 0
        n = len(text)

        while i < n:
            # Yorumlar (// veya /* */)
            if i + 1 < n and text[i] == "/" and text[i + 1] == "/":
                end = text.find("\n", i)
                if end == -1:
                    end = n
                tokens.append(("COMMENT", i, end))
                i = end
            
            elif i + 1 < n and text[i] == "/" and text[i + 1] == "*":
                start = i
                end = text.find("*/", i)
                if end == -1:
                    end = n
                else:
                    end += 2 
                tokens.append(("COMMENT", start, end))
                i = end
             # Preprocessor direktifleri (#include, #define)
            elif text[i] == "#":
                start = i
                i += 1
               
                while i < n and text[i].isspace():
                    i += 1
                
                directive_start = i
                while i < n and text[i].isalpha():
                    i += 1
                directive = text[directive_start:i]
                
                if directive in self.preprocessor:
                   
                    end = text.find("\n", i)
                    if end == -1:
                        end = n
                    tokens.append(("PREPROCESSOR", start, end))
                    i = end
           
            # Sayılar
            elif text[i].isdigit():
                start = i
                while i < n and text[i].isdigit():
                    i += 1
                tokens.append(("NUMBER", start, i))
            #Stringler
            elif text[i] == '"' or text[i] == "'":
                    quote_char = text[i]
                    start = i
                    i += 1
                    while i < n and text[i] != quote_char:
                        if text[i] == "\\" and i + 1 < n: 
                            i += 2
                        else:
                            i += 1
                    i += 1  
                    tokens.append(("STRING", start, i))

            # Operatörler
            elif text[i] in self.operators:
                start = i
                while i < n and text[i] in self.operators:
                    i += 1
                tokens.append(("OPERATOR", start, i))

            # Anahtar kelimeler veya değişken isimleri
            elif text[i].isalpha() or text[i] == "_":
                start = i
                while i < n and (text[i].isalnum() or text[i] == "_"):
                    i += 1
                word = text[start:i]
                if word in self.keywords:
                    tokens.append(("KEYWORD", start, i))
                else:
                    tokens.append(("VARIABLE", start, i))

            else:
                i += 1
            

        return tokens

class SyntaxHighlighterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighter")

        # Metin alanı
        self.text_area = ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Token renkleri
        self.token_colors = {
            "KEYWORD": "green",
            "VARIABLE": "blue",
            "NUMBER": "red",
            "STRING": "red",
            "OPERATOR": "orange",
            "COMMENT": "gray",
            "PREPROCESSOR": "purple"
        }

        # Tag'leri başta tanımla
        for token_type, color in self.token_colors.items():
            self.text_area.tag_config(token_type, foreground=color)

        # Lexer
        self.lexer = Lexer()

        # Gerçek zamanlı vurgulama
        self.text_area.bind("<KeyRelease>", self.update_highlighting)

    def update_highlighting(self, event=None):
        text = self.text_area.get("1.0", tk.END)
        
        # Eski tag'leri temizle
        for tag in self.token_colors:
            self.text_area.tag_remove(tag, "1.0", tk.END)

        tokens = self.lexer.tokenize(text)

        # Vurgulama uygula
        for token_type, start, end in tokens:
            self.text_area.tag_add(
                token_type,
                f"1.0+{start}c",
                f"1.0+{end}c"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighterApp(root)
    root.mainloop()

from tkinter import *
import customtkinter as ctk
import json
from deep_translator import GoogleTranslator


#OBSERVAÇÃO: []->VETOR, ()->TUPLA, {} -> DICIONÁRIO

class Main_Menu():
    def __init__(self) -> None:
        print("Janela Main Menu Iniciada")

        self.dict_lista_de_languages={
            'Escolha um idioma':'',
            'arabic': 'ar', 
            'catalan': 'ca', 
            'chinese (simplified)': 'zh-CN', 
            'chinese (traditional)': 'zh-TW', 
            'croatian': 'hr', 
            'english': 'en', 
            'filipino': 'tl', 
            'french': 'fr', 
            'german': 'de', 
            'guarani': 'gn', 
            'hebrew': 'iw', 
            'indonesian': 'id', 
            'italian': 'it', 
            'japanese': 'ja', 
            'korean': 'ko', 
            'latin': 'la', 
            'polish': 'pl', 
            'portuguese': 'pt', 
            'romanian': 'ro', 
            'russian': 'ru', 
            'scots gaelic': 'gd', 
            'serbian': 'sr', 
            'slovak': 'sk', 
            'slovenian': 'sl',
            'spanish': 'es', 
            'swedish': 'sv', 
            'thai': 'th', 
            'turkish': 'tr', 
            'ukrainian': 'uk'}
        
        self.lista_de_languages_origens = []
        self.lista_de_languages_destinos = []
        self.idiomaIN = ""
        self.idiomaOUT = ""
        
        for idioma in self.dict_lista_de_languages:
            print(idioma)
            self.lista_de_languages_origens.append(idioma)
            self.lista_de_languages_destinos.append(idioma)
        
        # DEFININDO APARÊNCIA
        with open(file="settings/appearance/default.json",mode="r") as file:
            arquivoAparencia = file.read()
            dic_lista_de_aparencia=json.loads(arquivoAparencia)
        
        # DEFININDO TEMA PADRÃO
        with open(file="settings/themes/default.json",mode="r") as file:
            arquivoTema = file.read()
            dic_lista_de_temas=json.loads(arquivoTema)
        
        self.lista_de_aparencia = [] # LISTA DE APARÊNCIAS
        self.lista_de_temas = [] # LISTA DE TEMAS

        for aparencia in dic_lista_de_aparencia:
            #print(aparencia)
            self.lista_de_aparencia.append(aparencia)
        
        for tema in dic_lista_de_temas:
            #print(tema)
            self.lista_de_temas.append(tema)
        
       
        self.MainWindow()
        
        pass

    def Escolha_a_aparencia(self,cor):
        ctk.set_appearance_mode(cor)

    def Escolha_o_tema(self,cor):
        ctk.set_default_color_theme(cor)

    def Escolha_idioma_origem(self,idiomaIN):
        self.idiomaIN = idiomaIN
        print(self.idiomaIN)  
        

    def Escolha_idioma_destino(self,idiomaOUT):
        self.idiomaOUT = idiomaOUT
        print(self.idiomaOUT)
        
    def Sair(self,janela):
        janela.close()

    def Traduzir_idioma(self):
        try:
            self.texto = str(self.txt_texto.get(1.0,"end-1c"))
            tradutor = GoogleTranslator(source=f"{self.idiomaIN}", target=f"{self.idiomaOUT}")
            traducao = tradutor.translate(text=self.texto)
            self.txt_texto.delete("1.0", "end") 
            self.txt_texto.insert("end-1c",traducao)
        except:
            windows_msn = ctk.CTk()
            windows_msn.title("Informativo")
            windows_msn.geometry("400x100")
            lbl_msn = ctk.CTkLabel(windows_msn,width=400,height=100,font=ctk.CTkFont(family="Comic_Sans_MS_Bold",size=24,weight="bold"),fg_color="#f4f4f4", bg_color="#131313", text="Por favor, informe um idioma")
            lbl_msn.pack()
            windows_msn.after(2000,windows_msn.destroy)
            print("Por favor, informe um idioma")
        pass

    def MainWindow(self):
        # COMEÇANDO A JANELA PRINCIPAL
        self.janela = ctk.CTk()
        self.janela.title("Maia Translator")
        self.janela.geometry("800x550")
        # DESCREVE O TITULO 
        lblTitulo = ctk.CTkLabel(self.janela,text="Maia Translator", font=("Arial",24))
        lblTitulo.place(relwidth=1, rely=0.02)
        # DESCREVE LIGUAGEM DE ORIGEM
        lbl_lang_origem = ctk.CTkLabel(self.janela,text="Origem", font=("Arial",16))
        lbl_lang_origem.place(relx=0.15, rely=0.1, anchor=N)
        cmb_lang_origem = ctk.CTkComboBox(self.janela,width=200,dropdown_font=("Arial",18), font=("Arial",18), values=self.lista_de_languages_origens, command=self.Escolha_idioma_origem)
        cmb_lang_origem.place(relx=0.15, rely=0.15, anchor=N)
         # DESCREVE LIGUAGEM DE DESTINO
        lbl_lang_dest = ctk.CTkLabel(self.janela,text="Destino", font=("Arial",16))
        lbl_lang_dest.place(relx=0.85, rely=0.1, anchor=N)
        cmb_lang_dest= ctk.CTkComboBox(self.janela,width=200,dropdown_font=("Arial",18), font=("Arial",18), values=self.lista_de_languages_destinos, command=self.Escolha_idioma_destino)
        cmb_lang_dest.place(relx=0.85, rely=0.15, anchor=N)
        # CAIXA DE TEXTO PARA ESCREVER E TRADUZIR
        self.txt_texto = ctk.CTkTextbox(self.janela, width=780, height=300, font=("Arial",18))
        self.txt_texto.place(relwidth=0.92,relheight=0.5,relx=0.04, rely=0.25)
        # BOTÃO DE TRADUZIR
        btn_traduzir = ctk.CTkButton(self.janela,text="TRADUZIR", font=("Arial",20), width=300, height=80, command=self.Traduzir_idioma)
        btn_traduzir.place(relwidth=0.5, relx=0.25, rely=0.82)
                
        self.janela.mainloop()


#ctk.set_appearance_mode("system") # default(system), dark, light
#ctk.set_default_color_theme("blue") # default(blue), green, dark-blue
#{'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
      
import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator

def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para desenvolvimento e PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MainMenu:
    def __init__(self) -> None:
        print("Janela Main Menu Iniciada")
        
        # Configuração inicial de aparência do CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Carrega mapa de idiomas do GoogleTranslator
        self._carregar_idiomas()
        
        # Constrói a interface gráfica
        self.main_window()

    def _carregar_idiomas(self):
        """Carrega e formata os idiomas suportados pelo deep-translator."""
        try:
            # Obtém dicionário original {'afrikaans': 'af', ...}
            raw_langs = GoogleTranslator().get_supported_languages(as_dict=True)
        except Exception:
            # Fallback básico caso haja falha de conexão na inicialização
            raw_langs = {
                'portuguese': 'pt', 'english': 'en', 'spanish': 'es',
                'french': 'fr', 'german': 'de', 'italian': 'it',
                'japanese': 'ja', 'korean': 'ko', 'chinese (simplified)': 'zh-CN'
            }
            
        self.mapa_idiomas = {}
        for nome, codigo in raw_langs.items():
            nome_formatado = nome.title()
            self.mapa_idiomas[nome_formatado] = codigo
            
        # Lista ordenada de nomes para as Comboboxes
        self.lista_nomes_destino = sorted(list(self.mapa_idiomas.keys()))
        self.lista_nomes_origem = ["Detectar idioma"] + self.lista_nomes_destino

    def alterar_tema(self):
        """Alterna entre os modos Dark e Light."""
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def inverter_idiomas(self):
        """Inverte os idiomas de origem e destino se aplicável."""
        origem_atual = self.cmb_origem.get()
        destino_atual = self.cmb_destino.get()
        
        if origem_atual == "Detectar idioma":
            self.exibir_mensagem("Aviso", "Não é possível inverter quando a origem é 'Detectar idioma'.")
            return
            
        self.cmb_origem.set(destino_atual)
        self.cmb_destino.set(origem_atual)
        
        # Inverte também os textos das caixas se houver tradução
        texto_origem = self.txt_origem.get("1.0", "end-1c")
        texto_destino = self.txt_destino.get("1.0", "end-1c")
        
        if texto_destino.strip():
            self.txt_origem.delete("1.0", "end")
            self.txt_origem.insert("1.0", texto_destino)
            self._atualizar_contador()
            self.traduzir_idioma()

    def limpar_texto(self):
        """Limpa a caixa de texto de entrada e de saída."""
        self.txt_origem.delete("1.0", "end")
        self.txt_destino.configure(state="normal")
        self.txt_destino.delete("1.0", "end")
        self.txt_destino.configure(state="disabled")
        self._atualizar_contador()

    def copiar_traducao(self):
        """Copia a tradução gerada para a área de transferência."""
        texto = self.txt_destino.get("1.0", "end-1c").strip()
        if texto:
            self.janela.clipboard_clear()
            self.janela.clipboard_append(texto)
            self.btn_copiar.configure(text="Copiado! ✓")
            self.janela.after(2000, lambda: self.btn_copiar.configure(text="📋 Copiar"))
        else:
            self.exibir_mensagem("Aviso", "Nenhum texto traduzido para copiar.")

    def _atualizar_contador(self, event=None):
        """Atualiza a contagem de caracteres da caixa de entrada."""
        qtd = len(self.txt_origem.get("1.0", "end-1c"))
        self.lbl_contador.configure(text=f"{qtd} caracteres")

    def traduzir_idioma(self):
        """Realiza a tradução utilizando deep_translator."""
        texto_origem = self.txt_origem.get("1.0", "end-1c").strip()
        if not texto_origem:
            self.exibir_mensagem("Aviso", "Por favor, digite um texto para traduzir.")
            return

        nome_origem = self.cmb_origem.get()
        nome_destino = self.cmb_destino.get()

        code_origem = "auto" if nome_origem == "Detectar idioma" else self.mapa_idiomas.get(nome_origem, "auto")
        code_destino = self.mapa_idiomas.get(nome_destino, "en")

        # Atualiza estado do botão para feedback visual
        self.btn_traduzir.configure(state="disabled", text="Traduzindo...")
        self.janela.update_idletasks()

        try:
            tradutor = GoogleTranslator(source=code_origem, target=code_destino)
            traducao = tradutor.translate(text=texto_origem)

            self.txt_destino.configure(state="normal")
            self.txt_destino.delete("1.0", "end")
            self.txt_destino.insert("1.0", traducao)
            self.txt_destino.configure(state="disabled")
        except Exception as e:
            self.exibir_mensagem("Erro de Tradução", f"Falha ao traduzir: {str(e)}")
        finally:
            self.btn_traduzir.configure(state="normal", text="TRADUZIR ➔")

    def exibir_mensagem(self, titulo: str, mensagem: str):
        """Exibe uma janela popup estilizada usando CTkToplevel."""
        popup = ctk.CTkToplevel(self.janela)
        popup.title(titulo)
        popup.geometry("380x160")
        popup.resizable(False, False)
        popup.transient(self.janela)  # Mantém no topo da janela principal
        popup.grab_set()             # Modal

        ico_path = resource_path("icones/maia_tradutor.ico")
        if os.path.exists(ico_path):
            try:
                popup.iconbitmap(ico_path)
            except Exception:
                pass
        elif hasattr(self, 'favicon') and self.favicon:
            try:
                popup.iconphoto(False, self.favicon)
            except Exception:
                pass

        lbl_title = ctk.CTkLabel(popup, text=titulo, font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=(15, 5))

        lbl_msg = ctk.CTkLabel(popup, text=mensagem, font=ctk.CTkFont(size=14), wraplength=340)
        lbl_msg.pack(pady=10)

        btn_ok = ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy)
        btn_ok.pack(pady=(5, 15))

    def main_window(self):
        """Inicializa e organiza os elementos da janela principal."""
        self.janela = ctk.CTk()
        self.janela.title("Maia Translator")
        self.janela.geometry("940x620")
        self.janela.minsize(850, 550)

        # Ícone da janela (Favicon)
        ico_path = resource_path("icones/maia_tradutor.ico")
        png_path = resource_path("icones/maia_tradutor_16x16.png")
        
        if os.path.exists(ico_path):
            try:
                self.janela.iconbitmap(ico_path)
            except Exception as e:
                print(f"Erro ao carregar iconbitmap: {e}")
        elif os.path.exists(png_path):
            try:
                pil_img = Image.open(png_path)
                self.favicon = ImageTk.PhotoImage(pil_img)
                self.janela.iconphoto(True, self.favicon)
            except Exception as e:
                print(f"Erro ao carregar favicon PNG: {e}")

        # --- CABEÇALHO ---
        frame_header = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame_header.pack(fill="x", pady=(15, 10))

        # Título e Subtítulo (Agrupados à esquerda)
        frame_title = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_title.pack(side="left", padx=20)

        lbl_titulo = ctk.CTkLabel(
            frame_title, text="Maia Translator",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        )
        lbl_titulo.pack(anchor="w")

        lbl_subtitulo = ctk.CTkLabel(
            frame_title, text="Tradução rápida e inteligente",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="gray"
        )
        lbl_subtitulo.pack(anchor="w")

        # Switch de Tema (À direita)
        self.switch_tema = ctk.CTkSwitch(
            frame_header, text="Modo Escuro", command=self.alterar_tema,
            font=ctk.CTkFont(size=13)
        )
        self.switch_tema.pack(side="right", padx=20)
        self.switch_tema.select()  # Padrão Dark

        # --- PAINEL PRINCIPAL (GRID DUPLO) ---
        frame_body = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame_body.pack(fill="both", expand=True, padx=20, pady=5)
        frame_body.grid_columnconfigure(0, weight=1)
        frame_body.grid_columnconfigure(1, weight=0)
        frame_body.grid_columnconfigure(2, weight=1)
        frame_body.grid_rowconfigure(0, weight=1)

        # --- CARTÃO ESQUERDO: ORIGEM ---
        card_origem = ctk.CTkFrame(frame_body, corner_radius=12)
        card_origem.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        header_origem = ctk.CTkFrame(card_origem, fg_color="transparent")
        header_origem.pack(fill="x", padx=12, pady=10)

        lbl_origem = ctk.CTkLabel(header_origem, text="De:", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_origem.pack(side="left", padx=(0, 5))

        self.cmb_origem = ctk.CTkComboBox(
            header_origem, values=self.lista_nomes_origem, width=180,
            font=ctk.CTkFont(size=13), dropdown_font=ctk.CTkFont(size=13)
        )
        self.cmb_origem.pack(side="left", fill="x", expand=True)
        self.cmb_origem.set("Detectar idioma")

        btn_limpar = ctk.CTkButton(
            header_origem, text="✕ Limpar", width=70, height=28,
            fg_color="transparent", hover_color=("#D1D5DB", "#374151"),
            text_color=("gray10", "gray90"), command=self.limpar_texto
        )
        btn_limpar.pack(side="right", padx=(5, 0))

        self.txt_origem = ctk.CTkTextbox(
            card_origem, font=ctk.CTkFont(size=15), corner_radius=8, wrap="word"
        )
        self.txt_origem.pack(fill="both", expand=True, padx=12, pady=(0, 5))
        self.txt_origem.bind("<KeyRelease>", self._atualizar_contador)

        footer_origem = ctk.CTkFrame(card_origem, fg_color="transparent")
        footer_origem.pack(fill="x", padx=12, pady=(0, 8))

        self.lbl_contador = ctk.CTkLabel(
            footer_origem, text="0 caracteres", font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.lbl_contador.pack(side="left")

        # --- COLUNA CENTRAL: SWAP ---
        frame_swap = ctk.CTkFrame(frame_body, fg_color="transparent")
        frame_swap.grid(row=0, column=1, sticky="ns", padx=2, pady=5)

        btn_swap = ctk.CTkButton(
            frame_swap, text="⇄", width=38, height=38, corner_radius=19,
            font=ctk.CTkFont(size=18, weight="bold"), command=self.inverter_idiomas
        )
        btn_swap.pack(expand=True)

        # --- CARTÃO DIREITO: DESTINO ---
        card_destino = ctk.CTkFrame(frame_body, corner_radius=12)
        card_destino.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        header_destino = ctk.CTkFrame(card_destino, fg_color="transparent")
        header_destino.pack(fill="x", padx=12, pady=10)

        lbl_destino = ctk.CTkLabel(header_destino, text="Para:", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_destino.pack(side="left", padx=(0, 5))

        self.cmb_destino = ctk.CTkComboBox(
            header_destino, values=self.lista_nomes_destino, width=180,
            font=ctk.CTkFont(size=13), dropdown_font=ctk.CTkFont(size=13)
        )
        self.cmb_destino.pack(side="left", fill="x", expand=True)
        # Seleciona Português se disponível, senão primeiro da lista
        if "Portuguese" in self.lista_nomes_destino:
            self.cmb_destino.set("Portuguese")
        elif self.lista_nomes_destino:
            self.cmb_destino.set(self.lista_nomes_destino[0])

        self.btn_copiar = ctk.CTkButton(
            header_destino, text="📋 Copiar", width=80, height=28,
            fg_color="transparent", hover_color=("#D1D5DB", "#374151"),
            text_color=("gray10", "gray90"), command=self.copiar_traducao
        )
        self.btn_copiar.pack(side="right", padx=(5, 0))

        self.txt_destino = ctk.CTkTextbox(
            card_destino, font=ctk.CTkFont(size=15), corner_radius=8, wrap="word"
        )
        self.txt_destino.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        self.txt_destino.configure(state="disabled")

        # --- BOTÃO DE AÇÃO PRINCIPAL ---
        frame_action = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame_action.pack(fill="x", padx=20, pady=(10, 20))

        self.btn_traduzir = ctk.CTkButton(
            frame_action, text="TRADUZIR ➔", font=ctk.CTkFont(size=16, weight="bold"),
            height=48, corner_radius=10, command=self.traduzir_idioma
        )
        self.btn_traduzir.pack(fill="x", padx=100)

        # Permite atalho Ctrl+Enter para traduzir
        self.janela.bind("<Control-Return>", lambda e: self.traduzir_idioma())

        self.janela.mainloop()

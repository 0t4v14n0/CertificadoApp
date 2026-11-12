import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pandas as pd
import webbrowser
import os
import re


class CertificadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Certificados")
        self.root.geometry("550x620")
        self.root.resizable(False, False)

        # Caminhos dos arquivos
        self.template_path = ""
        self.dados_path = ""
        self.assinatura_path = ""
        self.fonte_path = "arial.ttf"

        # Coordenadas reais e tamanhos
        self.nome_x = 500
        self.nome_y = 500
        self.ass_x = 800
        self.ass_y = 800
        self.tamanho_fonte = 60
        self.escala_ass = 1.0

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  INTERFACE PRINCIPAL                                               #
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        main = tb.Frame(self.root, padding=20)
        main.pack(fill=BOTH, expand=True)

        # ---------------- CABEÇALHO com link à direita ---------------- #
        header = tb.Frame(main)
        header.pack(fill=X, pady=(0, 4))

        tb.Label(
            header,
            text="Gerador de Certificados",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary",
        ).pack(side=LEFT)

        tb.Button(
            header,
            text="📖 Como usar?",
            bootstyle="link-info",
            cursor="hand2",
            command=lambda: webbrowser.open(
                "https://seuusuario.github.io/certificados-tutorial"
            ),
        ).pack(side=RIGHT)

        tb.Label(
            main,
            text="Automatize a criação de certificados em lote",
            bootstyle="secondary",
        ).pack(anchor=W, pady=(0, 20))

        # ---------------------- PASSO 1 ------------------------------- #
        step1 = tb.Labelframe(
            main, text="  📁  Passo 1 · Arquivos Base  ",
            padding=15, bootstyle="info",
        )
        step1.pack(fill=X, pady=8)

        self.lbl_template = tb.Label(
            step1, text="⚠ Nenhum template selecionado", bootstyle="danger"
        )
        self.lbl_template.pack(anchor=W)
        tb.Button(
            step1, text="Selecionar Template (Fundo)",
            command=self.selecionar_template,
            bootstyle="outline-info", width=40,
        ).pack(anchor=W, pady=4)

        self.lbl_assinatura = tb.Label(
            step1, text="⚠ Nenhuma assinatura selecionada (Opcional)",
            bootstyle="warning",
        )
        self.lbl_assinatura.pack(anchor=W)
        tb.Button(
            step1, text="Selecionar Assinatura (PNG)",
            command=self.selecionar_assinatura,
            bootstyle="outline-info", width=40,
        ).pack(anchor=W, pady=4)

        # ---------------------- PASSO 2 ------------------------------- #
        step2 = tb.Labelframe(
            main, text="  🛠  Passo 2 · Modelagem  ",
            padding=15, bootstyle="warning",
        )
        step2.pack(fill=X, pady=8)
        tb.Button(
            step2, text="Ajustar Posições, Fontes e Tamanho",
            command=self.abrir_modelador,
            bootstyle="warning", width=40,
        ).pack(anchor=W)

        # ---------------------- PASSO 3 ------------------------------- #
        step3 = tb.Labelframe(
            main, text="  📊  Passo 3 · Dados e Geração  ",
            padding=15, bootstyle="success",
        )
        step3.pack(fill=X, pady=8)

        self.lbl_dados = tb.Label(
            step3, text="⚠ Nenhuma planilha selecionada", bootstyle="danger"
        )
        self.lbl_dados.pack(anchor=W)
        tb.Button(
            step3, text="Selecionar Planilha (Nomes)",
            command=self.selecionar_dados,
            bootstyle="outline-success", width=40,
        ).pack(anchor=W, pady=4)

        # ---------------- PROGRESSO + STATUS ------------------------- #
        self.progress = tb.Progressbar(
            main, bootstyle="success-striped", length=400, mode="determinate"
        )
        self.progress.pack(pady=(25, 5))
        self.lbl_status = tb.Label(
            main, text="Pronto para começar", bootstyle="secondary"
        )
        self.lbl_status.pack()

        tb.Button(
            main, 
            text="GERAR CERTIFICADOS",
            command=self.gerar_certificados,
            bootstyle="success"
        ).pack(pady=10, ipadx=40, ipady=10)

    # ------------------------------------------------------------------ #
    #  HELPERS DE SELEÇÃO                                                #
    # ------------------------------------------------------------------ #
    def _mostrar_thumb(self, path, size=(180, 120)):
        try:
            img = Image.open(path)
            img.thumbnail(size)
            self._thumb_img = ImageTk.PhotoImage(img)
            if hasattr(self, "thumb_label") and self.thumb_label.winfo_exists():
                self.thumb_label.destroy()
            self.thumb_label = tb.Label(self.root, image=self._thumb_img)
            self.thumb_label.place(relx=0.95, rely=0.08, anchor=NE)
        except Exception:
            pass  # thumbnail é opcional; ignora se falhar

    def selecionar_template(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.template_path = path
            nome = os.path.basename(path)
            self.lbl_template.config(
                text=f"✓ Template: {nome}", bootstyle="success"
            )
            self._mostrar_thumb(path)

    def selecionar_assinatura(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens PNG", "*.png")]
        )
        if path:
            self.assinatura_path = path
            nome = os.path.basename(path)
            self.lbl_assinatura.config(
                text=f"✓ Assinatura: {nome}", bootstyle="success"
            )

    def selecionar_dados(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")]
        )
        if path:
            self.dados_path = path
            nome = os.path.basename(path)
            self.lbl_dados.config(
                text=f"✓ Base de Dados: {nome}", bootstyle="success"
            )

    # ------------------------------------------------------------------ #
    #  MODELADOR VISUAL                                                  #
    # ------------------------------------------------------------------ #
    def abrir_modelador(self):
        if not self.template_path:
            messagebox.showwarning(
                "Aviso", "Selecione o template no Passo 1 primeiro!"
            )
            return

        top = tb.Toplevel(self.root)
        top.title("Arraste e Personalize os Elementos")

        frame_controles = tb.Frame(top, padding=10)
        frame_controles.pack(fill=X)

        img_temp = Image.open(self.template_path)
        LARGURA_TELA = 900
        self.escala_tela = LARGURA_TELA / img_temp.width
        nova_altura = int(img_temp.height * self.escala_tela)

        img_temp_resized = img_temp.resize((LARGURA_TELA, nova_altura))
        self.tk_bg = ImageTk.PhotoImage(img_temp_resized)

        canvas = tb.Canvas(top, width=LARGURA_TELA, height=nova_altura)
        canvas.pack()
        canvas.create_image(0, 0, image=self.tk_bg, anchor="nw")

        self.drag_data = {"x": 0, "y": 0, "item": None}

        # -------- Renderizador Avançado do Nome -------- #
        self.tk_nome = None
        self.nome_id = canvas.create_image(
            self.nome_x * self.escala_tela,
            self.nome_y * self.escala_tela,
            anchor="nw", tags="draggable",
        )

        def atualizar_preview_nome():
            texto_exemplo = "NOME DO ALUNO DA SILVA"

            if self.dados_path:
                try:
                    df = (
                        pd.read_csv(self.dados_path)
                        if self.dados_path.endswith(".csv")
                        else pd.read_excel(self.dados_path)
                    )
                    if "Nome" in df.columns and len(df) > 0:
                        texto_exemplo = str(df.iloc[0]["Nome"])
                except Exception:
                    pass

            try:
                fonte_preview = ImageFont.truetype(
                    self.fonte_path,
                    max(1, int(self.tamanho_fonte * self.escala_tela)),
                )
            except Exception:
                fonte_preview = ImageFont.load_default()

            img_txt = Image.new(
                "RGBA",
                (int(3000 * self.escala_tela), int(400 * self.escala_tela)),
                (0, 0, 0, 0),
            )
            draw = ImageDraw.Draw(img_txt)
            draw.text((0, 0), texto_exemplo, font=fonte_preview, fill="black")

            bbox = img_txt.getbbox()
            if bbox:
                img_txt = img_txt.crop((0, 0, bbox[2], bbox[3]))

            self.tk_nome = ImageTk.PhotoImage(img_txt)
            canvas.itemconfig(self.nome_id, image=self.tk_nome)

        atualizar_preview_nome()

        # -------- Assinatura (se existir) -------- #
        if self.assinatura_path:
            self.img_ass_original = Image.open(
                self.assinatura_path
            ).convert("RGBA")
            largura_ass_tela = int(
                self.img_ass_original.width * self.escala_ass * self.escala_tela
            )
            altura_ass_tela = int(
                self.img_ass_original.height * self.escala_ass * self.escala_tela
            )
            img_ass_resized = self.img_ass_original.resize(
                (largura_ass_tela, altura_ass_tela)
            )
            self.tk_ass = ImageTk.PhotoImage(img_ass_resized)
            self.ass_id = canvas.create_image(
                self.ass_x * self.escala_tela,
                self.ass_y * self.escala_tela,
                image=self.tk_ass, anchor="nw", tags="draggable",
            )

        # -------- Controles -------- #
        def mudar_fonte():
            path = filedialog.askopenfilename(
                filetypes=[("Fontes", "*.ttf;*.otf")]
            )
            if path:
                self.fonte_path = path
                atualizar_preview_nome()

        def centralizar_nome():
            bbox = canvas.bbox(self.nome_id)
            if bbox:
                largura_texto = bbox[2] - bbox[0]
                novo_x = (LARGURA_TELA - largura_texto) / 2
                canvas.coords(
                    self.nome_id, novo_x, canvas.coords(self.nome_id)[1]
                )

        tb.Button(
            frame_controles, text="🔤 Mudar Fonte",
            command=mudar_fonte, bootstyle="info",
        ).pack(side="left", padx=5)

        tb.Button(
            frame_controles, text="↔ Centralizar Nome",
            command=centralizar_nome, bootstyle="info-outline",
        ).pack(side="left", padx=5)

        def atualizar_fonte(val):
            self.tamanho_fonte = int(float(val))
            atualizar_preview_nome()

        def atualizar_assinatura(val):
            if self.assinatura_path:
                self.escala_ass = int(float(val)) / 100.0
                nova_largura = max(
                    1,
                    int(
                        self.img_ass_original.width
                        * self.escala_ass
                        * self.escala_tela
                    ),
                )
                nova_altura = max(
                    1,
                    int(
                        self.img_ass_original.height
                        * self.escala_ass
                        * self.escala_tela
                    ),
                )
                img_ass_resized = self.img_ass_original.resize(
                    (nova_largura, nova_altura)
                )
                self.tk_ass = ImageTk.PhotoImage(img_ass_resized)
                canvas.itemconfig(self.ass_id, image=self.tk_ass)

        slider_fonte = tb.Scale(
            frame_controles, from_=20, to=400, command=atualizar_fonte
        )
        slider_fonte.set(self.tamanho_fonte)
        tb.Label(frame_controles, text="Tamanho Fonte").pack(
            side="left", padx=(15, 5)
        )
        slider_fonte.pack(side="left")

        slider_ass = tb.Scale(
            frame_controles, from_=10, to=300, command=atualizar_assinatura
        )
        slider_ass.set(int(self.escala_ass * 100))
        tb.Label(frame_controles, text="Escala Assinatura").pack(
            side="left", padx=(15, 5)
        )
        slider_ass.pack(side="left")

        # -------- Drag & Drop -------- #
        def on_click(event):
            item = canvas.find_withtag("current")
            if item:
                self.drag_data["item"] = item[0]
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y

        def on_drag(event):
            if self.drag_data["item"]:
                dx = event.x - self.drag_data["x"]
                dy = event.y - self.drag_data["y"]
                canvas.move(self.drag_data["item"], dx, dy)
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y

        def on_release(event):
            self.drag_data["item"] = None

        canvas.tag_bind("draggable", "<ButtonPress-1>", on_click)
        canvas.tag_bind("draggable", "<B1-Motion>", on_drag)
        canvas.tag_bind("draggable", "<ButtonRelease-1>", on_release)

        def salvar_posicoes():
            nx, ny = canvas.coords(self.nome_id)
            self.nome_x = int(nx / self.escala_tela)
            self.nome_y = int(ny / self.escala_tela)

            if self.assinatura_path:
                ax, ay = canvas.coords(self.ass_id)
                self.ass_x = int(ax / self.escala_tela)
                self.ass_y = int(ay / self.escala_tela)

            top.destroy()

        tb.Button(
            frame_controles, text="✔ CONFIRMAR",
            command=salvar_posicoes, bootstyle="success",
        ).pack(side="right", padx=10)

    # ------------------------------------------------------------------ #
    #  GERAÇÃO EM LOTE                                                   #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _sanitizar_nome(nome: str) -> str:
        """Remove caracteres inválidos para nome de arquivo (Windows-safe)."""
        return re.sub(r'[\\/:*?"<>|]', "_", nome).strip() or "sem_nome"

    def gerar_certificados(self):
        if not self.template_path or not self.dados_path:
            messagebox.showerror(
                "Erro",
                "Arquivos base incompletos (Template e Dados são obrigatórios).",
            )
            return

        try:
            df = (
                pd.read_csv(self.dados_path)
                if self.dados_path.endswith(".csv")
                else pd.read_excel(self.dados_path)
            )

            if "Nome" not in df.columns:
                messagebox.showerror(
                    "Erro",
                    "A planilha precisa ter uma coluna chamada 'Nome'.",
                )
                return

            os.makedirs("Certificados_Gerados", exist_ok=True)

            try:
                fonte = ImageFont.truetype(self.fonte_path, self.tamanho_fonte)
            except IOError:
                fonte = ImageFont.load_default()

            total = len(df)
            self.progress["maximum"] = total
            self.progress["value"] = 0

            for index, row in df.iterrows():
                nome = str(row["Nome"])

                with Image.open(self.template_path) as imagem:
                    draw = ImageDraw.Draw(imagem)
                    draw.text(
                        (self.nome_x, self.nome_y), nome, font=fonte, fill="black"
                    )

                    if self.assinatura_path:
                        with Image.open(self.assinatura_path) as assinatura:
                            assinatura = assinatura.convert("RGBA")
                            nova_largura = int(assinatura.width * self.escala_ass)
                            nova_altura = int(assinatura.height * self.escala_ass)
                            try:
                                assinatura = assinatura.resize(
                                    (nova_largura, nova_altura),
                                    Image.Resampling.LANCZOS,
                                )
                            except AttributeError:
                                assinatura = assinatura.resize(
                                    (nova_largura, nova_altura), Image.ANTIALIAS
                                )
                            imagem.paste(
                                assinatura, (self.ass_x, self.ass_y), assinatura
                            )

                    nome_seguro = self._sanitizar_nome(nome)
                    imagem.save(
                        f"Certificados_Gerados/Certificado_{nome_seguro}.png"
                    )

                self.progress["value"] = index + 1
                self.lbl_status.config(
                    text=f"Processando: {index + 1}/{total} — {nome}",
                    bootstyle="info",
                )
                self.root.update_idletasks()

            self.lbl_status.config(
                text=f"✓ {total} certificados gerados com sucesso!",
                bootstyle="success",
            )
            messagebox.showinfo(
                "Concluído", "Lote gerado na pasta 'Certificados_Gerados'!"
            )
            self.progress["value"] = 0

        except Exception as e:
            messagebox.showerror("Erro", f"Falha na geração: {str(e)}")
            self.lbl_status.config(
                text="Erro durante a geração", bootstyle="danger"
            )


# ---------------------------------------------------------------------- #
#  PONTO DE ENTRADA                                                      #
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    app_window = tb.Window(themename="darkly")

    # Ícone da janela (opcional)
    caminho_icone = "CertificadoApp.ico"
    if os.path.exists(caminho_icone):
        try:
            app_window.iconbitmap(caminho_icone)
        except Exception:
            pass  # alguns sistemas não suportam .ico

    # Link "Como usar" com contraste melhor no tema darkly
    app_window.style.configure(
        "Link.TButton",
        foreground="#4a9eff",
        font=("Segoe UI", 9, "underline"),
    )

    app = CertificadoApp(app_window)
    app_window.mainloop()
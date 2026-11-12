# 🎓 Gerador de Certificados PRO

Um aplicativo desktop moderno desenvolvido em Python para automatizar a geração de certificados em lote. Ele permite carregar um template base, uma lista de nomes via planilha (Excel/CSV) e posicionar textos e assinaturas visualmente usando *Drag & Drop* antes de exportar centenas de certificados em segundos.

## ✨ Funcionalidades

* **Modelagem Visual (Drag & Drop):** Arraste o nome e a assinatura diretamente sobre o template para definir a posição exata (X, Y).
* **Pré-visualização em Tempo Real:** Ajuste o tamanho da fonte e a escala da assinatura com sliders e veja o resultado antes de gerar.
* **Fontes Personalizadas:** Suporte total para carregar fontes customizadas (`.ttf` / `.otf`) para combinar com o design do seu certificado.
* **Processamento em Lote:** Lê os nomes de planilhas `.xlsx` ou `.csv` e gera arquivos `.png` individuais para cada aluno.
* **Interface Moderna:** UI limpa e responsiva construída com `ttkbootstrap` (tema dark).
* **Feedback Visual:** Barra de progresso e status de execução em tempo real para evitar telas congeladas.

## 🚀 Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado na sua máquina.

As bibliotecas necessárias para rodar o projeto estão listadas no arquivo `requirements.txt`.

```bash
# Clone o repositório
git clone https://github.com/0t4v14n0/gerador-certificados-pro.git
cd gerador-certificados-pro

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv .venv

# Ative o ambiente virtual (Windows)
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## 🛠️ Como Usar (Código-Fonte)

1. Execute o aplicativo:
   ```bash
   python app.py
   ```
2. **Passo 1:** Selecione a imagem de fundo do seu certificado (Template) e, opcionalmente, uma imagem de assinatura com fundo transparente (PNG).
3. **Passo 2:** Clique em "Ajustar Posições, Fontes e Tamanho". Arraste os elementos na tela para os locais corretos e clique em "Confirmar".
4. **Passo 3:** Selecione a planilha. **Importante:** A planilha deve conter obrigatoriamente uma coluna com o cabeçalho exato escrito `Nome`.
5. Clique em **Gerar Certificados**. Os arquivos finais serão salvos automaticamente na pasta `Certificados_Gerados`.

## 📦 Como Compilar para `.exe` (Windows)

Para distribuir o aplicativo como um executável autônomo (sem necessidade de instalar o Python), utilize o `PyInstaller`.

1. Instale o PyInstaller no seu ambiente virtual:
   ```bash
   pip install pyinstaller
   ```
2. Rode o comando de compilação (forçando a coleta do tema visual do ttkbootstrap):
   ```bash
   pyinstaller --noconsole --onefile --icon=CertificadoApp.ico --collect-all ttkbootstrap app.py
   ```
3. O executável pronto para uso estará na pasta `dist/`.

## 💻 Tecnologias Utilizadas

* **Python 3**
* **Tkinter + ttkbootstrap:** Criação da interface gráfica com temas modernos.
* **Pillow (PIL):** Manipulação, redimensionamento e renderização de textos nas imagens.
* **Pandas / openpyxl:** Leitura inteligente de dados em arquivos CSV e planilhas Excel.

---
Desenvolvido por **Otaviano Cruz**.
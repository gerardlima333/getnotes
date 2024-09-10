import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import tempfile
import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
class ListaDeComprasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Compras")
        self.root.geometry("600x500")

     
        self.title_font = tkfont.Font(family='Arial', size=24, weight="bold")
        self.label_font = tkfont.Font(family='Arial', size=12)
        self.entry_font = tkfont.Font(family='Arial', size=10)

        self.marca = ""
        self.produto = ""
        self.data = ""
        self.preco = ""
        self.metodo_pagamento = ""

       
        self.vendas = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Lista de Compras", font=self.title_font)
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        
        tk.Label(self.frame, text="Marca:", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_marca = tk.Entry(self.frame, font=self.entry_font, width=30)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Produto:", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_produto = tk.Entry(self.frame, font=self.entry_font, width=30)
        self.entry_produto.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Data:", font=self.label_font).grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_data = tk.Entry(self.frame, font=self.entry_font, width=30)
        self.entry_data.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Preço:", font=self.label_font).grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_preco = tk.Entry(self.frame, font=self.entry_font, width=30)
        self.entry_preco.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Método de Pagamento:", font=self.label_font).grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_metodo_pagamento = tk.Entry(self.frame, font=self.entry_font, width=30)
        self.entry_metodo_pagamento.grid(row=5, column=1, padx=5, pady=5)

        # Botões
        self.button_adicionar = tk.Button(self.frame, text="Adicionar Venda", font=self.label_font, command=self.adicionar_venda)
        self.button_adicionar.grid(row=6, column=0, columnspan=2, pady=10)

        self.button_imprimir_vendas = tk.Button(self.frame, text="fechar caixa", font=self.label_font, command=self.imprimir_lista_vendas)
        self.button_imprimir_vendas.grid(row=8, column=0, columnspan=2, pady=10)

        self.button_sair = tk.Button(self.frame, text="Sair", font=self.label_font, command=self.root.quit)
        self.button_sair.grid(row=10, column=0, columnspan=2, pady=10)

    def adicionar_venda(self):
        marca = self.entry_marca.get().strip()
        produto = self.entry_produto.get().strip()
        data = self.entry_data.get().strip()
        preco = self.entry_preco.get().strip()
        metodo_pagamento = self.entry_metodo_pagamento.get().strip()

        if marca and produto and data and preco and metodo_pagamento:
            self.vendas.append((marca, produto, data, preco, metodo_pagamento))
            messagebox.showinfo("Sucesso", f"Venda de '{produto}' adicionada à lista.")
            self.entry_marca.delete(0, tk.END)
            self.entry_produto.delete(0, tk.END)
            self.entry_data.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)
            self.entry_metodo_pagamento.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

    def fechar_caixa(self):
        if not self.vendas:
            messagebox.showwarning("Aviso", "Não há vendas para fechar o caixa.")
            return

       
        self.fechar_caixa.extend(self.vendas)
        self.vendas = []  

    
        pdf_file = f"fechar_caixa_{date.today().strftime('%Y-%m-%d')}.pdf"
        self.gerar_pdf_fechar_caixa(pdf_file)

        messagebox.showinfo("Caixa Fechado", "O caixa foi fechado com sucesso.")

    def imprimir_lista_vendas(self):
        if not self.vendas:
            messagebox.showwarning("Aviso", "Lista de vendas está vazia.")
            return

       
        pdf_file = f"lista_vendas_{date.today().strftime('%Y-%m-%d')}.pdf"
        self.gerar_pdf_venda(pdf_file)

        os.startfile(pdf_file)
    

    def gerar_pdf_venda(self, pdf_file):
        c = canvas.Canvas(pdf_file, pagesize=A4)
        c.setFont("Helvetica", 10)  

        ficha_width = 150  
        ficha_height = 70 

        x_spacing = 15  
        y_spacing = 15

        x_start = 20
        y_start = 800


        for venda in reversed(self.vendas):
            marca, produto, data, preco, metodo_pagamento = venda

            c.rect(x_start, y_start - ficha_height, ficha_width, ficha_height)  # Caixa da ficha


            c.drawString(x_start + 10, y_start - 10, f"Marca: {marca}")
            c.drawString(x_start + 10, y_start - 20, f"Produto: {produto}")
            c.drawString(x_start + 10, y_start - 30, f"Data: {data}")

      
            hora_atual = datetime.now().strftime('%H:%M:%S')
            c.drawString(x_start + 10, y_start - 40, f"Hora: {hora_atual}")

            c.drawString(x_start + 10, y_start - 50, f"Preço: R${preco}")
            c.drawString(x_start + 10, y_start - 60, f"Método de Pagamento: {metodo_pagamento}")

            x_start += ficha_width + x_spacing


            if x_start + ficha_width > A4[0] - x_spacing:
                x_start = 20
                y_start -= ficha_height + y_spacing



        c.save()


    def imprimir_fechar_caixa(self):
        if not self.fechar_caixa:
            messagebox.showwarning("Aviso", "Fechamento de caixa está vazio.")
            return

        pdf_file = f"fechar_caixa_{date.today().strftime('%Y-%m-%d')}.pdf"
        self.gerar_pdf_fechar_caixa(pdf_file)

        os.startfile(pdf_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = ListaDeComprasApp(root)
    root.mainloop()

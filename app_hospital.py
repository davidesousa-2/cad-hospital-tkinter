import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os

class AppHospital(tb.Window):
    def __init__(self):
        # Inicializa a janela com o tema 'flatly' (moderno, limpo e ótimo para saúde)
        super().__init__(themename="flatly")

        # Configurações da Janela
        self.title("Sistema Hospitalar - Cadastro de Paciente")
        self.geometry("550x850")
        self.resizable(False, False)

        # Título da Tela
        self.titulo = tb.Label(
            self, 
            text="Cadastro de Paciente", 
            font=("Helvetica", 20, "bold"), 
            bootstyle="primary"
        )
        self.titulo.pack(pady=(25, 15))

        # Container Principal para os Campos
        self.frame = tb.Frame(self)
        self.frame.pack(fill="x", padx=40)

        # --- Nome Completo ---
        self.lbl_nome = tb.Label(self.frame, text="Nome Completo:", font=("Helvetica", 11, "bold"))
        self.lbl_nome.pack(anchor="w", pady=(5, 2))
        self.txt_nome = tb.Entry(self.frame, width=50)
        self.txt_nome.pack(fill="x", pady=(0, 5))

        # --- CPF ---
        self.lbl_cpf = tb.Label(self.frame, text="CPF:", font=("Helvetica", 11, "bold"))
        self.lbl_cpf.pack(anchor="w", pady=(5, 2))
        self.txt_cpf = tb.Entry(self.frame, width=50)
        self.txt_cpf.pack(fill="x", pady=(0, 5))
        # Nota: Placeholder text em Entry tradicional/ttk requer bindings,
        # para manter o código limpo, os campos começam vazios.

        # --- Data de Nascimento ---
        self.lbl_nascimento = tb.Label(self.frame, text="Data de Nascimento (DD/MM/AAAA):", font=("Helvetica", 11, "bold"))
        self.lbl_nascimento.pack(anchor="w", pady=(5, 2))
        self.txt_nascimento = tb.Entry(self.frame, width=50)
        self.txt_nascimento.pack(fill="x", pady=(0, 5))

        # --- Gênero ---
        self.lbl_genero = tb.Label(self.frame, text="Gênero:", font=("Helvetica", 11, "bold"))
        self.lbl_genero.pack(anchor="w", pady=(5, 2))
        self.cbo_genero = tb.Combobox(
            self.frame, 
            values=["Masculino", "Feminino", "Outro", "Não informar"], 
            state="readonly"
        )
        self.cbo_genero.pack(fill="x", pady=(0, 5))
        self.cbo_genero.set("Selecione...")

        # --- Tipo Sanguíneo ---
        self.lbl_sangue = tb.Label(self.frame, text="Tipo Sanguíneo:", font=("Helvetica", 11, "bold"))
        self.lbl_sangue.pack(anchor="w", pady=(5, 2))
        self.cbo_sangue = tb.Combobox(
            self.frame, 
            values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
            state="readonly"
        )
        self.cbo_sangue.pack(fill="x", pady=(0, 20))
        self.cbo_sangue.set("Selecione...")

        # --- Botão de Salvar ---
        # O bootstyle="success" deixa o botão verde, ideal para ações positivas/salvar
        self.btn_salvar = tb.Button(
            self.frame, 
            text="Cadastrar Paciente", 
            command=self.salvar_cadastro, 
            bootstyle="success",
        )
        self.btn_salvar.pack(fill="x", pady=(0, 20))

        # -------------------------------------------------------------
        # ÁREA DE RESULTADOS (Exibição dos Pacientes Cadastrados)
        # -------------------------------------------------------------
        self.lbl_resultados = tb.Label(self, text="Pacientes Cadastrados:", font=("Helvetica", 12, "bold"), bootstyle="secondary")
        self.lbl_resultados.pack(anchor="w", padx=40, pady=(10, 5))

        # Caixa de texto com barra de rolagem (ScrolledText) estilizada pelo bootstrap
        self.txt_resultados = ScrolledText(self, width=50, height=10, font=("Courier New", 10))
        self.txt_resultados.pack(fill="both", expand=True, padx=40, pady=(0, 30))
        
        # Carrega os pacientes já existentes se o arquivo já tiver dados
        self.atualizar_lista_resultados()

    def salvar_cadastro(self):
        nome = self.txt_nome.get().strip()
        cpf = self.txt_cpf.get().strip()
        nascimento = self.txt_nascimento.get().strip()
        genero = self.cbo_genero.get()
        sangue = self.cbo_sangue.get()

        if not nome or not cpf or not nascimento or genero == "Selecione..." or sangue == "Selecione...":
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos.")
            return

        dados_paciente = f"Nome: {nome} | CPF: {cpf} | Nasc: {nascimento} | Gênero: {genero} | Sangue: {sangue}\n"

        try:
            with open("pacientes.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(dados_paciente)
            
            messagebox.showinfo("Sucesso", f"Paciente {nome} cadastrado!")
            
            self.limpar_campos()
            self.atualizar_lista_resultados() # Atualiza a tela com o novo paciente
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")

    def atualizar_lista_resultados(self):
        """Lê o arquivo de texto e exibe tudo dentro da caixinha de resultados"""
        # Habilita a edição temporariamente para atualizar o texto
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("1.0", "end")
        
        if os.path.exists("pacientes.txt"):
            with open("pacientes.txt", "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                self.txt_resultados.insert("1.0", conteudo)
        else:
            self.txt_resultados.insert("1.0", "Nenhum paciente cadastrado ainda.")
            
        # Bloqueia o usuário de digitar direto na caixa de resultados
        self.txt_resultados.configure(state="disabled")

    def limpar_campos(self):
        self.txt_nome.delete(0, 'end')
        self.txt_cpf.delete(0, 'end')
        self.txt_nascimento.delete(0, 'end')
        self.cbo_genero.set("Selecione...")
        self.cbo_sangue.set("Selecione...")

if __name__ == "__main__":
    app = AppHospital()
    app.mainloop()

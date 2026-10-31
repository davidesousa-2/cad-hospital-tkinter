import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os

class AppHospital(tb.Window):
    def __init__(self):
        # Inicializa a janela com o tema 'flatly'
        super().__init__(themename="flatly")

        # Configurações da Janela (Aumentada a largura para acomodar melhor a tabela)
        self.title("Sistema Hospitalar - Cadastro e Consulta")
        self.geometry("750x850")
        self.resizable(False, False)

        # Título da Tela
        self.titulo = tb.Label(
            self, 
            text="Cadastro de Paciente", 
            font=("Helvetica", 20, "bold"), 
            bootstyle="primary"
        )
        self.titulo.pack(pady=(25, 15))

        # Container Principal para os Campos de Cadastro
        self.frame = tb.Frame(self)
        self.frame.pack(fill="x", padx=40)

        # --- Nome Completo ---
        self.lbl_nome = tb.Label(self.frame, text="Nome Completo:", font=("Helvetica", 11, "bold"))
        self.lbl_nome.pack(anchor="w", pady=(5, 2))
        self.txt_nome = tb.Entry(self.frame)
        self.txt_nome.pack(fill="x", pady=(0, 5))

        # --- CPF ---
        self.lbl_cpf = tb.Label(self.frame, text="CPF:", font=("Helvetica", 11, "bold"))
        self.lbl_cpf.pack(anchor="w", pady=(5, 2))
        self.txt_cpf = tb.Entry(self.frame)
        self.txt_cpf.pack(fill="x", pady=(0, 5))

        # --- Data de Nascimento ---
        self.lbl_nascimento = tb.Label(self.frame, text="Data de Nascimento (DD/MM/AAAA):", font=("Helvetica", 11, "bold"))
        self.lbl_nascimento.pack(anchor="w", pady=(5, 2))
        self.txt_nascimento = tb.Entry(self.frame)
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
        self.btn_salvar = tb.Button(
            self.frame, 
            text="Cadastrar Paciente", 
            command=self.salvar_cadastro, 
            bootstyle="success",
        )
        self.btn_salvar.pack(fill="x", pady=(0, 25))

        # -------------------------------------------------------------
        # ÁREA DE CONSULTA (Tabela e Busca)
        # -------------------------------------------------------------
        # Divisor visual
        self.separador = tb.Separator(self, bootstyle="secondary")
        self.separador.pack(fill="x", padx=40, pady=10)

        # Container para a barra de busca
        self.frame_busca = tb.Frame(self)
        self.frame_busca.pack(fill="x", padx=40, pady=(10, 5))

        self.lbl_busca = tb.Label(self.frame_busca, text="Buscar por CPF:", font=("Helvetica", 11, "bold"))
        self.lbl_busca.pack(side="left", padx=(0, 10))
        
        self.txt_busca = tb.Entry(self.frame_busca, width=30)
        self.txt_busca.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Evento para buscar em tempo real enquanto digita
        self.txt_busca.bind("<KeyRelease>", self.filtrar_pacientes)

        # Container para a tabela e sua barra de rolagem
        self.frame_tabela = tb.Frame(self)
        self.frame_tabela.pack(fill="both", expand=True, padx=40, pady=(10, 30))

        # Configuração das colunas da tabela
        colunas = ("nome", "cpf", "nascimento", "genero", "sangue")
        self.tabela = tb.Treeview(
            self.frame_tabela, 
            columns=colunas, 
            show="headings", 
            bootstyle="primary"
        )
        
        # Definindo os cabeçalhos e tamanhos das colunas
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("cpf", text="CPF")
        self.tabela.heading("nascimento", text="Data Nasc.")
        self.tabela.heading("genero", text="Gênero")
        self.tabela.heading("sangue", text="Alt.")

        self.tabela.column("nome", width=200, anchor="w")
        self.tabela.column("cpf", width=120, anchor="center")
        self.tabela.column("nascimento", width=100, anchor="center")
        self.tabela.column("genero", width=100, anchor="center")
        self.tabela.column("sangue", width=50, anchor="center")

        # Barra de rolagem para a tabela
        self.scrollbar = tb.Scrollbar(self.frame_tabela, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=self.scrollbar.set)

        # Empacotando tabela e scrollbar lado a lado
        self.tabela.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Carrega os pacientes na tabela
        self.atualizar_tabela()

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
            self.atualizar_tabela() # Atualiza a tabela com o novo paciente
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")

    def ler_arquivo_pacientes(self):
        """Função auxiliar para ler o arquivo txt e estruturar os dados em uma lista de dicionários"""
        lista_pacientes = []
        if os.path.exists("pacientes.txt"):
            with open("pacientes.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    if "Nome:" in linha:
                        try:
                            # Divide a linha usando o caractere '|' e limpa os textos
                            partes = [p.split(":")[1].strip() for p in linha.split("|")]
                            lista_pacientes.append({
                                "nome": partes[0],
                                "cpf": partes[1],
                                "nascimento": partes[2],
                                "genero": partes[3],
                                "sangue": partes[4]
                            })
                        except IndexError:
                            continue # Pula linhas que possam estar corrompidas
        return lista_pacientes

    def atualizar_tabela(self, lista_customizada=None):
        """Limpa a tabela e insere os dados fornecidos ou lê direto do arquivo"""
        # Limpa todas as linhas atuais da tabela
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        
        # Se não passarmos uma lista filtrada, pegamos todos os pacientes do arquivo
        pacientes = lista_customizada if lista_customizada is not None else self.ler_arquivo_pacientes()
        
        # Insere os dados na tabela
        for p in pacientes:
            self.tabela.insert("", "end", values=(p["nome"], p["cpf"], p["nascimento"], p["genero"], p["sangue"]))

    def filtrar_pacientes(self, event):
        """Filtra os pacientes na tabela em tempo real conforme o usuário digita o CPF"""
        termo_busca = self.txt_busca.get().strip()
        todos_pacientes = self.ler_arquivo_pacientes()
        
        # Filtra a lista mantendo apenas os pacientes onde o CPF contém o termo digitado
        pacientes_filtrados = [p for p in todos_pacientes if termo_busca in p["cpf"]]
        
        # Atualiza a tabela apenas com os resultados do filtro
        self.atualizar_tabela(pacientes_filtrados)

    def limpar_campos(self):
        self.txt_nome.delete(0, 'end')
        self.txt_cpf.delete(0, 'end')
        self.txt_nascimento.delete(0, 'end')
        self.cbo_genero.set("Selecione...")
        self.cbo_sangue.set("Selecione...")

if __name__ == "__main__":
    app = AppHospital()
    app.mainloop()

import customtkinter as ctk
from tkinter import messagebox
import os

# Configuração do tema visual (moderno e limpo)
ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

class AppHospital(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela (Aumentada para caber a lista de resultados)
        self.title("Sistema Hospitalar - Cadastro de Paciente")
        self.geometry("550x850")
        self.resizable(False, False)

        # Título da Tela
        self.titulo = ctk.CTkLabel(self, text="Cadastro de Paciente", font=ctk.CTkFont(size=24, weight="bold"))
        self.titulo.pack(pady=(20, 10))

        # Container Principal para os Campos
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(fill="x", padx=40)

        # --- Nome Completo ---
        self.lbl_nome = ctk.CTkLabel(self.frame, text="Nome Completo:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_nome.pack(anchor="w", pady=(5, 2))
        self.txt_nome = ctk.CTkEntry(self.frame, placeholder_text="Digite o nome completo", width=470)
        self.txt_nome.pack(anchor="w", pady=(0, 5))

        # --- CPF ---
        self.lbl_cpf = ctk.CTkLabel(self.frame, text="CPF:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_cpf.pack(anchor="w", pady=(5, 2))
        self.txt_cpf = ctk.CTkEntry(self.frame, placeholder_text="000.000.000-00", width=470)
        self.txt_cpf.pack(anchor="w", pady=(0, 5))

        # --- Data de Nascimento ---
        self.lbl_nascimento = ctk.CTkLabel(self.frame, text="Data de Nascimento:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_nascimento.pack(anchor="w", pady=(5, 2))
        self.txt_nascimento = ctk.CTkEntry(self.frame, placeholder_text="DD/MM/AAAA", width=470)
        self.txt_nascimento.pack(anchor="w", pady=(0, 5))

        # --- Gênero ---
        self.lbl_genero = ctk.CTkLabel(self.frame, text="Gênero:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_genero.pack(anchor="w", pady=(5, 2))
        self.cbo_genero = ctk.CTkComboBox(self.frame, values=["Masculino", "Feminino", "Outro", "Não informar"], width=470, state="readonly")
        self.cbo_genero.pack(anchor="w", pady=(0, 5))
        self.cbo_genero.set("Selecione...")
        

        # --- Tipo Sanguíneo ---
        self.lbl_sangue = ctk.CTkLabel(self.frame, text="Tipo Sanguíneo:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_sangue.pack(anchor="w", pady=(5, 2))
        self.cbo_sangue = ctk.CTkComboBox(self.frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], width=470, state="readonly")
        self.cbo_sangue.pack(anchor="w", pady=(0, 15))
        self.cbo_sangue.set("Selecione...")

        # --- Botão de Salvar ---
        self.btn_salvar = ctk.CTkButton(self.frame, text="Cadastrar Paciente", command=self.salvar_cadastro, height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_salvar.pack(fill="x", pady=(0, 15))

        # -------------------------------------------------------------
        # ÁREA DE RESULTADOS (Exibição dos Pacientes Cadastrados)
        # -------------------------------------------------------------
        self.lbl_resultados = ctk.CTkLabel(self, text="Pacientes Cadastrados:", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_resultados.pack(anchor="w", padx=40, pady=(10, 5))

        # Caixa de texto com barra de rolagem automática
        self.txt_resultados = ctk.CTkTextbox(self, width=470, height=220, font=ctk.CTkFont(size=12))
        self.txt_resultados.pack(padx=40, pady=(0, 20))
        
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
        self.txt_resultados.delete("0.0", "end")
        
        if os.path.exists("pacientes.txt"):
            with open("pacientes.txt", "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                self.txt_resultados.insert("0.0", conteudo)
        else:
            self.txt_resultados.insert("0.0", "Nenhum paciente cadastrado ainda.")
            
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

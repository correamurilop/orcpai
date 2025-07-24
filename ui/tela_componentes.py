import customtkinter as ctk
from core import file_manager
from core.models import Componente
from core import componentes_manager
import tkinter.messagebox as messagebox

class TelaComponentes(ctk.CTkFrame):
    def __init__(self, master, janela_principal, painel, orcamento, caminho_arquivo):
        super().__init__(master)
        self.janela_principal = janela_principal
        self.painel = painel
        self.orcamento = orcamento
        self.caminho_arquivo = caminho_arquivo

        # Título da tela
        self.label_titulo = ctk.CTkLabel(
            self, 
            text=f"Componentes do Painel: {painel.nome}", 
            font=("Arial", 20, "bold")
        )
        self.label_titulo.pack(pady=20)

        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="⬅️ Voltar aos Painéis",
            command=self.voltar_paineis,
            height=30
        )
        self.btn_voltar.pack(pady=10, padx=20, anchor="w")

        # Frame para adicionar componentes
        self.frame_adicionar = ctk.CTkFrame(self)
        self.frame_adicionar.pack(pady=10, padx=20, fill="x")

        self.label_adicionar = ctk.CTkLabel(
            self.frame_adicionar, 
            text="Buscar e Adicionar Componente:", 
            font=("Arial", 14, "bold")
        )
        self.label_adicionar.pack(pady=10)

        # Frame para busca de componentes
        self.frame_busca = ctk.CTkFrame(self.frame_adicionar)
        self.frame_busca.pack(pady=10, padx=20, fill="x")

        self.label_busca = ctk.CTkLabel(self.frame_busca, text="🔍 Buscar componente:")
        self.label_busca.pack(side="left", padx=(0, 10))

        self.entry_busca_comp = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Digite para buscar componentes...",
            width=250
        )
        self.entry_busca_comp.pack(side="left", padx=(0, 10))
        self.entry_busca_comp.bind("<KeyRelease>", self.filtrar_componentes_cadastrados)



        # Frame para lista de componentes (sempre visível)
        self.frame_lista_comp = ctk.CTkFrame(self.frame_adicionar)
        self.frame_lista_comp.pack(pady=10, padx=20, fill="x")

        self.scrollable_comp = ctk.CTkScrollableFrame(self.frame_lista_comp, height=150)
        self.scrollable_comp.pack(fill="both", expand=True, padx=5, pady=5)



        # Frame para lista de componentes
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista, 
            text="Componentes do Painel:", 
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=10)

        # ScrollableFrame para lista de componentes
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista, height=200)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para botões de ação
        self.frame_acoes = ctk.CTkFrame(self.frame_lista)
        self.frame_acoes.pack(pady=10, fill="x")

        self.btn_salvar = ctk.CTkButton(
            self.frame_acoes, 
            text="💾 Salvar Alterações", 
            command=self.salvar,
            fg_color="green",
            hover_color="darkgreen",
            height=40
        )
        self.btn_salvar.pack(side="left", padx=10, fill="x", expand=True)



        # Atualizar breadcrumb no menu lateral
        self.janela_principal.atualizar_breadcrumb_painel(
            self.orcamento.nome, 
            self.painel.nome, 
            self.voltar_paineis
        )
        
        # Inicializar sistema de componentes e carregar dados
        componentes_manager.inicializar_componentes()
        self.atualizar_lista_componentes()
        self.atualizar_lista_componentes_cadastrados()

    def filtrar_componentes_cadastrados(self, event=None):
        """Filtra componentes conforme o texto digitado"""
        self.atualizar_lista_componentes_cadastrados()

    def atualizar_lista_componentes_cadastrados(self):
        """Atualiza a lista de componentes cadastrados"""
        # Limpar lista atual
        for widget in self.scrollable_comp.winfo_children():
            widget.destroy()

        # Obter filtro
        termo_busca = self.entry_busca_comp.get()
        
        # Buscar componentes
        componentes_encontrados = componentes_manager.buscar_componentes(termo_busca)

        if not componentes_encontrados:
            label_vazio = ctk.CTkLabel(
                self.scrollable_comp,
                text="Nenhum componente encontrado.",
                font=("Arial", 10, "italic"),
                text_color="gray"
            )
            label_vazio.pack(pady=10)
            return

        # Criar item para cada componente
        for comp_info in componentes_encontrados:
            self.criar_item_componente_cadastrado(comp_info)

    def criar_item_componente_cadastrado(self, comp_info):
        """Cria um item visual para um componente cadastrado"""
        frame_item = ctk.CTkFrame(self.scrollable_comp)
        frame_item.pack(fill="x", padx=5, pady=2)

        # Informações do componente
        texto_comp = f"⚙️ {comp_info.nome}"

        label_info = ctk.CTkLabel(
            frame_item,
            text=texto_comp,
            font=("Arial", 11),
            anchor="w"
        )
        label_info.pack(side="left", padx=10, pady=5, fill="x", expand=True)

        # Botão adicionar
        btn_add = ctk.CTkButton(
            frame_item,
            text="➕ Adicionar",
            command=lambda: self.adicionar_componente_cadastrado(comp_info),
            width=80,
            height=25,
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_add.pack(side="right", padx=5, pady=5)



    def adicionar_componente_cadastrado(self, comp_info):
        """Adiciona um componente cadastrado ao painel"""
        # Dialog para pedir quantidade
        dialog = ctk.CTkInputDialog(
            text=f"Quantidade para '{comp_info.nome}':",
            title="Adicionar Componente"
        )
        quantidade_str = dialog.get_input()
        
        if quantidade_str is None:  # Usuário cancelou
            return
            
        try:
            quantidade_str = quantidade_str.strip()
            if not quantidade_str:
                messagebox.showwarning("Aviso", "Digite a quantidade do componente.")
                return

            quantidade = int(quantidade_str)
            if quantidade <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Aviso", "Digite uma quantidade válida (número inteiro positivo).")
            return

        # Verificar se componente já existe
        componente_existente = self.painel.obter_componente(comp_info.nome)
        if componente_existente:
            # Perguntar se quer somar as quantidades
            resposta = messagebox.askyesno(
                "Componente Existente",
                f"O componente '{comp_info.nome}' já existe com quantidade {componente_existente.quantidade}.\n\n"
                f"Deseja somar {quantidade} à quantidade existente?"
            )
            if resposta:
                componente_existente.quantidade += quantidade
                messagebox.showinfo("Sucesso", f"Quantidade atualizada para {componente_existente.quantidade}.")
            else:
                return
        else:
            # Adicionar novo componente
            novo_componente = Componente(nome=comp_info.nome, quantidade=quantidade)
            self.painel.adicionar_componente(novo_componente)
            messagebox.showinfo("Sucesso", f"Componente '{comp_info.nome}' adicionado com sucesso!")

        # Salvar automaticamente no arquivo
        try:
            file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar componente: {str(e)}")
            return

        # Limpar campo quantidade e atualizar lista
        entry_qtd.delete(0, "end")
        self.atualizar_lista_componentes()



    def atualizar_lista_componentes(self):
        """Atualiza a lista visual de componentes"""
        # Limpar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.painel.componentes:
            label_vazio = ctk.CTkLabel(
                self.scrollable_frame, 
                text="Nenhum componente adicionado ainda.",
                font=("Arial", 12, "italic")
            )
            label_vazio.pack(pady=20)
            return

        # Adicionar cada componente
        for i, componente in enumerate(self.painel.componentes):
            frame_item = ctk.CTkFrame(self.scrollable_frame)
            frame_item.pack(fill="x", padx=5, pady=2)

            # Label com informações do componente
            label_info = ctk.CTkLabel(
                frame_item,
                text=f"{componente.quantidade}x {componente.nome}",
                font=("Arial", 12),
                anchor="w"
            )
            label_info.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # Botão excluir
            btn_excluir = ctk.CTkButton(
                frame_item,
                text="🗑️",
                command=lambda nome=componente.nome: self.excluir_componente(nome),
                width=40,
                height=30,
                fg_color="red",
                hover_color="darkred"
            )
            btn_excluir.pack(side="right", padx=5, pady=5)



    def excluir_componente(self, nome_componente):
        """Exclui um componente do painel"""
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o componente '{nome_componente}'?"
        )
        
        if resposta:
            self.painel.remover_componente(nome_componente)
            
            # Salvar automaticamente no arquivo
            try:
                file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
                self.atualizar_lista_componentes()
                messagebox.showinfo("Sucesso", "Componente excluído e salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar exclusão: {str(e)}")

    def salvar(self):
        """Salva as alterações no arquivo de orçamento"""
        try:
            file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def voltar_paineis(self):
        """Volta para a tela de painéis"""
        from ui.tela_paineis import TelaPaineis
        
        # Limpar breadcrumb
        self.janela_principal.limpar_breadcrumb()
        
        for widget in self.master.winfo_children():
            widget.destroy()

        tela_paineis = TelaPaineis(
            self.master, 
            self.janela_principal, 
            self.orcamento, 
            self.caminho_arquivo
        )
        tela_paineis.pack(fill="both", expand=True) 
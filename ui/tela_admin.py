import customtkinter as ctk
import json
import tkinter.messagebox as messagebox
from core import componentes_manager
from core.componentes_manager import ComponenteInfo

class TelaAdmin(ctk.CTkFrame):
    def __init__(self, master, janela_principal):
        super().__init__(master)
        self.janela_principal = janela_principal
        self.componente_selecionado = None

        # Título da tela
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="🔧 Administração de Componentes", 
            font=("Arial", 20, "bold")
        )
        self.label_titulo.pack(pady=20)

        # Aviso de acesso administrativo
        self.label_aviso = ctk.CTkLabel(
            self,
            text="⚠️ ÁREA ADMINISTRATIVA - Gerencie os componentes do sistema",
            font=("Arial", 12, "bold"),
            text_color="orange"
        )
        self.label_aviso.pack(pady=5)

        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="⬅️ Voltar ao Início",
            command=self.voltar_inicio,
            height=30
        )
        self.btn_voltar.pack(pady=10, padx=20, anchor="w")

        # Frame para busca e ações
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(pady=10, padx=20, fill="x")

        self.label_busca = ctk.CTkLabel(
            self.frame_busca, 
            text="🔍 Procurar componente:", 
            font=("Arial", 14)
        )
        self.label_busca.pack(side="left", padx=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Digite para filtrar componentes...",
            width=300
        )
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_componentes)

        self.btn_limpar_busca = ctk.CTkButton(
            self.frame_busca,
            text="✖️ Limpar",
            command=self.limpar_busca,
            width=80,
            height=30
        )
        self.btn_limpar_busca.pack(side="left", padx=5)

        # Botão adicionar componente na área de busca
        self.btn_adicionar_topo = ctk.CTkButton(
            self.frame_busca,
            text="➕ Novo Componente",
            command=self.adicionar_componente,
            width=140,
            height=30,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_adicionar_topo.pack(side="right", padx=10)

        # Frame para lista de componentes
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista, 
            text="Componentes cadastrados:", 
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=10)

        # ScrollableFrame para lista de componentes
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista, height=400)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para botões de ação
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=20, padx=20, fill="x")

        # Botões de ação principais
        self.btn_editar = ctk.CTkButton(
            self.frame_botoes, 
            text="✏️ Editar Componente", 
            command=self.editar_componente,
            height=40
        )
        self.btn_editar.pack(side="left", padx=10, fill="x", expand=True)

        self.btn_excluir = ctk.CTkButton(
            self.frame_botoes, 
            text="🗑️ Excluir Componente", 
            command=self.excluir_componente,
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        self.btn_excluir.pack(side="left", padx=10, fill="x", expand=True)

        # Inicializar sistema e carregar componentes
        componentes_manager.inicializar_componentes()
        self.atualizar_lista_visual()

    def atualizar_lista_visual(self, filtro=""):
        """Atualiza a lista visual de componentes"""
        # Limpar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.componente_selecionado = None
        
        # Buscar componentes
        if filtro:
            componentes = componentes_manager.buscar_componentes(filtro)
        else:
            componentes = componentes_manager.listar_componentes_cadastrados()
        
        if not componentes:
            label_vazio = ctk.CTkLabel(
                self.scrollable_frame,
                text="Nenhum componente encontrado." if filtro else "Nenhum componente cadastrado.",
                font=("Arial", 12, "italic"),
                text_color="gray"
            )
            label_vazio.pack(pady=20)
            return
        
        # Criar item para cada componente
        for comp_info in componentes:
            self.criar_item_componente(comp_info)

    def criar_item_componente(self, comp_info):
        """Cria um item visual para um componente na lista"""
        # Frame do item
        frame_item = ctk.CTkFrame(self.scrollable_frame)
        frame_item.pack(fill="x", padx=5, pady=3)
        
        # Botão principal (nome do componente) - clicável para selecionar
        texto_componente = f"⚙️ {comp_info.nome}"
        
        btn_nome = ctk.CTkButton(
            frame_item,
            text=texto_componente,
            command=lambda: self.selecionar_componente(comp_info.nome),
            anchor="w",
            height=40,
            font=("Arial", 12)
        )
        btn_nome.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Frame para botões de ação
        frame_acoes = ctk.CTkFrame(frame_item)
        frame_acoes.pack(side="right", padx=5, pady=5)
        
        # Botão editar
        btn_editar = ctk.CTkButton(
            frame_acoes,
            text="✏️",
            command=lambda: self.editar_componente_por_nome(comp_info.nome),
            width=40,
            height=30,
            fg_color="blue",
            hover_color="darkblue"
        )
        btn_editar.pack(side="left", padx=2)
        
        # Botão excluir
        btn_excluir = ctk.CTkButton(
            frame_acoes,
            text="🗑️",
            command=lambda: self.excluir_componente_por_nome(comp_info.nome),
            width=40,
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        btn_excluir.pack(side="left", padx=2)



    def selecionar_componente(self, nome_componente):
        """Seleciona um componente (destaca visualmente)"""
        self.componente_selecionado = nome_componente
        
        # Redesenhar lista para destacar selecionado
        filtro_atual = self.entry_busca.get()
        self.atualizar_lista_visual(filtro_atual)
        
        # Destacar o selecionado
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and nome_componente in child.cget("text"):
                        child.configure(fg_color="orange", hover_color="darkorange")

    def filtrar_componentes(self, event=None):
        """Filtra componentes conforme o texto digitado"""
        filtro = self.entry_busca.get()
        self.atualizar_lista_visual(filtro)

    def limpar_busca(self):
        """Limpa o filtro de busca"""
        self.entry_busca.delete(0, "end")
        self.atualizar_lista_visual()

    def adicionar_componente(self):
        """Abre dialog para adicionar novo componente"""
        self.mostrar_dialog_componente()

    def editar_componente(self):
        """Edita o componente selecionado"""
        if not self.componente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um componente para editar.")
            return
        
        self.editar_componente_por_nome(self.componente_selecionado)

    def editar_componente_por_nome(self, nome_componente):
        """Edita um componente específico pelo nome"""
        try:
            comp_info = componentes_manager.carregar_componente_info(nome_componente)
            self.mostrar_dialog_componente(comp_info)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar componente: {str(e)}")

    def excluir_componente(self):
        """Exclui o componente selecionado"""
        if not self.componente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um componente para excluir.")
            return
        
        self.excluir_componente_por_nome(self.componente_selecionado)

    def excluir_componente_por_nome(self, nome_componente):
        """Exclui um componente específico pelo nome"""
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o componente '{nome_componente}'?\n\n"
            "Esta ação não pode ser desfeita."
        )
        
        if resposta:
            if componentes_manager.excluir_componente(nome_componente):
                self.atualizar_lista_visual()
                messagebox.showinfo("Sucesso", "Componente excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao excluir o componente.")



    def mostrar_dialog_componente(self, comp_info=None):
        """Mostra dialog para criar/editar componente"""
        # Determinar se é edição ou criação
        eh_edicao = comp_info is not None
        titulo = "Editar Componente" if eh_edicao else "Novo Componente"
        
        # Criar janela toplevel
        dialog = ctk.CTkToplevel(self)
        dialog.title(titulo)
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        
        # Centralizar na tela
        dialog.transient(self)
        dialog.grab_set()
        
        # Título
        label_titulo = ctk.CTkLabel(
            dialog,
            text=titulo,
            font=("Arial", 16, "bold")
        )
        label_titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = ctk.CTkFrame(dialog)
        frame_principal.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Nome do componente
        label_nome = ctk.CTkLabel(frame_principal, text="Nome do Componente:", font=("Arial", 12, "bold"))
        label_nome.pack(pady=(10, 5), anchor="w", padx=10)
        
        entry_nome = ctk.CTkEntry(frame_principal, width=400, placeholder_text="Ex: Disjuntor Trifásico 32A")
        entry_nome.pack(pady=(0, 10), padx=10)
        

        
        # Descrição
        label_descricao = ctk.CTkLabel(frame_principal, text="Descrição:", font=("Arial", 12, "bold"))
        label_descricao.pack(pady=(10, 5), anchor="w", padx=10)
        
        textbox_descricao = ctk.CTkTextbox(frame_principal, width=400, height=80)
        textbox_descricao.pack(pady=(0, 10), padx=10)
        
        # Regras derivadas
        label_regras = ctk.CTkLabel(frame_principal, text="Componentes Derivados (Regras):", font=("Arial", 12, "bold"))
        label_regras.pack(pady=(10, 5), anchor="w", padx=10)
        
        # Frame para regras
        frame_regras = ctk.CTkFrame(frame_principal)
        frame_regras.pack(pady=(0, 10), padx=10, fill="x")
        
        # Lista de regras
        self.regras_atuais = []
        scrollable_regras = ctk.CTkScrollableFrame(frame_regras, height=150)
        scrollable_regras.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame para adicionar regra
        frame_add_regra = ctk.CTkFrame(frame_regras)
        frame_add_regra.pack(fill="x", padx=5, pady=5)
        
        entry_regra_nome = ctk.CTkEntry(frame_add_regra, placeholder_text="Nome do componente derivado", width=250)
        entry_regra_nome.pack(side="left", padx=5)
        
        entry_regra_qtd = ctk.CTkEntry(frame_add_regra, placeholder_text="Qtd", width=60)
        entry_regra_qtd.pack(side="left", padx=5)
        
        btn_add_regra = ctk.CTkButton(
            frame_add_regra, 
            text="➕", 
            width=30,
            command=lambda: self.adicionar_regra_dialog(scrollable_regras, entry_regra_nome, entry_regra_qtd)
        )
        btn_add_regra.pack(side="left", padx=5)
        
        # Preencher campos se for edição
        if eh_edicao:
            entry_nome.insert(0, comp_info.nome)
            textbox_descricao.insert("1.0", comp_info.descricao)
            self.regras_atuais = comp_info.regras_derivadas.copy()
            self.atualizar_lista_regras_dialog(scrollable_regras)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(dialog)
        frame_botoes.pack(pady=20, fill="x", padx=20)
        
        # Botão salvar
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="💾 Salvar",
            command=lambda: self.salvar_componente_dialog(
                dialog, entry_nome, textbox_descricao, eh_edicao
            ),
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_salvar.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=dialog.destroy,
            fg_color="red",
            hover_color="darkred"
        )
        btn_cancelar.pack(side="right", fill="x", expand=True, padx=5)
        
        # Armazenar referências para uso nos callbacks
        self.dialog_scrollable_regras = scrollable_regras

    def adicionar_regra_dialog(self, scrollable_regras, entry_nome, entry_qtd):
        """Adiciona uma regra derivada no dialog"""
        nome = entry_nome.get().strip()
        qtd_str = entry_qtd.get().strip()
        
        if not nome or not qtd_str:
            messagebox.showwarning("Aviso", "Preencha nome e quantidade da regra.")
            return
        
        try:
            quantidade = int(qtd_str)
            if quantidade <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade deve ser um número inteiro positivo.")
            return
        
        # Adicionar à lista
        self.regras_atuais.append({"nome": nome, "quantidade": quantidade})
        
        # Limpar campos
        entry_nome.delete(0, "end")
        entry_qtd.delete(0, "end")
        
        # Atualizar lista visual
        self.atualizar_lista_regras_dialog(scrollable_regras)

    def atualizar_lista_regras_dialog(self, scrollable_regras):
        """Atualiza a lista visual de regras no dialog"""
        # Limpar lista
        for widget in scrollable_regras.winfo_children():
            widget.destroy()
        
        if not self.regras_atuais:
            label_vazio = ctk.CTkLabel(scrollable_regras, text="Nenhuma regra adicionada", font=("Arial", 10, "italic"))
            label_vazio.pack(pady=10)
            return
        
        # Adicionar cada regra
        for i, regra in enumerate(self.regras_atuais):
            frame_regra = ctk.CTkFrame(scrollable_regras)
            frame_regra.pack(fill="x", padx=5, pady=2)
            
            label_regra = ctk.CTkLabel(
                frame_regra,
                text=f"{regra['quantidade']}x {regra['nome']}",
                anchor="w"
            )
            label_regra.pack(side="left", padx=10, pady=5, fill="x", expand=True)
            
            btn_remover = ctk.CTkButton(
                frame_regra,
                text="🗑️",
                width=30,
                height=25,
                fg_color="red",
                hover_color="darkred",
                command=lambda idx=i: self.remover_regra_dialog(idx, scrollable_regras)
            )
            btn_remover.pack(side="right", padx=5, pady=5)

    def remover_regra_dialog(self, indice, scrollable_regras):
        """Remove uma regra do dialog"""
        if 0 <= indice < len(self.regras_atuais):
            self.regras_atuais.pop(indice)
            self.atualizar_lista_regras_dialog(scrollable_regras)

    def salvar_componente_dialog(self, dialog, entry_nome, textbox_descricao, eh_edicao):
        """Salva o componente do dialog"""
        nome = entry_nome.get().strip()
        descricao = textbox_descricao.get("1.0", "end").strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do componente.")
            return
        
        # Criar objeto ComponenteInfo
        comp_info = ComponenteInfo(
            nome=nome,
            descricao=descricao,
            regras_derivadas=self.regras_atuais.copy()
        )
        
        try:
            # Salvar componente
            componentes_manager.salvar_componente_info(comp_info)
            
            # Fechar dialog
            dialog.destroy()
            
            # Atualizar lista
            self.atualizar_lista_visual()
            
            acao = "editado" if eh_edicao else "criado"
            messagebox.showinfo("Sucesso", f"Componente '{nome}' {acao} com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar componente: {str(e)}")

    def voltar_inicio(self):
        """Volta para a tela inicial"""
        self.janela_principal.voltar_inicio() 
import customtkinter as ctk
from core.models import Painel
from core import file_manager
import tkinter.messagebox as messagebox
import threading

class TelaPaineis(ctk.CTkFrame):
    def __init__(self, master, janela_principal, orcamento, caminho_arquivo):
        super().__init__(master)
        self.janela_principal = janela_principal
        self.orcamento = orcamento
        self.caminho_arquivo = caminho_arquivo

        # Título da tela
        self.label_titulo = ctk.CTkLabel(
            self, 
            text=f"Painéis do Orçamento: {orcamento.nome}", 
            font=("Arial", 20, "bold")
        )
        self.label_titulo.pack(pady=20)

        # Botão voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="⬅️ Voltar aos Orçamentos",
            command=self.voltar_orcamentos,
            height=30
        )
        self.btn_voltar.pack(pady=10, padx=20, anchor="w")

        # Frame para busca
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(pady=10, padx=20, fill="x")

        self.label_busca = ctk.CTkLabel(
            self.frame_busca, 
            text="🔍 Procurar painel:", 
            font=("Arial", 14)
        )
        self.label_busca.pack(side="left", padx=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Digite para filtrar painéis...",
            width=300
        )
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_paineis)

        self.btn_limpar_busca = ctk.CTkButton(
            self.frame_busca,
            text="✖️ Limpar",
            command=self.limpar_busca,
            width=80,
            height=30
        )
        self.btn_limpar_busca.pack(side="left", padx=5)

        # Botão adicionar painel na área de busca
        self.btn_adicionar_topo = ctk.CTkButton(
            self.frame_busca,
            text="➕ Novo Painel",
            command=self.adicionar_painel,
            width=120,
            height=30,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_adicionar_topo.pack(side="right", padx=10)

        # Frame para lista de painéis
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista, 
            text="Painéis disponíveis:", 
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=10)

        # ScrollableFrame para lista de painéis
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista, height=250)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Variável para armazenar painel selecionado
        self.painel_selecionado = None

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=20, padx=20, fill="x")

        # Botões de ação
        self.btn_adicionar = ctk.CTkButton(
            self.frame_botoes, 
            text="➕ Novo Painel", 
            command=self.adicionar_painel,
            height=40
        )
        self.btn_adicionar.pack(pady=5, padx=10, fill="x")

        self.btn_abrir = ctk.CTkButton(
            self.frame_botoes, 
            text="📂 Abrir Painel", 
            command=self.abrir_painel,
            height=40
        )
        self.btn_abrir.pack(pady=5, padx=10, fill="x")



        self.btn_excluir = ctk.CTkButton(
            self.frame_botoes, 
            text="🗑️ Excluir Painel", 
            command=self.excluir_painel,
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        self.btn_excluir.pack(pady=5, padx=10, fill="x")

        self.btn_salvar = ctk.CTkButton(
            self.frame_botoes, 
            text="💾 Salvar Alterações", 
            command=self.salvar,
            fg_color="green",
            hover_color="darkgreen",
            height=40
        )
        self.btn_salvar.pack(pady=5, padx=10, fill="x")

        # Atualizar breadcrumb no menu lateral
        self.janela_principal.limpar_breadcrumb()
        self.janela_principal.adicionar_breadcrumb(
            f"📋 {self.orcamento.nome}", 
            self.voltar_orcamentos
        )
        
        # Carregar lista inicial
        self.atualizar_lista_visual()

    def get_lista_nomes(self):
        """Retorna lista com nomes dos painéis"""
        return [painel.nome for painel in self.orcamento.paineis] if self.orcamento.paineis else []

    def atualizar_lista_visual(self, filtro=""):
        """Atualiza a lista visual de painéis"""
        # Limpar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.painel_selecionado = None
        
        lista_completa = self.get_lista_nomes()
        
        # Aplicar filtro se fornecido
        if filtro:
            lista_filtrada = [nome for nome in lista_completa if filtro.lower() in nome.lower()]
        else:
            lista_filtrada = lista_completa
        
        if not lista_filtrada:
            label_vazio = ctk.CTkLabel(
                self.scrollable_frame,
                text="Nenhum painel encontrado." if not filtro else f"Nenhum resultado para '{filtro}'.",
                font=("Arial", 12, "italic"),
                text_color="gray"
            )
            label_vazio.pack(pady=20)
            return
        
        # Criar item para cada painel
        for nome_painel in lista_filtrada:
            self.criar_item_painel(nome_painel)

    def criar_item_painel(self, nome_painel):
        """Cria um item visual para um painel na lista"""
        # Obter informações do painel
        painel = self.orcamento.obter_painel(nome_painel)
        num_componentes = len(painel.componentes) if painel else 0
        
        # Frame do item
        frame_item = ctk.CTkFrame(self.scrollable_frame)
        frame_item.pack(fill="x", padx=5, pady=3)
        
        # Botão principal (nome do painel) - clicável para selecionar
        texto_painel = f"⚡ {nome_painel}"
        if painel:
            texto_painel += f" ({painel.tipo}) - {num_componentes} componentes"
        
        btn_nome = ctk.CTkButton(
            frame_item,
            text=texto_painel,
            anchor="w",
            height=40,
            font=("Arial", 12)
        )
        btn_nome.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Implementar detecção de duplo clique
        btn_nome._click_count = 0
        btn_nome._timer = None
        
        def handle_click():
            btn_nome._click_count += 1
            
            if btn_nome._timer:
                btn_nome._timer.cancel()
            
            def process_click():
                if btn_nome._click_count == 1:
                    # Clique simples - selecionar
                    self.selecionar_painel(nome_painel)
                elif btn_nome._click_count >= 2:
                    # Duplo clique - abrir
                    self.abrir_painel_por_nome(nome_painel)
                
                btn_nome._click_count = 0
            
            btn_nome._timer = threading.Timer(0.3, process_click)  # 300ms de espera
            btn_nome._timer.start()
        
        btn_nome.configure(command=handle_click)
        

        
        # Frame para botões de ação
        frame_acoes = ctk.CTkFrame(frame_item)
        frame_acoes.pack(side="right", padx=5, pady=5)
        
        # Botão abrir
        btn_abrir = ctk.CTkButton(
            frame_acoes,
            text="📂",
            command=lambda nome=nome_painel: self.abrir_painel_por_nome(nome),
            width=40,
            height=30,
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_abrir.pack(side="left", padx=2)
        
        # Botão renomear
        btn_renomear = ctk.CTkButton(
            frame_acoes,
            text="✏️",
            command=lambda nome=nome_painel: self.renomear_painel_por_nome(nome),
            width=40,
            height=30,
            fg_color="orange",
            hover_color="darkorange"
        )
        btn_renomear.pack(side="left", padx=2)
        
        # Botão excluir
        btn_excluir = ctk.CTkButton(
            frame_acoes,
            text="🗑️",
            command=lambda nome=nome_painel: self.excluir_painel_por_nome(nome),
            width=40,
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        btn_excluir.pack(side="left", padx=2)

    def selecionar_painel(self, nome_painel):
        """Seleciona um painel (destaca visualmente)"""
        self.painel_selecionado = nome_painel
        
        # Redesenhar lista para destacar selecionado
        filtro_atual = self.entry_busca.get()
        self.atualizar_lista_visual(filtro_atual)
        
        # Destacar o selecionado
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and nome_painel in child.cget("text"):
                        child.configure(fg_color="orange", hover_color="darkorange")

    def filtrar_paineis(self, event=None):
        """Filtra painéis conforme o texto digitado"""
        filtro = self.entry_busca.get()
        self.atualizar_lista_visual(filtro)

    def limpar_busca(self):
        """Limpa o filtro de busca"""
        self.entry_busca.delete(0, "end")
        self.atualizar_lista_visual()

    def atualizar_lista(self):
        """Atualiza a lista de painéis (método mantido para compatibilidade)"""
        self.atualizar_lista_visual()

    def adicionar_painel(self):
        """Adiciona um novo painel ao orçamento"""
        # Dialog para nome do painel
        dialog = ctk.CTkInputDialog(
            text="Digite o nome do novo painel:",
            title="Novo Painel"
        )
        nome = dialog.get_input()
        
        if nome and nome.strip():
            nome = nome.strip()
            
            # Verificar se já existe painel com esse nome
            if any(p.nome == nome for p in self.orcamento.paineis):
                messagebox.showwarning("Aviso", f"Já existe um painel com o nome '{nome}'.")
                return
            
            # Criar janela personalizada para seleção do tipo
            self.mostrar_dialog_tipo_painel(nome)

    def mostrar_dialog_tipo_painel(self, nome_painel):
        """Mostra dialog personalizado para seleção do tipo de painel"""
        # Tipos de painéis disponíveis
        tipos_disponiveis = ["QDF/QDL"]  # Futuramente: ["QDF/QDL", "CCM", "QDG", "QGBT", etc.]
        
        # Criar janela toplevel
        dialog = ctk.CTkToplevel(self)
        dialog.title("Tipo do Painel")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Centralizar na tela
        dialog.transient(self)
        dialog.grab_set()
        
        # Label de instrução
        label = ctk.CTkLabel(
            dialog,
            text=f"Selecione o tipo do painel:\n'{nome_painel}'",
            font=("Arial", 14)
        )
        label.pack(pady=20)
        
        # Dropdown para tipo
        self.tipo_selecionado = ctk.CTkOptionMenu(
            dialog,
            values=tipos_disponiveis,
            width=200
        )
        self.tipo_selecionado.set(tipos_disponiveis[0])  # Selecionar o primeiro por padrão
        self.tipo_selecionado.pack(pady=10)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(dialog)
        frame_botoes.pack(pady=20, fill="x", padx=20)
        
        # Botão confirmar
        btn_confirmar = ctk.CTkButton(
            frame_botoes,
            text="✅ Confirmar",
            command=lambda: self.confirmar_adicao_painel(dialog, nome_painel),
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_confirmar.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=dialog.destroy,
            fg_color="red",
            hover_color="darkred"
        )
        btn_cancelar.pack(side="right", fill="x", expand=True, padx=5)

    def confirmar_adicao_painel(self, dialog, nome_painel):
        """Confirma a adição do painel com o tipo selecionado"""
        tipo_selecionado = self.tipo_selecionado.get()
        
        # Fechar dialog atual
        dialog.destroy()
        
        # Se for QDF/QDL, mostrar dialog de subtipo
        if tipo_selecionado == "QDF/QDL":
            self.mostrar_dialog_subtipo_painel(nome_painel, tipo_selecionado)
        else:
            # Para outros tipos (futuros), criar painel diretamente
            self.criar_painel_final(nome_painel, tipo_selecionado, "")

    def mostrar_dialog_subtipo_painel(self, nome_painel, tipo_principal):
        """Mostra dialog para seleção de subtipo do painel QDF/QDL"""
        # Subtipos disponíveis para QDF/QDL
        subtipos_disponiveis = ["Espinha Completa", "Meia Espinha", "Cabeado"]
        
        # Criar janela toplevel
        dialog = ctk.CTkToplevel(self)
        dialog.title("Subtipo do Painel")
        dialog.geometry("350x220")
        dialog.resizable(False, False)
        
        # Centralizar na tela
        dialog.transient(self)
        dialog.grab_set()
        
        # Label de instrução
        label = ctk.CTkLabel(
            dialog,
            text=f"Selecione o subtipo do painel:\n'{nome_painel}' ({tipo_principal})",
            font=("Arial", 14)
        )
        label.pack(pady=20)
        
        # Dropdown para subtipo
        self.subtipo_selecionado = ctk.CTkOptionMenu(
            dialog,
            values=subtipos_disponiveis,
            width=250
        )
        self.subtipo_selecionado.set("Espinha Completa")  # Padrão conforme solicitado
        self.subtipo_selecionado.pack(pady=10)
        
        # Label informativo
        info_label = ctk.CTkLabel(
            dialog,
            text="💡 Por enquanto, apenas 'Espinha Completa' está implementado",
            font=("Arial", 10),
            text_color="orange"
        )
        info_label.pack(pady=5)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(dialog)
        frame_botoes.pack(pady=20, fill="x", padx=20)
        
        # Botão confirmar
        btn_confirmar = ctk.CTkButton(
            frame_botoes,
            text="✅ Confirmar",
            command=lambda: self.confirmar_subtipo_painel(dialog, nome_painel, tipo_principal),
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_confirmar.pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=dialog.destroy,
            fg_color="red",
            hover_color="darkred"
        )
        btn_cancelar.pack(side="right", fill="x", expand=True, padx=5)

    def confirmar_subtipo_painel(self, dialog, nome_painel, tipo_principal):
        """Confirma a adição do painel com tipo e subtipo selecionados"""
        subtipo_selecionado = self.subtipo_selecionado.get()
        
        # Fechar dialog
        dialog.destroy()
        
        # Criar painel com tipo completo
        self.criar_painel_final(nome_painel, tipo_principal, subtipo_selecionado)

    def criar_painel_final(self, nome_painel, tipo_principal, subtipo):
        """Cria o painel final com tipo e subtipo"""
        # Montar tipo completo
        if subtipo:
            tipo_completo = f"{tipo_principal} - {subtipo}"
        else:
            tipo_completo = tipo_principal
        
        # Criar e adicionar o painel
        novo_painel = Painel(nome=nome_painel, tipo=tipo_completo)
        self.orcamento.adicionar_painel(novo_painel)
        
        # Salvar automaticamente no arquivo
        try:
            file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar painel: {str(e)}")
            return
        
        # Atualizar interface
        self.atualizar_lista_visual()
        messagebox.showinfo("Sucesso", f"Painel '{nome_painel}' ({tipo_completo}) adicionado e salvo com sucesso!")

    def excluir_painel(self):
        """Exclui o painel selecionado"""
        if not self.painel_selecionado:
            messagebox.showwarning("Aviso", "Selecione um painel para excluir.")
            return
        
        self.excluir_painel_por_nome(self.painel_selecionado)

    def excluir_painel_por_nome(self, nome_painel):
        """Exclui um painel específico pelo nome"""
        # Confirmar exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o painel '{nome_painel}'?\n\nTodos os componentes do painel serão perdidos."
        )
        
        if resposta:
            self.orcamento.remover_painel(nome_painel)
            
            # Salvar automaticamente no arquivo
            try:
                file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
                self.atualizar_lista_visual()
                messagebox.showinfo("Sucesso", "Painel excluído e salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar exclusão: {str(e)}")



    def renomear_painel_por_nome(self, nome_painel):
        """Renomeia um painel específico pelo nome"""
        try:
            # Encontrar o painel
            painel = self.orcamento.obter_painel(nome_painel)
            if not painel:
                messagebox.showerror("Erro", "Painel não encontrado.")
                return
            
            # Dialog para novo nome
            dialog = ctk.CTkInputDialog(
                text=f"Novo nome para o painel:",
                title="Renomear Painel"
            )
            novo_nome = dialog.get_input()
            
            if novo_nome is None or not novo_nome.strip():  # Usuário cancelou ou não digitou nada
                return
            
            novo_nome = novo_nome.strip()
            
            # Verificar se o nome mudou
            if novo_nome == painel.nome:
                messagebox.showinfo("Aviso", "O nome não foi alterado.")
                return
            
            # Verificar se já existe um painel com esse nome
            if self.orcamento.obter_painel(novo_nome):
                messagebox.showerror("Erro", f"Já existe um painel com o nome '{novo_nome}'.")
                return
            
            # Atualizar o nome do painel
            painel.nome = novo_nome
            
            # Salvar automaticamente no arquivo
            file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
            
            # Atualizar a lista visual
            self.atualizar_lista_visual()
            
            messagebox.showinfo("Sucesso", f"Painel renomeado para '{novo_nome}' com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao renomear painel: {str(e)}")

    def abrir_painel(self):
        """Abre o painel selecionado para edição de componentes"""
        if not self.painel_selecionado:
            messagebox.showwarning("Aviso", "Selecione um painel para abrir.")
            return
        
        self.abrir_painel_por_nome(self.painel_selecionado)

    def abrir_painel_por_nome(self, nome_painel):
        """Abre um painel específico pelo nome"""
        painel = self.orcamento.obter_painel(nome_painel)
        if painel:
            # Navegar para tela de componentes
            from ui.tela_componentes import TelaComponentes
            
            for widget in self.master.winfo_children():
                widget.destroy()

            tela_componentes = TelaComponentes(
                self.master, 
                self.janela_principal, 
                painel, 
                self.orcamento, 
                self.caminho_arquivo
            )
            tela_componentes.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Erro", "Painel não encontrado.")

    def salvar(self):
        """Salva as alterações no arquivo de orçamento"""
        try:
            file_manager.salvar_orcamento(self.orcamento, self.caminho_arquivo)
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")



    def voltar_orcamentos(self):
        """Volta para a tela de orçamentos"""
        self.janela_principal.voltar_inicio() 
import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ORCPAI – Orçamento de Painéis")
        
        # Configurar janela sempre maximizada
        self.state('zoomed')  # Maximizar no Windows
        
        # Desabilitar redimensionamento
        self.resizable(False, False)
        
        # Configurar protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Garantir que a janela permaneça maximizada
        self.bind('<Configure>', self.on_configure)

        # Frame de menu lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        # Frame principal (área de troca de telas)
        self.area_principal = ctk.CTkFrame(self)
        self.area_principal.pack(side="right", fill="both", expand=True)

        # Título do menu
        self.titulo_menu = ctk.CTkLabel(
            self.menu_lateral, 
            text="ORCPAI", 
            font=("Arial", 18, "bold")
        )
        self.titulo_menu.pack(pady=20)

        # Botão para abrir a tela de orçamentos
        self.btn_orcamentos = ctk.CTkButton(
            self.menu_lateral, 
            text="📋 Orçamentos", 
            command=self.abrir_tela_orcamentos,
            height=40
        )
        self.btn_orcamentos.pack(padx=20, pady=10, fill="x")
        
        # Frame para breadcrumb (inicialmente vazio)
        self.frame_breadcrumb = ctk.CTkFrame(self.menu_lateral)
        self.frame_breadcrumb.pack(padx=20, pady=10, fill="x")
        self.frame_breadcrumb.pack_forget()  # Inicialmente oculto
        
        # Variáveis para controlar o breadcrumb
        self.breadcrumb_buttons = []

        # Bind para atalho administrativo (Ctrl+Alt+A)
        self.bind_all("<Control-Alt-a>", self.abrir_admin)

        # Inicia com a tela de orçamentos carregada
        self.abrir_tela_orcamentos()

    def abrir_tela_orcamentos(self):
        """Abre a tela de listagem de orçamentos"""
        from ui.tela_orcamentos import TelaOrcamentos

        # Limpa a área principal
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        # Carrega a nova tela
        tela = TelaOrcamentos(self.area_principal, self)
        tela.pack(fill="both", expand=True)

    def abrir_admin(self, event=None):
        """Abre a tela administrativa (atalho secreto Ctrl+Alt+A)"""
        from ui.tela_admin import TelaAdmin
        
        # Limpa a área principal
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        
        # Carrega a tela admin
        tela = TelaAdmin(self.area_principal, self)
        tela.pack(fill="both", expand=True)

    def adicionar_breadcrumb(self, texto, comando=None):
        """Adiciona um item ao breadcrumb"""
        # Mostrar o frame se estiver oculto
        self.frame_breadcrumb.pack(padx=20, pady=10, fill="x", after=self.btn_orcamentos)
        
        # Criar botão para o breadcrumb
        btn = ctk.CTkButton(
            self.frame_breadcrumb,
            text=texto,
            command=comando if comando else lambda: None,
            height=30,
            fg_color="gray70",
            hover_color="gray60",
            font=("Arial", 11)
        )
        btn.pack(padx=5, pady=2, fill="x")
        
        # Armazenar referência
        self.breadcrumb_buttons.append(btn)

    def limpar_breadcrumb(self):
        """Remove todos os itens do breadcrumb"""
        for btn in self.breadcrumb_buttons:
            btn.destroy()
        self.breadcrumb_buttons.clear()
        self.frame_breadcrumb.pack_forget()

    def atualizar_breadcrumb_painel(self, nome_orcamento, nome_painel, comando_voltar_paineis):
        """Atualiza o breadcrumb para mostrar orçamento > painel"""
        self.limpar_breadcrumb()
        
        # Adicionar orçamento
        self.adicionar_breadcrumb(f"📋 {nome_orcamento}", comando_voltar_paineis)
        
        # Adicionar painel atual
        self.adicionar_breadcrumb(f"⚡ {nome_painel}")

    def on_configure(self, event):
        """Intercepta eventos de configuração da janela para mantê-la maximizada"""
        if event.widget == self:
            # Se a janela não estiver maximizada, força maximização
            if self.state() != 'zoomed':
                self.state('zoomed')

    def on_closing(self):
        """Controla o fechamento da aplicação"""
        self.quit()
        self.destroy()

    def voltar_inicio(self):
        """Volta para a tela inicial de orçamentos"""
        self.limpar_breadcrumb()
        self.abrir_tela_orcamentos() 
import customtkinter as ctk
from core import file_manager
from core.models import Orcamento
import os
from datetime import datetime
import tkinter.messagebox as messagebox
import threading

class TelaOrcamentos(ctk.CTkFrame):
    def __init__(self, master, janela_principal):
        super().__init__(master)
        self.janela_principal = janela_principal

        # Título da tela
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="Gerenciamento de Orçamentos", 
            font=("Arial", 20, "bold")
        )
        self.label_titulo.pack(pady=20)

        # Frame para busca
        self.frame_busca = ctk.CTkFrame(self)
        self.frame_busca.pack(pady=10, padx=20, fill="x")

        self.label_busca = ctk.CTkLabel(
            self.frame_busca, 
            text="🔍 Procurar orçamento:", 
            font=("Arial", 14)
        )
        self.label_busca.pack(side="left", padx=10)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Digite para filtrar orçamentos...",
            width=300
        )
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_orcamentos)

        self.btn_limpar_busca = ctk.CTkButton(
            self.frame_busca,
            text="✖️ Limpar",
            command=self.limpar_busca,
            width=80,
            height=30
        )
        self.btn_limpar_busca.pack(side="left", padx=5)

        # Frame para lista de arquivos
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_lista = ctk.CTkLabel(
            self.frame_lista, 
            text="Orçamentos disponíveis:", 
            font=("Arial", 14, "bold")
        )
        self.label_lista.pack(pady=10)

        # ScrollableFrame para lista de orçamentos
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame_lista, height=250)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Variável para armazenar orçamento selecionado
        self.orcamento_selecionado = None

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=20, padx=20, fill="x")

        # Botões de ação
        self.btn_adicionar = ctk.CTkButton(
            self.frame_botoes, 
            text="➕ Novo Orçamento", 
            command=self.adicionar_orcamento,
            height=40
        )
        self.btn_adicionar.pack(pady=5, padx=10, fill="x")

        self.btn_abrir = ctk.CTkButton(
            self.frame_botoes, 
            text="📂 Abrir Orçamento", 
            command=self.abrir_orcamento,
            height=40
        )
        self.btn_abrir.pack(pady=5, padx=10, fill="x")



        self.btn_excluir = ctk.CTkButton(
            self.frame_botoes, 
            text="🗑️ Excluir Orçamento", 
            command=self.excluir_orcamento,
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        self.btn_excluir.pack(pady=5, padx=10, fill="x")

        self.btn_exportar = ctk.CTkButton(
            self.frame_botoes, 
            text="📊 Exportar para Excel", 
            command=self.exportar_excel,
            height=40
        )
        self.btn_exportar.pack(pady=5, padx=10, fill="x")

        # Carregar lista inicial
        self.atualizar_lista_visual()

    def carregar_lista(self):
        """Carrega a lista de orçamentos disponíveis com seus nomes reais"""
        arquivos = file_manager.listar_arquivos_orcamentos()
        orcamentos_info = []
        
        for arquivo in arquivos:
            try:
                # Carregar o orçamento para obter o nome real
                orcamento = file_manager.carregar_orcamento(arquivo)
                nome_arquivo = file_manager.obter_nome_arquivo_sem_extensao(arquivo)
                orcamentos_info.append({
                    'nome_exibicao': orcamento.nome,
                    'nome_arquivo': nome_arquivo,
                    'data': orcamento.data
                })
            except Exception:
                # Se houver erro ao carregar, usar o nome do arquivo
                nome_arquivo = file_manager.obter_nome_arquivo_sem_extensao(arquivo)
                orcamentos_info.append({
                    'nome_exibicao': nome_arquivo,
                    'nome_arquivo': nome_arquivo,
                    'data': 'N/A'
                })
        
        return orcamentos_info

    def atualizar_lista_visual(self, filtro=""):
        """Atualiza a lista visual de orçamentos"""
        # Limpar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.orcamento_selecionado = None
        
        lista_completa = self.carregar_lista()
        
        # Aplicar filtro se fornecido
        if filtro:
            lista_filtrada = [info for info in lista_completa if filtro.lower() in info['nome_exibicao'].lower()]
        else:
            lista_filtrada = lista_completa
        
        if not lista_filtrada:
            label_vazio = ctk.CTkLabel(
                self.scrollable_frame,
                text="Nenhum orçamento encontrado." if not filtro else f"Nenhum resultado para '{filtro}'.",
                font=("Arial", 12, "italic"),
                text_color="gray"
            )
            label_vazio.pack(pady=20)
            return
        
        # Criar item para cada orçamento
        for info_orcamento in lista_filtrada:
            self.criar_item_orcamento(info_orcamento)

    def criar_item_orcamento(self, info_orcamento):
        """Cria um item visual para um orçamento na lista"""
        nome_exibicao = info_orcamento['nome_exibicao']
        nome_arquivo = info_orcamento['nome_arquivo']
        data = info_orcamento['data']
        
        # Frame do item
        frame_item = ctk.CTkFrame(self.scrollable_frame)
        frame_item.pack(fill="x", padx=5, pady=3)
        
        # Botão principal (nome do orçamento) - clicável para selecionar, duplo clique para abrir
        texto_botao = f"📋 {nome_exibicao}"
        if data != 'N/A':
            texto_botao += f" ({data})"
            
        btn_nome = ctk.CTkButton(
            frame_item,
            text=texto_botao,
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
                    self.selecionar_orcamento(nome_arquivo)
                elif btn_nome._click_count >= 2:
                    # Duplo clique - abrir
                    self.abrir_orcamento_por_nome(nome_arquivo)
                
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
            command=lambda: self.abrir_orcamento_por_nome(nome_arquivo),
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
            command=lambda: self.renomear_orcamento_por_nome(nome_arquivo),
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
            command=lambda: self.excluir_orcamento_por_nome(nome_arquivo),
            width=40,
            height=30,
            fg_color="red",
            hover_color="darkred"
        )
        btn_excluir.pack(side="left", padx=2)

    def selecionar_orcamento(self, nome_arquivo):
        """Seleciona um orçamento (destaca visualmente)"""
        self.orcamento_selecionado = nome_arquivo
        
        # Redesenhar lista para destacar selecionado
        filtro_atual = self.entry_busca.get()
        self.atualizar_lista_visual(filtro_atual)
        
        # Destacar o selecionado
        self.destacar_item_selecionado(nome_arquivo)

    def destacar_item_selecionado(self, nome_arquivo_selecionado):
        """Destaca visualmente o item selecionado"""
        lista_atual = self.carregar_lista()
        
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and "📋" in child.cget("text"):
                        # Encontrar qual orçamento este botão representa
                        for info in lista_atual:
                            if info['nome_arquivo'] == nome_arquivo_selecionado:
                                if info['nome_exibicao'] in child.cget("text"):
                                    child.configure(fg_color="orange", hover_color="darkorange")
                                    return

    def filtrar_orcamentos(self, event=None):
        """Filtra orçamentos conforme o texto digitado"""
        filtro = self.entry_busca.get()
        self.atualizar_lista_visual(filtro)

    def limpar_busca(self):
        """Limpa o filtro de busca"""
        self.entry_busca.delete(0, "end")
        self.atualizar_lista_visual()

    def atualizar_lista(self):
        """Atualiza a lista de orçamentos (método mantido para compatibilidade)"""
        self.atualizar_lista_visual()

    def adicionar_orcamento(self):
        """Cria um novo orçamento"""
        # Dialog para nome do orçamento
        dialog = ctk.CTkInputDialog(
            text="Digite o nome do novo orçamento:",
            title="Novo Orçamento"
        )
        nome = dialog.get_input()
        
        if nome and nome.strip():
            nome = nome.strip()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"{nome}_{timestamp}"
            
            orcamento = Orcamento(nome=nome, data=datetime.now().strftime('%Y-%m-%d'))
            caminho = f"orcamentos/{nome_arquivo}.orcpai"
            
            try:
                file_manager.salvar_orcamento(orcamento, caminho)
                self.atualizar_lista_visual()
                messagebox.showinfo("Sucesso", f"Orçamento '{nome}' criado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar orçamento: {str(e)}")

    def excluir_orcamento(self):
        """Exclui o orçamento selecionado"""
        if not self.orcamento_selecionado:
            messagebox.showwarning("Aviso", "Selecione um orçamento para excluir.")
            return
        
        self.excluir_orcamento_por_nome(self.orcamento_selecionado)

    def excluir_orcamento_por_nome(self, nome_orcamento):
        """Exclui um orçamento específico pelo nome"""
        # Confirmar exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o orçamento '{nome_orcamento}'?\n\nEsta ação não pode ser desfeita."
        )
        
        if resposta:
            caminho = f"orcamentos/{nome_orcamento}.orcpai"
            if file_manager.excluir_orcamento(caminho):
                self.atualizar_lista_visual()
                messagebox.showinfo("Sucesso", "Orçamento excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao excluir o orçamento.")



    def renomear_orcamento_por_nome(self, nome_arquivo):
        """Renomeia um orçamento específico pelo nome do arquivo"""
        try:
            # Carregar o orçamento atual
            caminho_atual = f"orcamentos/{nome_arquivo}.orcpai"
            orcamento = file_manager.carregar_orcamento(caminho_atual)
            
            # Dialog para novo nome
            dialog = ctk.CTkInputDialog(
                text=f"Novo nome para o orçamento:",
                title="Renomear Orçamento"
            )
            novo_nome = dialog.get_input()
            
            if novo_nome is None or not novo_nome.strip():  # Usuário cancelou ou não digitou nada
                return
            
            novo_nome = novo_nome.strip()
            
            # Verificar se o nome mudou
            if novo_nome == orcamento.nome:
                messagebox.showinfo("Aviso", "O nome não foi alterado.")
                return
            
            # Atualizar o nome no objeto orçamento
            orcamento.nome = novo_nome
            
            # Salvar com o nome atualizado (mantém o mesmo arquivo)
            file_manager.salvar_orcamento(orcamento, caminho_atual)
            
            # Atualizar a lista visual
            self.atualizar_lista_visual()
            
            messagebox.showinfo("Sucesso", f"Orçamento renomeado para '{novo_nome}' com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao renomear orçamento: {str(e)}")

    def abrir_orcamento(self):
        """Abre o orçamento selecionado para edição"""
        if not self.orcamento_selecionado:
            messagebox.showwarning("Aviso", "Selecione um orçamento para abrir.")
            return
        
        self.abrir_orcamento_por_nome(self.orcamento_selecionado)

    def abrir_orcamento_por_nome(self, nome_orcamento):
        """Abre um orçamento específico pelo nome"""
        try:
            caminho = f"orcamentos/{nome_orcamento}.orcpai"
            orcamento = file_manager.carregar_orcamento(caminho)

            # Navegar para tela de painéis
            from ui.tela_paineis import TelaPaineis
            
            for widget in self.master.winfo_children():
                widget.destroy()

            TelaPaineis(self.master, self.janela_principal, orcamento, caminho).pack(fill="both", expand=True)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir orçamento: {str(e)}")

    def exportar_excel(self):
        """Exporta o orçamento selecionado para Excel"""
        if not self.orcamento_selecionado:
            messagebox.showwarning("Aviso", "Selecione um orçamento para exportar.")
            return
        
        try:
            from core.exportador_excel import exportar_orcamento_para_excel
            
            caminho = f"orcamentos/{self.orcamento_selecionado}.orcpai"
            orcamento = file_manager.carregar_orcamento(caminho)
            
            # Nome do arquivo Excel
            nome_excel = f"{self.orcamento_selecionado}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            exportar_orcamento_para_excel(orcamento, nome_excel)
            messagebox.showinfo("Sucesso", f"Orçamento exportado para: {nome_excel}")
            
        except ImportError:
            messagebox.showwarning("Aviso", "Funcionalidade de exportação ainda não implementada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")


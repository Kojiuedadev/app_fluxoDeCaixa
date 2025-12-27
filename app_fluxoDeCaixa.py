import customtkinter as ctk
from tkinter import messagebox
import datetime
import os
import zipfile
import platform

# Configurações de Cores Premium
COR_FUNDO = "#121212"
COR_CARD_VENDAS = "#1E1E1E"
COR_ENTRADA = "#2E7D32"
COR_SAIDA = "#C62828"
COR_DESTAQUE = "#3b8ed0"

class AppFluxoCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Agro & Construção Pro - v6.6")
        self.geometry("1200x950")
        self.configure(fg_color=COR_FUNDO)

        # --- ESTRUTURA DE PASTAS ORGANIZADA ---
        self.pasta_raiz = "Sistema_Caixa_KojiProg"
        self.pasta_dados = os.path.join(self.pasta_raiz, "Banco_de_Dados")
        self.pasta_relatorios = os.path.join(self.pasta_raiz, "Relatorios")
        self.pasta_backup = os.path.join(self.pasta_raiz, "Backups")

        # Criar pastas automaticamente
        for p in [self.pasta_dados, self.pasta_relatorios, self.pasta_backup]:
            if not os.path.exists(p): 
                os.makedirs(p)

        # Caminhos dos Arquivos
        self.arquivo = os.path.join(self.pasta_dados, "fluxo_caixa.csv")
        self.historico = os.path.join(self.pasta_dados, "historico_vendas.csv")

        self.verificar_troca_de_dia()
        self.fazer_backup_local()
        
        # --- UI: HEADER ---
        self.frame_topo = ctk.CTkFrame(self, fg_color="#1A1A1A", height=80, corner_radius=0)
        self.frame_topo.pack(fill="x", padx=0, pady=0)

        self.label_titulo = ctk.CTkLabel(self.frame_topo, text="  🛠️ AGRO & CONSTRUÇÃO PRO", 
                                       font=("Segoe UI", 24, "bold"), text_color=COR_DESTAQUE)
        self.label_titulo.pack(side="left", padx=30, pady=20)

        self.label_relogio = ctk.CTkLabel(self.frame_topo, text="", font=("JetBrains Mono", 16), text_color="#777777")
        self.label_relogio.pack(side="right", padx=30)
        self.atualizar_relogio()

        # --- UI: TABS ---
        self.tabview = ctk.CTkTabview(self, fg_color=COR_FUNDO, segmented_button_fg_color="#1A1A1A",
                                     segmented_button_selected_color=COR_DESTAQUE, corner_radius=15)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10,0))
        
        self.tab_hoje = self.tabview.add("  🏪 CAIXA DO DIA  ")
        self.tab_historico = self.tabview.add("  📂 HISTÓRICO COMPLETO  ")

        self.configurar_aba_hoje()
        self.configurar_aba_historico()

        # --- UI: FOOTER (ASSINATURA) ---
        self.frame_footer = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.frame_footer.pack(fill="x", side="bottom", padx=25, pady=5)
        
        self.label_assinatura = ctk.CTkLabel(self.frame_footer, 
                                            text="Desenvolvido por KojiProg © 2025", 
                                            font=("Segoe UI", 11, "italic"), 
                                            text_color="#444444")
        self.label_assinatura.pack(side="right")

        self.atualizar_tela()

    def atualizar_relogio(self):
        agora = datetime.datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
        self.label_relogio.configure(text=agora)
        self.after(1000, self.atualizar_relogio)

    def salvar(self, tipo):
        try:
            val_texto = self.input_valor.get().replace(",", ".")
            if not val_texto: return
            val = float(val_texto)
            
            if tipo == "SAÍDA": 
                val = -abs(val)
                desc_padrao = "Saída"
            else:
                val = abs(val)
                desc_padrao = "Venda"
            
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            desc = self.input_desc.get().strip() or desc_padrao
            
            with open(self.arquivo, "a") as f:
                f.write(f"{data};{tipo};{desc};{val};{self.metodo_var.get()}\n")
            
            self.input_valor.delete(0, 'end')
            self.input_valor.focus()
            self.atualizar_tela()
            self.fazer_backup_local()
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")

    def configurar_aba_hoje(self):
        # Cards
        self.frame_cards = ctk.CTkFrame(self.tab_hoje, fg_color="transparent")
        self.frame_cards.pack(pady=10, fill="x")
        self.card_mensal = self.criar_card(self.frame_cards, "FATURAMENTO MÊS", "R$ 0,00", "#7B1FA2")
        self.card_entradas = self.criar_card(self.frame_cards, "ENTRADAS HOJE", "R$ 0,00", COR_ENTRADA)
        self.card_gastos = self.criar_card(self.frame_cards, "SAÍDAS HOJE", "R$ 0,00", COR_SAIDA)
        self.card_saldo = self.criar_card(self.frame_cards, "SALDO ATUAL", "R$ 0,00", COR_DESTAQUE)

        # Meio
        self.corpo = ctk.CTkFrame(self.tab_hoje, fg_color="transparent")
        self.corpo.pack(fill="both", expand=True, pady=10)

        self.scroll_extrato = ctk.CTkScrollableFrame(self.corpo, fg_color="#181818", label_text="Lançamentos de Hoje")
        self.scroll_extrato.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Painel Lateral
        self.painel_metodos = ctk.CTkFrame(self.corpo, width=280, fg_color=COR_CARD_VENDAS, corner_radius=15)
        self.painel_metodos.pack(side="right", fill="y")
        ctk.CTkLabel(self.painel_metodos, text="FECHAMENTO POR TIPO", font=("Segoe UI", 14, "bold")).pack(pady=20)
        self.res_din = self.criar_linha_metodo(self.painel_metodos, "💵 DINHEIRO")
        self.res_pix = self.criar_linha_metodo(self.painel_metodos, "📱 PIX")
        self.res_deb = self.criar_linha_metodo(self.painel_metodos, "💳 DÉBITO")
        self.res_cre = self.criar_linha_metodo(self.painel_metodos, "💳 CRÉDITO")
        ctk.CTkButton(self.painel_metodos, text="📂 ABRIR BACKUPS", fg_color="#333333", command=self.abrir_pasta_backup).pack(pady=20, padx=20, fill="x")

        # Entrada de Dados
        self.frame_reg = ctk.CTkFrame(self.tab_hoje, fg_color=COR_CARD_VENDAS, corner_radius=15, border_width=1, border_color="#333333")
        self.frame_reg.pack(pady=10, fill="x")
        self.input_desc = ctk.CTkEntry(self.frame_reg, placeholder_text="Descrição...", height=45, fg_color="#121212")
        self.input_desc.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.input_valor = ctk.CTkEntry(self.frame_reg, placeholder_text="R$ 0,00", width=150, height=45, font=("Segoe UI", 18, "bold"), fg_color="#121212")
        self.input_valor.grid(row=0, column=1, padx=10, pady=20)
        self.input_valor.bind("<Return>", lambda event: self.salvar("ENTRADA"))

        self.metodo_var = ctk.StringVar(value="Dinheiro")
        self.combo_met = ctk.CTkComboBox(self.frame_reg, values=["Dinheiro", "PIX", "Débito", "Crédito"], variable=self.metodo_var, height=45)
        self.combo_met.grid(row=0, column=2, padx=10, pady=20)
        
        ctk.CTkButton(self.frame_reg, text="➕ ENTRADA", fg_color=COR_ENTRADA, font=("Segoe UI", 12, "bold"), command=lambda: self.salvar("ENTRADA")).grid(row=0, column=3, padx=10)
        ctk.CTkButton(self.frame_reg, text="➖ SAÍDA", fg_color=COR_SAIDA, font=("Segoe UI", 12, "bold"), command=lambda: self.salvar("SAÍDA")).grid(row=0, column=4, padx=20)
        self.frame_reg.grid_columnconfigure(0, weight=1)

    def criar_card(self, master, titulo, valor, cor_barra):
        f = ctk.CTkFrame(master, fg_color=COR_CARD_VENDAS, corner_radius=12, border_width=1, border_color="#333333")
        f.pack(side="left", padx=8, expand=True, fill="both")
        barra = ctk.CTkFrame(f, fg_color=cor_barra, width=4, height=40, corner_radius=10); barra.place(x=10, y=15)
        ctk.CTkLabel(f, text=titulo, font=("Segoe UI", 12, "bold"), text_color="#999999").pack(pady=(15,0), padx=(25,0), anchor="w")
        lbl = ctk.CTkLabel(f, text=valor, font=("Segoe UI", 22, "bold")); lbl.pack(pady=(0,15), padx=(25,0), anchor="w"); return lbl

    def criar_linha_metodo(self, master, texto):
        f = ctk.CTkFrame(master, fg_color="#252525", height=60); f.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(f, text=texto, font=("Segoe UI", 11)).pack(pady=(5,0))
        lbl = ctk.CTkLabel(f, text="R$ 0,00", font=("Segoe UI", 16, "bold"), text_color=COR_ENTRADA); lbl.pack(pady=(0,5)); return lbl

    def atualizar_tela(self):
        for w in self.scroll_extrato.winfo_children(): w.destroy()
        for w in self.scroll_hist.winfo_children(): w.destroy()
        t_hoje, e_hoje, s_hoje, e_mes = {"Dinheiro": 0.0, "PIX": 0.0, "Débito": 0.0, "Crédito": 0.0}, 0.0, 0.0, 0.0
        mes_atual = datetime.datetime.now().strftime("%m/%Y")

        if os.path.exists(self.historico):
            with open(self.historico, "r") as f:
                for l in reversed(f.readlines()):
                    p = l.strip().split(";")
                    if len(p) < 5: continue
                    if p[0][3:] == mes_atual and float(p[3]) > 0: e_mes += float(p[3])
                    row = ctk.CTkFrame(self.scroll_hist, fg_color="#222222"); row.pack(fill="x", pady=2, padx=5)
                    ctk.CTkLabel(row, text=f"📅 {p[0]} | {p[4]} | {p[2][:20]} | R$ {abs(float(p[3])):,.2f}").pack(side="left", padx=10)

        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                linhas = [l for l in f.readlines() if l.strip()]
                for i, l in enumerate(reversed(linhas)):
                    idx_real = len(linhas) - 1 - i
                    p = l.strip().split(";")
                    v = float(p[3]); met = p[4]
                    if v > 0: e_hoje += v; t_hoje[met] += v; e_mes += v
                    else: s_hoje += abs(v)
                    row = ctk.CTkFrame(self.scroll_extrato, fg_color="#222222", corner_radius=8); row.pack(fill="x", pady=4, padx=5)
                    ctk.CTkFrame(row, fg_color=COR_ENTRADA if v > 0 else COR_SAIDA, width=4, height=30).pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=f"{p[2][:25]}", font=("Segoe UI", 12)).pack(side="left", padx=20)
                    ctk.CTkButton(row, text="🗑️", width=30, fg_color="transparent", hover_color=COR_SAIDA, command=lambda idx=idx_real: self.excluir_item(idx)).pack(side="right", padx=5)
                    ctk.CTkButton(row, text="✏️", width=30, fg_color="transparent", hover_color=COR_DESTAQUE, command=lambda idx=idx_real, d=p[2], v=v, m=met: self.abrir_edicao(idx, d, v, m)).pack(side="right", padx=5)
                    ctk.CTkLabel(row, text=f"R$ {abs(v):,.2f}", font=("Segoe UI", 13, "bold"), text_color=COR_ENTRADA if v > 0 else COR_SAIDA).pack(side="right", padx=20)

        self.res_din.configure(text=f"R$ {t_hoje['Dinheiro']:,.2f}")
        self.res_pix.configure(text=f"R$ {t_hoje['PIX']:,.2f}")
        self.res_deb.configure(text=f"R$ {t_hoje['Débito']:,.2f}")
        self.res_cre.configure(text=f"R$ {t_hoje['Crédito']:,.2f}")
        self.card_entradas.configure(text=f"R$ {e_hoje:,.2f}"); self.card_gastos.configure(text=f"R$ {s_hoje:,.2f}")
        self.card_saldo.configure(text=f"R$ {e_hoje - s_hoje:,.2f}"); self.card_mensal.configure(text=f"R$ {e_mes:,.2f}")

    def excluir_item(self, index):
        if messagebox.askyesno("Confirmar", "🗑️ Apagar este registro?"):
            with open(self.arquivo, "r") as f: linhas = f.readlines()
            if index < len(linhas):
                del linhas[index]; open(self.arquivo, "w").writelines(linhas)
                self.atualizar_tela(); self.fazer_backup_local()

    def abrir_edicao(self, index, d, v, m):
        janela = ctk.CTkToplevel(self); janela.title("Editar"); janela.geometry("350x400"); janela.attributes("-topmost", True)
        ctk.CTkLabel(janela, text="Editar Detalhes", font=("Segoe UI", 16, "bold")).pack(pady=20)
        ed = ctk.CTkEntry(janela, width=250); ed.insert(0, d); ed.pack(pady=10)
        ev = ctk.CTkEntry(janela, width=250); ev.insert(0, str(abs(v))); ev.pack(pady=10)
        em = ctk.CTkComboBox(janela, values=["Dinheiro", "PIX", "Débito", "Crédito"], width=250); em.set(m); em.pack(pady=10)
        def salvar_edicao():
            with open(self.arquivo, "r") as f: linhas = f.readlines()
            try:
                nv = float(ev.get().replace(",", ".")); p = linhas[index].split(";")
                if "SAÍDA" in linhas[index]: nv = -nv
                linhas[index] = f"{p[0]};{p[1]};{ed.get()};{nv};{em.get()}\n"
                open(self.arquivo, "w").writelines(linhas); janela.destroy(); self.atualizar_tela(); self.fazer_backup_local()
            except: pass
        ctk.CTkButton(janela, text="Salvar", command=salvar_edicao).pack(pady=20)

    def configurar_aba_historico(self):
        self.scroll_hist = ctk.CTkScrollableFrame(self.tab_historico, fg_color="#121212", label_text="Registros Antigos")
        self.scroll_hist.pack(fill="both", expand=True, padx=10, pady=10)

    def abrir_pasta_backup(self):
        c = os.path.abspath(self.pasta_backup)
        if platform.system() == "Windows": os.startfile(c)
        else: messagebox.showinfo("Backup", f"Pasta: {c}")

    def fazer_backup_local(self):
        try:
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            nome = os.path.join(self.pasta_backup, f"backup_{ts}.zip")
            with zipfile.ZipFile(nome, 'w') as z:
                if os.path.exists(self.arquivo): z.write(self.arquivo)
                if os.path.exists(self.historico): z.write(self.historico)
            backups = sorted([os.path.join(self.pasta_backup, f) for f in os.listdir(self.pasta_backup)])
            if len(backups) > 10: os.remove(backups[0])
        except: pass

    def verificar_troca_de_dia(self):
        if not os.path.exists(self.arquivo): return
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        with open(self.arquivo, "r") as f:
            linhas = f.readlines()
            if not linhas or linhas[-1].split(";")[0] == hoje: return
            du = linhas[-1].split(";")[0]
            ent, sai = 0.0, 0.0
            for l in linhas:
                v = float(l.split(";")[3])
                if v > 0: ent += v
                else: sai += abs(v)
            with open(os.path.join(self.pasta_relatorios, f"Relatorio_{du.replace('/','-')}.txt"), "w") as r:
                r.write(f"DATA: {du}\nENTRADAS: {ent}\nSAIDAS: {sai}\nSALDO: {ent-sai}")
            with open(self.historico, "a") as h: h.writelines(linhas)
            open(self.arquivo, "w").write("")

if __name__ == "__main__":
    app = AppFluxoCaixa(); app.mainloop()
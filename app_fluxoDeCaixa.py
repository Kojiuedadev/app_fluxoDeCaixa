import customtkinter as ctk
from tkinter import messagebox
import datetime
import os
import shutil 
import zipfile
import platform # Adicionado para saber como abrir a pasta no Windows/Mac/Linux

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppFluxoCaixa(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Agro/Construção - Gestão de Caixa v5.6")
        self.geometry("1150x950") 
        self.arquivo = "fluxo_caixa.csv"
        self.historico = "historico_vendas.csv"
        self.pasta_relatorios = "Relatorios_Fechamento"
        self.pasta_backup = "Backup_Nuvem"

        for pasta in [self.pasta_relatorios, self.pasta_backup]:
            if not os.path.exists(pasta):
                os.makedirs(pasta)

        self.verificar_troca_de_dia()
        self.fazer_backup_local()

        self.label_titulo = ctk.CTkLabel(self, text="GESTÃO AGRO & CONSTRUÇÃO", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_hoje = self.tabview.add("CAIXA DO DIA (HOJE)")
        self.tab_historico = self.tabview.add("HISTÓRICO DE VENDAS")

        self.configurar_aba_hoje()
        self.configurar_aba_historico()
        self.atualizar_tela()

    def abrir_pasta_backup(self):
        """Abre a pasta de backups no explorador de arquivos do sistema."""
        caminho_absoluto = os.path.abspath(self.pasta_backup)
        if platform.system() == "Windows":
            os.startfile(caminho_absoluto)
        elif platform.system() == "Darwin": # Mac
            import subprocess
            subprocess.Popen(["open", caminho_absoluto])
        else: # Linux
            import subprocess
            subprocess.Popen(["xdg-open", caminho_absoluto])

    def fazer_backup_local(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            nome_backup = os.path.join(self.pasta_backup, f"backup_sistema_{timestamp}.zip")
            
            with zipfile.ZipFile(nome_backup, 'w') as zipf:
                if os.path.exists(self.arquivo): zipf.write(self.arquivo)
                if os.path.exists(self.historico): zipf.write(self.historico)
                if os.path.exists(self.pasta_relatorios):
                    for root, dirs, files in os.walk(self.pasta_relatorios):
                        for file in files:
                            zipf.write(os.path.join(root, file))
            
            backups = sorted([os.path.join(self.pasta_backup, f) for f in os.listdir(self.pasta_backup)])
            if len(backups) > 10: os.remove(backups[0])
        except Exception as e:
            print(f"Erro ao gerar backup: {e}")

    def configurar_aba_hoje(self):
        self.frame_cards = ctk.CTkFrame(self.tab_hoje, fg_color="transparent")
        self.frame_cards.pack(pady=10, fill="x")
        self.card_mensal = self.criar_card(self.frame_cards, "FATURAMENTO MENSAL", "R$ 0,00", "#5c3d91") 
        self.card_entradas = self.criar_card(self.frame_cards, "ENTRADAS HOJE", "R$ 0,00", "#2d8a4e")
        self.card_gastos = self.criar_card(self.frame_cards, "SAÍDAS HOJE", "R$ 0,00", "#a62d2d")
        self.card_saldo = self.criar_card(self.frame_cards, "SALDO DO DIA", "R$ 0,00", "#1f538d")

        self.cont_hoje = ctk.CTkFrame(self.tab_hoje, fg_color="transparent")
        self.cont_hoje.pack(fill="both", expand=True)

        self.scroll_extrato = ctk.CTkScrollableFrame(self.cont_hoje, height=350, label_text="VENDAS DE AGORA")
        self.scroll_extrato.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.frame_conf = ctk.CTkFrame(self.cont_hoje, width=250, border_width=2, border_color="#333333")
        self.frame_conf.pack(side="right", fill="y")
        
        ctk.CTkLabel(self.frame_conf, text="CONFERÊNCIA", font=("Roboto", 14, "bold")).pack(pady=10)
        self.res_din = self.criar_linha_resumo(self.frame_conf, "💵 DINHEIRO")
        self.res_pix = self.criar_linha_resumo(self.frame_conf, "📱 PIX")
        self.res_deb = self.criar_linha_resumo(self.frame_conf, "💳 DÉBITO")
        self.res_cre = self.criar_linha_resumo(self.frame_conf, "💳 CRÉDITO")

        # --- BOTÕES DE BACKUP ---
        ctk.CTkLabel(self.frame_conf, text="SEGURANÇA", font=("Roboto", 12, "bold"), text_color="gray").pack(pady=(20, 5))
        
        self.btn_pastabackup = ctk.CTkButton(self.frame_conf, text="📂 ABRIR PASTA ZIPS", 
                                             fg_color="#3d3d3d", hover_color="#575757",
                                             command=self.abrir_pasta_backup)
        self.btn_pastabackup.pack(pady=5, padx=10, fill="x")

        self.btn_backupmanual = ctk.CTkButton(self.frame_conf, text="🔄 GERAR BACKUP AGORA", 
                                             fg_color="#333333", command=self.fazer_backup_local)
        self.btn_backupmanual.pack(pady=5, padx=10, fill="x")

        self.frame_reg = ctk.CTkFrame(self.tab_hoje)
        self.frame_reg.pack(pady=15, fill="x")
        self.input_desc = ctk.CTkEntry(self.frame_reg, placeholder_text="Descrição..."); self.input_desc.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.input_valor = ctk.CTkEntry(self.frame_reg, placeholder_text="Valor R$"); self.input_valor.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.metodo_var = ctk.StringVar(value="Dinheiro")
        self.radio_f = ctk.CTkFrame(self.frame_reg, fg_color="transparent"); self.radio_f.grid(row=1, column=0, columnspan=3)
        for op in ["Dinheiro", "PIX", "Débito", "Crédito"]:
            ctk.CTkRadioButton(self.radio_f, text=op, variable=self.metodo_var, value=op).pack(side="left", padx=15)

        ctk.CTkButton(self.frame_reg, text="REGISTRAR ENTRADA", fg_color="#2d8a4e", height=40, command=lambda: self.salvar("ENTRADA")).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(self.frame_reg, text="REGISTRAR SAÍDA", fg_color="#a62d2d", height=40, command=lambda: self.salvar("SAÍDA")).grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        self.frame_reg.grid_columnconfigure((0,1,2), weight=1)

    def configurar_aba_historico(self):
        self.label_hist = ctk.CTkLabel(self.tab_historico, text="CONSULTA DE VENDAS ANTERIORES", font=("Roboto", 16, "bold"))
        self.label_hist.pack(pady=10)
        self.scroll_historico = ctk.CTkScrollableFrame(self.tab_historico, height=600, label_text="REGISTROS PASSADOS")
        self.scroll_historico.pack(fill="both", expand=True, padx=10, pady=10)

    def verificar_troca_de_dia(self):
        if not os.path.exists(self.arquivo): return
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        with open(self.arquivo, "r") as f:
            linhas = f.readlines()
            if not linhas: return
            data_ult = linhas[-1].split(";")[0]
        if data_ult != hoje:
            self.gerar_relatorio_fechamento(linhas, data_ult)
            with open(self.historico, "a") as h: h.writelines(linhas)
            with open(self.arquivo, "w") as f: f.write("") 

    def gerar_relatorio_fechamento(self, linhas, data):
        ent, sai = 0.0, 0.0
        for l in linhas:
            p = l.strip().split(";")
            if len(p) >= 4:
                v = float(p[3]); ent += v if v > 0 else 0; sai += abs(v) if v < 0 else 0
        with open(os.path.join(self.pasta_relatorios, f"Fechamento_{data.replace('/','-')}.txt"), "w") as f:
            f.write(f"Data: {data}\nEntradas: {ent}\nSaidas: {sai}\nSaldo: {ent-sai}")

    def criar_card(self, master, titulo, valor, cor):
        f = ctk.CTkFrame(master, fg_color=cor)
        f.pack(side="left", padx=5, expand=True, fill="both")
        ctk.CTkLabel(f, text=titulo, font=("Roboto", 10, "bold")).pack(pady=(10,0))
        lbl = ctk.CTkLabel(f, text=valor, font=("Roboto", 18, "bold")); lbl.pack(pady=(0,10)); return lbl

    def criar_linha_resumo(self, master, texto):
        f = ctk.CTkFrame(master, fg_color="#2b2b2b", corner_radius=8); f.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f, text=texto, font=("Roboto", 10)).pack()
        lbl = ctk.CTkLabel(f, text="R$ 0,00", font=("Roboto", 14, "bold"), text_color="#2d8a4e"); lbl.pack(pady=5); return lbl

    def salvar(self, tipo):
        try:
            val = float(self.input_valor.get().replace(",", "."))
            if tipo == "SAÍDA": val = -val
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            with open(self.arquivo, "a") as f:
                f.write(f"{data};{tipo};{self.input_desc.get() or 'Venda'};{val};{self.metodo_var.get()}\n")
            self.input_desc.delete(0, 'end'); self.input_valor.delete(0, 'end'); self.atualizar_tela()
            self.fazer_backup_local()
        except: pass

    def atualizar_tela(self):
        for w in self.scroll_extrato.winfo_children(): w.destroy()
        for w in self.scroll_historico.winfo_children(): w.destroy()
        t_hoje = {"Dinheiro": 0.0, "PIX": 0.0, "Débito": 0.0, "Crédito": 0.0}
        e_hoje, s_hoje, e_mes = 0.0, 0.0, 0.0
        mes_atual = datetime.datetime.now().strftime("%m/%Y")

        if os.path.exists(self.historico):
            with open(self.historico, "r") as f:
                linhas_h = f.readlines()
                for l in reversed(linhas_h):
                    p = l.strip().split(";")
                    if len(p) < 5: continue
                    if p[0][3:] == mes_atual and float(p[3]) > 0: e_mes += float(p[3])
                    row = ctk.CTkFrame(self.scroll_historico, fg_color="gray25")
                    row.pack(fill="x", pady=2, padx=5)
                    ctk.CTkLabel(row, text=f"{p[0]} | {p[4]:<8} | {p[2][:15]:<15} | R$ {abs(float(p[3])):.2f}", font=("Courier New", 12)).pack(side="left", padx=10)

        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                linhas = [l for l in f.readlines() if l.strip()]
                for i, l in enumerate(reversed(linhas)):
                    p = l.strip().split(";")
                    if len(p) < 5: continue
                    v = float(p[3]); met = p[4]
                    if v > 0: e_hoje += v; t_hoje[met] += v; e_mes += v
                    else: s_hoje += abs(v)
                    row = ctk.CTkFrame(self.scroll_extrato, fg_color="gray20" if i%2==0 else "gray25")
                    row.pack(fill="x", pady=2, padx=5)
                    ctk.CTkLabel(row, text=f"{p[4]:<8} | {p[2][:15]:<15} | R$ {abs(v):.2f}", 
                                 font=("Courier New", 12, "bold"), text_color="#2d8a4e" if v > 0 else "#ff5555").pack(side="left", padx=10)

        self.res_din.configure(text=f"R$ {t_hoje['Dinheiro']:,.2f}")
        self.res_pix.configure(text=f"R$ {t_hoje['PIX']:,.2f}")
        self.res_deb.configure(text=f"R$ {t_hoje['Débito']:,.2f}")
        self.res_cre.configure(text=f"R$ {t_hoje['Crédito']:,.2f}")
        self.card_mensal.configure(text=f"R$ {e_mes:,.2f}")
        self.card_entradas.configure(text=f"R$ {e_hoje:,.2f}")
        self.card_gastos.configure(text=f"R$ {s_hoje:,.2f}")
        self.card_saldo.configure(text=f"R$ {e_hoje - s_hoje:,.2f}")

if __name__ == "__main__":
    app = AppFluxoCaixa(); app.mainloop()
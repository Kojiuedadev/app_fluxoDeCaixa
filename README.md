📦 Sistema de Gestão Agro & Construção v5.6
Sistema leve e eficiente para controle de fluxo de caixa diário, faturamento mensal e backup automatizado em nuvem, desenvolvido especialmente para o varejo de materiais de construção e agropecuária.

🚀 Funcionalidades Principais
Caixa do Dia: Registro rápido de Entradas (Vendas) e Saídas (Pagamentos) com seleção de método (Dinheiro, PIX, Cartão).

Fechamento Diário Automático: Ao abrir o programa no dia seguinte, ele gera um relatório .txt detalhado e zera o caixa atual para um novo começo.

Histórico Integrado: Aba dedicada para consulta de todas as vendas de dias anteriores sem sair do programa.

Faturamento Mensal: Card em destaque que soma todas as vendas do mês corrente (Histórico + Hoje).

Backup em Nuvem: Gera automaticamente um arquivo .zip a cada registro feito. Se configurado com Google Drive ou OneDrive, seus dados ficam protegidos contra falhas no PC.

Conferência de Caixa: Resumo lateral por método de pagamento para facilitar a "batida" do caixa físico.

🛠️ Requisitos de Instalação
Para rodar este programa, você precisa ter o Python instalado no computador.

1. Instale o Python
Baixe a versão mais recente em python.org (marque a opção "Add Python to PATH" durante a instalação).

2. Instale as Bibliotecas Necessárias
Abra o seu terminal (CMD ou PowerShell) e digite os seguintes comandos:

Bash

pip install customtkinter
A biblioteca customtkinter é responsável pelo visual moderno e escuro do sistema.

📂 Como Estruturar as Pastas
O programa gerencia seus próprios arquivos, mas a estrutura final ficará assim:

app_fluxoDeCaixa.py (O código principal)

fluxo_caixa.csv (Vendas de hoje)

historico_vendas.csv (Vendas de dias passados)

Relatorios_Fechamento/ (Pasta com os resumos diários em .txt)

Backup_Nuvem/ (Pasta com os arquivos .zip de segurança)

☁️ Configurando o Backup em Nuvem (Recomendado)
Para que o backup seja realmente "em nuvem", siga estes passos:

Instale o Google Drive para Computador ou OneDrive.

Nas configurações do serviço de nuvem, selecione a pasta Backup_Nuvem dentro da pasta do projeto para ser sincronizada.

Pronto! A cada venda, o sistema gera o ZIP e a nuvem envia para a internet.

🖥️ Como Usar
Iniciar: Execute o arquivo app_fluxoDeCaixa.py.

Vender: Digite a descrição e o valor, escolha o método e aperte "Registrar Entrada".

Corrigir: Se errar, use o botão ✏️ para editar ou 🗑️ para excluir (disponível para vendas do dia).

Consultar: Clique na aba "Histórico" para ver vendas de datas passadas.

Abrir Backups: Use o botão "Abrir Pasta ZIPS" na lateral direita para acessar os arquivos de segurança.

🛡️ Segurança de Dados
O sistema mantém apenas os 10 backups mais recentes para otimizar espaço.

Nunca apague os arquivos .csv manualmente, a menos que queira resetar o sistema completamente.
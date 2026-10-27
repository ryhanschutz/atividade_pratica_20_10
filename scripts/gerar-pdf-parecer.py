import pymupdf

def gerar_pdf_parecer():
    doc = pymupdf.open()
    
    # Estilos e Configurações
    margem_x = 50
    largura_util = 595 - 2 * margem_x
    
    # Página 1: Identificação, Sumário Executivo e Impactos Trabalhistas
    page1 = doc.new_page(width=595, height=842)
    
    # Cabeçalho
    rect_topo = pymupdf.Rect(margem_x, 40, 595 - margem_x, 85)
    page1.draw_rect(rect_topo, color=(0.1, 0.2, 0.45), fill=(0.93, 0.95, 0.98), width=1.5)
    page1.insert_text((margem_x + 15, 60), "AeroMotion Dynamics S.A. - Divisão de Turbinas & Propulsão", fontsize=12, fontname="helv", color=(0.1, 0.2, 0.45))
    page1.insert_text((margem_x + 15, 76), "PARECER TÉCNICO, REGULATÓRIO, ÉTICO E PLANO DE MLOPS", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    
    html_p1 = """
    <style>
      body { font-family: Helvetica, sans-serif; font-size: 10pt; line-height: 1.45; color: #222; }
      h1 { font-size: 14pt; color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 4px; margin-top: 15px; }
      h2 { font-size: 11pt; color: #2b6cb0; margin-top: 12px; margin-bottom: 4px; }
      p { margin-bottom: 8px; text-align: justify; }
      ul { margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }
      li { margin-bottom: 4px; text-align: justify; }
      .meta { font-size: 8.5pt; color: #555; margin-bottom: 15px; }
      .box { background-color: #f7fafc; border-left: 4px solid #3182ce; padding: 8px; margin-bottom: 12px; }
    </style>
    <body>
      <div class="meta">
        <b>Data de Emissão:</b> 27/10/2026 &nbsp;|&nbsp; <b>Bancadas:</b> TURB-101 a TURB-104 &nbsp;|&nbsp; <b>Doc:</b> PARECER-ENG-REG-01/2026
      </div>
      
      <div class="box">
        <b>Sumário Executivo:</b> Este documento consolida a governança técnica, os impactos sociotrabalhistas, a conformidade à LGPD e ao EU AI Act, a cibersegurança industrial OT/IT e o plano de monitoramento contínuo (MLOps) para a operação do sistema de IA de monitoramento preditivo e visão computacional na montagem e testes de turbinas industriais de alta precisão.
      </div>

      <h1>1. Governança Regulatória e Impactos Éticos</h1>
      
      <h2>1.1 Impactos Trabalhistas e Requalificação Profissional de Inspetores Manuais</h2>
      <p>
        A implementação do monitoramento preditivo automatizado de vibração e da inspeção óptica/termográfica computadorizada transforma as rotinas operacionais fabris da AeroMotion Dynamics:
      </p>
      <ul>
        <li><b>Mitigação de Riscos Ergonômicos e Fadiga Ocular:</b> A inspeção tradicional manual de pás submetia inspetores a longas jornadas sob luz estroboscópica e exposição a radiação térmica. A triagem automática via Canny Edge e análise térmica HSV mitiga o cansaço visual e elimina erros decorrentes de fadiga cognitiva.</li>
        <li><b>Programa de Requalificação Profissional (Upskilling):</b> Nenhum posto de trabalho será suprimido. Os técnicos e inspetores passam por capacitação intensiva para atuarem como <i>Supervisores Técnicos de Inspeção Aumentada</i>, habilitados a validar anomalias limítrofes, monitorar alertas preditivos e alimentar ordens de manutenção corretiva e preventiva baseada na condição do equipamento.</li>
        <li><b>Explicabilidade Operacional e Confiabilidade:</b> Os sistemas de IA preditiva (Random Forest e Isolation Forest) fornecem scores de confiança e importância das grandezas físicas (pressão, temperatura, severidade dinâmica), assegurando transparência na tomada de decisão dos operadores.</li>
      </ul>
    </body>
    """
    rect_content1 = pymupdf.Rect(margem_x, 95, 595 - margem_x, 800)
    page1.insert_htmlbox(rect_content1, html_p1)
    page1.insert_text((595 - margem_x - 40, 820), "Página 1 de 3", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Página 2: LGPD, EU AI Act e Cibersegurança OT/IT
    page2 = doc.new_page(width=595, height=842)
    page2.draw_rect(pymupdf.Rect(margem_x, 40, 595 - margem_x, 65), color=(0.1, 0.2, 0.45), fill=(0.95, 0.95, 0.95), width=0.5)
    page2.insert_text((margem_x + 10, 56), "AeroMotion Dynamics S.A. | Conformidade Legal, Regulatória e Cibersegurança", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    html_p2 = """
    <style>
      body { font-family: Helvetica, sans-serif; font-size: 9.8pt; line-height: 1.45; color: #222; }
      h2 { font-size: 11pt; color: #2b6cb0; margin-top: 10px; margin-bottom: 4px; }
      p { margin-bottom: 8px; text-align: justify; }
      ul { margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }
      li { margin-bottom: 4px; text-align: justify; }
    </style>
    <body>
      <h2>1.2 Conformidade com a LGPD (Lei Geral de Proteção de Dados - Lei nº 13.709/2018)</h2>
      <p>
        A introdução de câmeras industriais (ópticas e de infravermelho) no ambiente fabril para validação geométrica e detecção de hotspots térmicos observa estritamente os preceitos de privacidade:
      </p>
      <ul>
        <li><b>Minimização e Princípio da Finalidade (Art. 6º, I e III):</b> Os sensores ópticos são confinados e posicionados no interior do compartimento das pás de turbina. O enquadramento é estritamente mecânico, sem captura de corredores de tráfego humano.</li>
        <li><b>Anonimização em Tempo Real no Nó Edge (Art. 12):</b> Caso ocorra intervenção humana imprevista na área de teste, o pipeline de captura aplica rotinas morfológicas e desfoque gaussiano para mascarar rostos e elementos identificadores de operadores antes de qualquer transmissão ou log.</li>
        <li><b>Proibição Expressa de Biometria:</b> O sistema não dispõe de módulos biométricos, sendo vedada sua utilização para controle de jornada ou vigilância pessoal dos trabalhadores.</li>
      </ul>

      <h2>1.3 Classificação Regulatória sob o EU AI Act (Sistemas de Alto Risco)</h2>
      <p>
        Pela legislação europeia (EU AI Act, Anexo III), o sistema classifica-se como <b>IA de Alto Risco (High-Risk)</b>, por constituir componente de segurança e integridade de sistemas mecânicos industriais pesados e propulsão:
      </p>
      <ul>
        <li><b>Mitigação de Falhas Catastróficas:</b> Exigência de taxa de falso negativo próxima a zero em cavitação e desgaste de rolamento, assegurada pelo treinamento com balanceamento de dados (SMOTE) atingindo Recall > 90% em todas as anomalias.</li>
        <li><b>Supervisão Humana Ativa (Human-in-the-Loop):</b> Os diagnósticos da API servem como apoio à engenharia, sendo vedada a ejeção automática de peças sem confirmação e auditoria humana.</li>
        <li><b>Trilha de Auditoria e Governança:</b> Todos os parâmetros de entrada e inferências são persistidos com carimbo de tempo, garantindo total rastreabilidade técnica e forense.</li>
      </ul>

      <h2>1.4 Cibersegurança Industrial e Convergência OT/IT (IEC 62443)</h2>
      <p>
        A integração da API preditiva às redes de Controladores Lógicos Programáveis (CLP/SCADA) exige controles cibernéticos rígidos:
      </p>
      <ul>
        <li><b>Segmentação em Zonas (Arquitetura Purdue):</b> A API e os nós de Edge residem no Nível 3 (DMZ Operacional), blindando as redes de chão de fábrica (Níveis 1 e 2) contra tráfego externo.</li>
        <li><b>Prevenção de Envenenamento de Dados (Data Poisoning):</b> Validação restritiva de tipos e faixas físicas operacionais via schemas Pydantic na API REST, descartando anomalias sintéticas induzidas por ataques de injeção de pacotes na rede local.</li>
        <li><b>Integridade de Artefatos:</b> Arquivos de modelo (.joblib) utilizam verificação criptográfica SHA-256 no momento da carga pelo serviço conteinerizado.</li>
      </ul>
    </body>
    """
    rect_content2 = pymupdf.Rect(margem_x, 75, 595 - margem_x, 800)
    page2.insert_htmlbox(rect_content2, html_p2)
    page2.insert_text((595 - margem_x - 40, 820), "Página 2 de 3", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Página 3: Plano de MLOps (Data/Concept Drift em 12 Meses) e Conclusão
    page3 = doc.new_page(width=595, height=842)
    page3.draw_rect(pymupdf.Rect(margem_x, 40, 595 - margem_x, 65), color=(0.1, 0.2, 0.45), fill=(0.95, 0.95, 0.95), width=0.5)
    page3.insert_text((margem_x + 10, 56), "AeroMotion Dynamics S.A. | Plano de MLOps e Monitoramento Contínuo", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    html_p3 = """
    <style>
      body { font-family: Helvetica, sans-serif; font-size: 9.8pt; line-height: 1.45; color: #222; }
      h1 { font-size: 13pt; color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 4px; margin-top: 5px; }
      h2 { font-size: 11pt; color: #2b6cb0; margin-top: 10px; margin-bottom: 4px; }
      p { margin-bottom: 8px; text-align: justify; }
      ul { margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }
      li { margin-bottom: 4px; text-align: justify; }
      table { width: 100%; border-collapse: collapse; margin-top: 8px; margin-bottom: 12px; font-size: 9pt; }
      th, td { border: 1px solid #cbd5e0; padding: 6px; text-align: left; }
      th { background-color: #ebf8ff; color: #2b6cb0; }
    </style>
    <body>
      <h1>2. Plano de MLOps: Monitoramento e Manutenção Contínua (Janela de 12 Meses)</h1>
      
      <h2>2.1 Estratégias contra Data Drift e Concept Drift</h2>
      <p>
        Durante o ciclo operacional de 12 meses das bancadas de teste, variações térmicas sazonais, desgaste gradual mecânico e calibrações de instrumentação geram distorções no padrão de telemetria:
      </p>
      <ul>
        <li><b>Monitoramento de Data Drift (Covariate Shift):</b> Execução automatizada semanal do teste bicaudal de Kolmogorov-Smirnov (KS-test) sobre as séries temporais dos sensores e cálculo do Population Stability Index (PSI). Um PSI superior a 0,2 em variáveis térmicas ou de vibração dispara reavaliação de calibração dos sensores.</li>
        <li><b>Monitoramento de Concept Drift:</b> Cruzamento contínuo entre os apontamentos do Isolation Forest (outliers estatísticos não documentados) e as predições supervisionadas. Caso a discordância atinja patamares superiores a 8%, inicia-se investigação técnica de novos modos de falha.</li>
        <li><b>Pipeline de Retreinamento Contínuo:</b> Coleta periódica de amostras validadas pelo time de manutenção. Os novos modelos só substituem as versões produtivas em Edge caso superem a linha de base em Recall de falhas críticas (>90%) e F1-Score Macro.</li>
      </ul>

      <h2>2.2 Resumo Comparativo de Desempenho dos Modelos</h2>
      <table>
        <tr>
          <th>Modelo / Abordagem</th>
          <th>Acurácia</th>
          <th>Recall Médio (Falhas)</th>
          <th>F1-Score Macro</th>
          <th>Aplicação Operacional</th>
        </tr>
        <tr>
          <td><b>Random Forest + SMOTE</b></td>
          <td>97.4%</td>
          <td>94.8%</td>
          <td>0.951</td>
          <td>Classificação multiclasse precisa de modos de avaria</td>
        </tr>
        <tr>
          <td><b>HistGradientBoosting</b></td>
          <td>96.8%</td>
          <td>93.2%</td>
          <td>0.942</td>
          <td>Processamento ultrarrápido em nós Edge de baixo consumo</td>
        </tr>
        <tr>
          <td><b>Isolation Forest</b></td>
          <td>N/A</td>
          <td>92.5% (Detecção)</td>
          <td>N/A</td>
          <td>Detecção de comportamentos anômalos não mapeados</td>
        </tr>
      </table>

      <h2>3. Conclusão e Parecer Técnico</h2>
      <p>
        O conjunto de soluções preditivas, algoritmos de visão computacional multimodal, conteinerização Docker e protocolos regulatórios atende integralmente aos requisitos de segurança operacional, governança da LGPD/EU AI Act e eficiência industrial da AeroMotion Dynamics S.A., conferindo excelência e prontidão para implantação em escala nas bancadas de teste TURB-101 a TURB-104.
      </p>
    </body>
    """
    rect_content3 = pymupdf.Rect(margem_x, 75, 595 - margem_x, 800)
    page3.insert_htmlbox(rect_content3, html_p3)
    page3.insert_text((595 - margem_x - 40, 820), "Página 3 de 3", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    caminho_pdf = "Parecer_Tecnico_Regulatorio_Etico_MLOps.pdf"
    doc.save(caminho_pdf)
    doc.close()
    print(f"PDF consolidado gerado com sucesso em: {caminho_pdf}")

if __name__ == "__main__":
    gerar_pdf_parecer()

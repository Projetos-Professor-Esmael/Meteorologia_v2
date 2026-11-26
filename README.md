# MeteoMapa v2

Site de meteorologia no estilo Windy, 100% estático (GitHub Pages) e gratuito:
mapa com vento animado e camadas (vento, temperatura, chuva, nuvens, pressão), linha do tempo de 4 dias, radar recente, busca de cidades, previsão de 7 dias, favoritos, notícias do tempo (Brasil, Mundo, Tempestades), relatório em PDF com links clicáveis, envio por WhatsApp e e-mail. **Sem login: qualquer pessoa usa direto.** Tema claro e escuro (segue o sistema e pode ser alternado no botão do topo; a escolha fica salva no navegador, e o mapa base troca junto).

## Como funciona (sem servidor próprio)
| Parte | Fonte / tecnologia | Observação |
|---|---|---|
| Previsão e grade do mapa | Open-Meteo (sem chave) | Gratuito só para uso não comercial; limite de uso justo (cerca de 10.000 chamadas/dia). Atribuição obrigatória (já no rodapé). |
| Busca de cidades | Geocoding do Open-Meteo | Mesmas regras. |
| Radar | RainViewer | Gratuito para uso pessoal/educacional; só radar recente, zoom até 7. Atribuição obrigatória (já incluída). |
| Mapa base | Esri (cinza claro/escuro e satélite), com troca automática para OpenStreetMap e Esri Ruas se falhar | A CARTO passou a exigir chave de API (marca d'água "API KEY REQUIRED"), por isso foi removida. Mantenha as atribuições. |
| Notícias | GitHub Actions + RSS, gravadas em `news.json` | Atualização a cada 3 horas; o navegador não lê RSS de outros sites por causa do CORS. |
| Relatório diário por e-mail | GitHub Actions + SMTP (Gmail com senha de app) | Lista de cidades em `cidades.json`; destinatários nos Secrets. |

## Novidades da v2
- Mapa base volta a aparecer, com 3 provedores em cascata.
- Layout responsivo reescrito (celular, tablet, desktop, paisagem), com áreas seguras do iPhone, `100dvh`, campo de busca sem zoom no iOS e painel recolhível.
- Leaflet e jsPDF hospedados na pasta `vendor/` (sem depender de CDN); jsPDF só carrega ao gerar o relatório.
- Menos partículas e grade mais leve no celular; respeita "reduzir movimento".

## Arquivos
- `vendor/`: Leaflet 1.9.4 e jsPDF 2.5.1 (licenças incluídas).
- `.nojekyll`: evita processamento Jekyll no GitHub Pages.
- `index.html`: o site inteiro.
- `news.json`: notícias (gerado pelo workflow).
- `cidades.json`: cidades do relatório diário por e-mail.
- `scripts/fetch_weather_news.py` e `scripts/daily_report.py`.
- `.github/workflows/news.yml` e `.github/workflows/daily-report.yml`.
- `TUTORIAL.md`: passo a passo completo.

## Limites honestos
- Não é o Windy: os dados vêm de modelos do Open-Meteo em uma grade de 8 x 6 pontos por tela, interpolada. Serve para ver padrões de vento, chuva e temperatura, não detalhes locais finos.
- "Tempo real" aqui significa modelos atualizados de hora em hora e notícias a cada 3 horas, não segundos.
- O WhatsApp automático e gratuito não existe: o botão usa o compartilhamento do sistema (celular) ou abre o WhatsApp para você anexar o PDF.
- Material informativo. Para alertas oficiais, consulte INMET e Defesa Civil.

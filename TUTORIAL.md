# Tutorial: publicar o MeteoMapa no GitHub Pages

O site funciona **sem login**: não há conta, senha nem cadastro. Os favoritos ficam salvos só no navegador de quem usa.

## 1. Enviar os arquivos
1. Crie um repositório público no GitHub (ex.: `meteomapa`).
2. Envie `index.html`, a pasta `vendor` (obrigatória), o arquivo `.nojekyll`, `news.json`, `cidades.json`, `README.md`, `TUTORIAL.md` e a pasta `scripts`.
3. **Pasta `.github`:** o envio pelo navegador costuma ignorar pastas que começam com ponto. Crie os dois arquivos pelo site: Add file > Create new file, digite `.github/workflows/news.yml` no nome (as barras criam as pastas), cole o conteúdo e clique em Commit changes. Repita com `.github/workflows/daily-report.yml`. (Com Git no computador, `git add -A` já inclui a pasta.)

## 2. Ativar o GitHub Pages
Settings > Pages > Build and deployment > Source: Deploy from a branch > Branch: `main` / `(root)` > Save. Em 1 a 2 minutos o endereço aparece: `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

## 3. Permitir que o robô grave as notícias
Settings > Actions > General > Workflow permissions > **Read and write permissions** > Save.

## 4. Primeira carga das notícias
1. Aba Actions > "Atualizar notícias do tempo" > Run workflow.
2. Abra a execução e leia o log: cada fonte informa quantos itens trouxe. Verde = ok.
3. Espere cerca de 1 minuto e recarregue o site com Ctrl+F5. Botão Notícias deve mostrar as manchetes.
Depois disso o workflow roda sozinho a cada 3 horas. O GitHub pode atrasar tarefas agendadas e desativa agendamentos de repositórios inativos por 60 dias: se isso acontecer, rode manualmente uma vez.

## 5. Relatório diário por e-mail (opcional)
1. No Gmail, ative a verificação em duas etapas e crie uma **senha de app** (nunca use a senha normal).
2. Settings > Secrets and variables > Actions > Secrets: crie `SMTP_USER` (seu e-mail), `SMTP_PASS` (a senha de app) e `MAIL_TO` (destinatários separados por vírgula).
3. Aba Variables: crie `SITE_URL` com o endereço do seu site.
4. Edite `cidades.json` com as cidades desejadas (nome, lat, lon).
5. Actions > "Relatório diário por e-mail" > Run workflow para testar. Depois ele roda todo dia às 06:00 (Brasília).
Outro provedor SMTP: defina também os Secrets `SMTP_HOST` e `SMTP_PORT`.

## 6. WhatsApp e e-mail pelo botão Relatório
- Celular: "Enviar por WhatsApp" abre o menu de compartilhamento com o PDF anexado.
- Computador: baixa o PDF e abre o WhatsApp com o resumo; anexe o arquivo.
- E-mail: baixa o PDF e abre o app de e-mail com o texto pronto.
Envio automático para qualquer número sem custo não existe: o WhatsApp oficial cobra por mensagem e exige conta Meta verificada.

## 7. Cuidados de uso e limites
- Open-Meteo: gratuito para uso não comercial, com atribuição. Se o site ganhar muito acesso, o limite diário pode ser atingido (o site avisa na tela). Uso comercial exige plano pago.
- RainViewer: uso pessoal ou educacional, radar recente, zoom até 7.
- Mapa base: mantenha as atribuições; para alto tráfego, avalie um provedor com chave gratuita.
- Termos e limites mudam: revise as páginas oficiais dos provedores de vez em quando.

## 8. Problemas comuns
| Sintoma | Causa provável | Solução |
|---|---|---|
| Mapa base cinza ou com marca d'água | Provedor de tiles bloqueado ou mudou regras | O site troca sozinho de provedor; se todos falharem, veja o console (F12) |
| Mapa sem cores ou "Limite gratuito atingido" | Muitas chamadas ao Open-Meteo no seu IP | Aguarde alguns minutos; evite arrastar o mapa sem parar |
| Notícias vazias | Workflow não rodou ou sem permissão de escrita | Passos 3 e 4; leia o log vermelho |
| `news.json` atualiza mas o site não | Cache do navegador ou deploy do Pages em andamento | Ctrl+F5 e aguarde 1 a 2 minutos |
| Workflow não aparece na aba Actions | Pasta `.github` não foi enviada | Passo 1.3 |
| E-mail diário não chega | Senha de app errada, Secrets ausentes ou spam | Releia o log da execução; confira os Secrets |
| Radar não aparece | RainViewer indisponível ou zoom acima de 7 | Reduza o zoom; tente depois |

## 9. O que ainda não existe (próximas etapas)
Favoritos sincronizados entre aparelhos (exigiria conta de usuário), alertas oficiais do INMET no mapa, camadas de ondas e satélite, grade mais fina por tela e visualização 3D.

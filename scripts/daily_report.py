"""Envia por e-mail a previsão de 3 dias das cidades de cidades.json.
Secrets: SMTP_USER, SMTP_PASS, MAIL_TO (lista separada por vírgula). Opcionais: SMTP_HOST, SMTP_PORT, SITE_URL."""
import json, os, smtplib, ssl, urllib.request, datetime as dt
from email.message import EmailMessage
from html import escape

WMO = {0: "Céu limpo", 1: "Poucas nuvens", 2: "Parcialmente nublado", 3: "Nublado", 45: "Neblina", 48: "Neblina", 51: "Garoa fraca", 53: "Garoa", 55: "Garoa forte",
       61: "Chuva fraca", 63: "Chuva", 65: "Chuva forte", 80: "Pancadas fracas", 81: "Pancadas", 82: "Pancadas fortes", 95: "Trovoada", 96: "Trovoada com granizo", 99: "Trovoada com granizo"}
def build(cidades, dados, site=""):
    hoje = dt.date.today().strftime("%d/%m/%Y")
    txt, htm = [f"Previsão do tempo, {hoje}", ""], [f"<h2>Previsão do tempo, {hoje}</h2>"]
    for c, d in zip(cidades, dados):
        dd = d["daily"]; txt.append(c["nome"]); htm.append(f"<h3>{escape(c['nome'])}</h3><ul>")
        for i, t in enumerate(dd["time"]):
            dia = dt.date.fromisoformat(t).strftime("%d/%m")
            linha = f"{dia}: {dd['temperature_2m_min'][i]:.0f}° a {dd['temperature_2m_max'][i]:.0f}°, chuva {dd['precipitation_probability_max'][i] or 0}%, {WMO.get(dd['weather_code'][i], 'sem descrição')}"
            txt.append("  " + linha); htm.append(f"<li>{escape(linha)}</li>")
        htm.append("</ul>"); txt.append("")
    rod = "Dados: Open-Meteo.com (CC BY 4.0). Para alertas oficiais consulte INMET e Defesa Civil."
    if site: txt.append("Mapa ao vivo: " + site); htm.append(f'<p><a href="{escape(site)}">Abrir o mapa ao vivo</a></p>')
    htm.append(f"<p style='color:#666;font-size:12px'>{rod}</p>"); txt.append(rod)
    return hoje, "\n".join(txt), "".join(htm)
def main():
    cidades = json.load(open("cidades.json", encoding="utf-8"))
    la, lo = ",".join(str(c["lat"]) for c in cidades), ",".join(str(c["lon"]) for c in cidades)
    u = f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&forecast_days=3&timezone=America/Sao_Paulo"
    dados = json.load(urllib.request.urlopen(u, timeout=30)); dados = dados if isinstance(dados, list) else [dados]
    hoje, txt, htm = build(cidades, dados, os.environ.get("SITE_URL", ""))
    user, pwd = os.environ["SMTP_USER"], os.environ["SMTP_PASS"]
    m = EmailMessage(); m["Subject"], m["From"], m["To"] = f"Previsão do tempo {hoje}", user, os.environ["MAIL_TO"]
    m.set_content(txt); m.add_alternative(htm, subtype="html")
    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com"), int(os.environ.get("SMTP_PORT", "465")), context=ssl.create_default_context()) as s:
        s.login(user, pwd); s.send_message(m)
    print("E-mail enviado para", os.environ["MAIL_TO"])
if __name__ == "__main__": main()

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

#LR_pred_znanii_ii
print("=== ЛАБОРАТОРНАЯ РАБОТА №2: WEB-SCRAPING ===\n")
# 1.1 Выбор исполнителя
artist=input("Введите имя исполнителя: ").strip()
if not artist:artist="Eminem"
print(f"\n[OK] Исполнитель выбран: {artist}")

# 1.2 Формирование URL для lyrics.com
encoded_artist=quote(artist)
url=f"https://www.lyrics.com/artist.php?name={encoded_artist}"
print(f"[OK] Сформирован URL: {url}")

# 2. Получение HTML-документа (веб-скрейпинг!)
print("\n[->] Отправка GET-запроса к серверу...")
response=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
print(f"[->] Статус ответа: {response.status_code}")

if response.status_code!=200:
    print("[!] Сервер не вернул успешный ответ. Завершение.")
    exit()
html_content=response.text
print("[OK] HTML-документ успешно получен.")

# 3. Извлечение TOP RESULT
print("\n[SEARCH] Поиск 'TOP RESULT' (заголовка исполнителя)...")
soup=BeautifulSoup(html_content,"html.parser")

top_result="Не найден"
h1 = soup.find("h1")
h2=soup.find("h2")

if h1:
        top_result=h1.get_text().strip()
        print(f"[+] Найден в <h1>: {top_result}")
        print(f"    HTML-фрагмент: {h1}")
elif h2:
    top_result=h2.get_text().strip()
    print(f"[+] Найден в <h2>: {top_result}")
    print(f"    HTML-фрагмент: {h2}")
else:print("[!] TOP RESULT не найден в заголовках <h1> или <h2>.")

# 3. Извлечение первых 3 песен
print("\n[SEARCH] Поиск первых 3 песен (ссылки с /lyric/ в href)...")
Songs=[]
track_links=soup.find_all("a",href=lambda href:href and "/lyric/" in href)

print(f"[->] Найдено потенциальных ссылок: {len(track_links)}")

for i,link in enumerate(track_links):
    title=link.get_text().strip()
    if title and title not in Songs:
        Songs.append(title)
        print(f"[+] Песня #{len(Songs)}: {title}")
        print(f"    HTML-фрагмент: {link}")
        if len(Songs)>=3:break

# 4. Вывод результата
print("\n"+"="*60)
print("РЕЗУЛЬТАТ")
print("="*60)
print(f"ИСПОЛНИТЕЛЬ: {artist}")
print(f"TOP RESULT: {top_result}")
print("\nТРИ ПЕРВЫЕ ПЕСНИ:")
if Songs:
    for i,song in enumerate(Songs[:3],1):print(f"{i}. {song}")
else:print("Песни не найдены.")

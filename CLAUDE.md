# Kawalerka A3 · Milczańska 18 (Poznań) – model 3D do spaceru

Jednoplikowa strona (`index.html`) z modelem 3D mieszkania kupionego w stanie deweloperskim.
Służy właścicielom (bez doświadczenia w 3D) do sprawdzania układu, mebli i wariantów łazienki
na etapie koncepcji, przed decyzjami instalacyjnymi. Interfejs i komentarze po polsku.

## Zasady pracy
- Wszystko zostaje w JEDNYM pliku `index.html` (HTML + CSS + JS). Bez bundlera, bez npm.
- three.js **r128** z CDN: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
  (API r128: `outputEncoding`, `BoxGeometry` itd. Nie podbijaj wersji bez potrzeby).
- Uruchomienie: otwórz `index.html` w przeglądarce (albo `npx serve .`).
- Po każdej zmianie zrób zrzut: `python3 tools/screenshot.py` (wymaga `pip install playwright && playwright install chromium`),
  potem obejrzyj `shots/*.png`.
- Wymiary podawaj w metrach w kodzie, w cm w UI. Nie zmieniaj geometrii ścian bez prośby użytkownika.
- Nie twierdź, że ścianę można usunąć. Model nie weryfikuje konstrukcji. Ściany zewnętrzne,
  międzylokalowe, słupek i szacht traktuj jako stałe, nie do ruszania. Karta dewelopera ma
  legendę ścian rozbieralnych/nierozbieralnych, ale każda zmiana ścian wymaga weryfikacji przez fachowca.

## Układ współrzędnych
- Początek (0,0) = wewnętrzny narożnik: ściana wejściowa (korytarz klatki) × lewa ściana.
- **x** → w prawo (0 … 4,25 m), **z** → w głąb, w stronę ogródka (0 … 6,70 m), **y** → w górę.
- Patrząc od wejścia w stronę ogródka: x=0 (szafa, stół, sofa) jest po PRAWEJ ręce – to poprawne, nie lustro.
- Rzut referencyjny: `reference/rzut_deweloper_A3.png` (wejście u góry, ogródek u dołu, ta sama orientacja co x/z).

## Wymiary (z karty lokalu dewelopera, ±5 cm)
| Element | x [m] | z [m] | uwagi |
|---|---|---|---|
| Wnętrze całe | 0–4,25 | 0–6,70 | wysokość H=2,55 (podana przez właścicieli 22.11.2026, potwierdzić po odbiorze) |
| Przedpokój | 0–1,88 | 0–2,07 | 3,72 m², otwarty na pokój |
| Łazienka | 2,00–4,25 | 0–1,95 | 4,28 m² |
| Ścianka przedpokój/łazienka | 1,88–2,00 | 0–2,07 | 12 cm, drzwi łazienki z=0,35–1,15 (80 cm), nadproże 2,05 |
| Ściana łazienka/pokój | 2,00–4,25 | 1,95–2,07 | 12 cm |
| Szacht instalacyjny | 3,65–4,25 | 2,07–2,76 | pełna wysokość, nie ruszać |
| Słupek przy wejściu | 0–0,32 | 0–0,30 | |
| Drzwi wejściowe | 0,75–1,65 | ściana z<0 | wys. 2,05 |
| Drzwi tarasowe | 1,72–3,42 | ściana z=6,70–6,95 | 1,70 m, wys. 2,25 |
| Pokój dzienny z aneksem | 0–4,25 | 2,07–6,70 | 19,32 m² |
| Ogródek | −0,15–4,40 | 6,95–12,20 | 23,49 m², ogrodzenie ~50 cm |
Ściany zewnętrzne 25 cm, działowe 12 cm.

## Struktura kodu
- `W(x0,x1,z0,z1,y0,y1)`: ściana. Pełne (y0=0) trafiają do `wallsG` + kolizje `solids`, nadproża do `lintG`.
  W widoku z góry `wallsG.scale.y=0.42`, `lintG` ukryte, sufit ukryty.
- `DEFAULT` – lista mebli tworzona helperem `R(id,nazwa,kind,x0,x1,z0,z1,h,kolor,wariant)`.
  Obiekt mebla: `{id,name,kind,x,z (środek),w (wzdłuż x),d (wzdłuż z),h,rot (stopnie),color,v,hidden}`.
- `v`: `'all'` | `'dev'` | `'nasz'`. Przełącznik „Wariant łazienki i kuchni” ustawia `state.bath` i pokazuje odpowiedni wariant.
- Pola opcjonalne mebla: `y` (wys. dolnej krawędzi: szafki wiszące, lustro, drabinka), `mods` (linie podziału frontów), `hob:2` (płyta 2-palnikowa), `fr` (wariant lodówki), `sink`, `face:'+x'` (front szafy od +x).
- `build(it)` rysuje mebel wg `kind`: sofa, bed, table, chair, wardrobe, tall, upper, sinkc, cook, tv, sink,
  bath, wc, washer, fridge, shower, showerq (półokrągły, narożnik w lokalnym +x,+z), ladder (grzejnik drabinkowy), mirror (lustro; oba z opcjonalnym `y` = wys. dolnej krawędzi), rug, plant (domyślnie prostopadłościan). Nowy rodzaj = nowy `case`.
- `CATALOG` – meble do dodania z listy: `[nazwa, kind, w, d, h, kolor]`.
- Stan zapisuje się w `localStorage` (klucz `a3-milczanska-uklad-v8`; v1–v7 migrują się z zachowaniem pozycji, przy migracji meble łazienki „nasz” biorą się z `DEFAULT`). Po zmianie `DEFAULT` użyj „Reset”
  albo podbij wersję klucza.
- Sterowanie: Spacer (WASD/strzałki + przeciąganie myszą; telefon: lewa połowa = chodzenie, prawa = rozglądanie),
  Z góry (przeciąganie mebla, skok 5 cm; tło = obrót; kółko/szczypanie = zoom; R = obrót mebla).
- „Kopiuj układ” daje JSON z pozycjami w cm, do wklejenia w rozmowie.

## Kontekst decyzji (stan na 22.11.2026)
- Etap 3/14: koncepcja układu. Odbiór techniczny od dewelopera do 31.12.2026.
- Łazienka „Nasz plan” (z inwentaryzacji wod-kan 02.11.2026, zmiany 22.11.2026):
  umywalka z szafką 60×40 w miejscu dewelopera, przy ścianie wejściowej (x 2,85–3,45, z 0–0,40);
  zabudowa GK 20 cm wzdłuż ściany od pokoju: stelaż WC (x 2,62–3,35, wys. 1,10) + za prysznicem do sufitu, na szerokość kabiny (x 3,35–4,25), obie z 1,75–1,95;
  prysznic półokrągły 90×90 w narożniku przy pionie, od lica zabudowy (x 3,35–4,25, z 0,85–1,75);
  WC podwieszane przed stelażem (x 2,82–3,22, z 1,22–1,75);
  szafa z pralką do sufitu w narożniku przy drzwiach (x 2,00–2,62, z 1,30–1,95);
  lustro 60×80 nad umywalką, dół 110 cm (x 2,85–3,45);
  grzejnik drabinkowy 50×125 na ścianie z umywalką, 115 cm nad podłogą, 16 cm od prawej ściany (x 3,59–4,09; pole `y` = wys. dolnej krawędzi).
  Kielich kanalizacji 110 mm jest w narożniku przy szachcie, a rura do WC idzie w zabudowie ze spadkiem ≥2%.
- Kuchnia: przełącznik „Wariant łazienki i kuchni” przełącza też kuchnię. „Deweloper” = układ z karty (L: lodówka w zabudowie + zmywarka + zlew pod łazienką, płyta wzdłuż prawej ściany).
  „Nasz plan” (22.11.2026): lista rozwijana „Wersja kuchni” (tablica `KITCHEN` = {id,name,desc}; meble wersji mają pole `fr` = id; wybór w `state.fridge`).
  Nowa wersja = wpis w `KITCHEN` + meble z `fr:'<id>'` (brakujące meble z `DEFAULT` dopisują się do zapisanego stanu przy wczytaniu).
  `pod` = jeden blat pod łazienką x 1,90–3,65 (lodówka podblatowa 60 + zmywarka 60 + zlew 55), `wolna` = lodówka wolnostojąca 60×145 + blat zmywarka/zlew x 2,52–3,65,
  `slupek` = słupek do sufitu x 1,90–2,50 (kind `slupek`, pole `split` = wysokości poziomych podziałów: cokół 10 cm, lodówka do zabudowy wnęka 140, podział na 1,55 = dół szafek wiszących) + blat zmywarka/zlew x 2,50–3,65;
  przy ścianie od RTV dolne 3×40 cm (z 2,76–3,96) z płytą 2-palnikową 30×52, wiszące nad nimi 2×60 cm; szafki wiszące 100 cm, góra pod sufitem (dół H−1 = 1,55 m).
  Linie podziału frontów z pola `mods` (szerokości modułów w m), pozycja zlewu z `sink:[x0,x1]`.
- Przedpokój „Nasz plan”: szafa do sufitu (z 0,62–2,04) + obudowa GK przewodu kominowego w narożniku przy wejściu
  (x 0–0,32, z 0,32–0,62, wymiar przyjęty, do zmierzenia) z płytką szafką 28 cm przed nią. „Deweloper” = szafa 2,40 m.

## Pomysły na dalsze kroki
- Łóżko vs sofa rozkładana.
- Etykiety wymiarów i odległości między meblami w widoku z góry (np. przejście ≥ 90 cm).
- Punkty elektryczne/wod-kan jako znaczniki na ścianach.
- Tekstury (płytki, panele), kolory ścian do wyboru.
- Eksport/import układu (wklejenie JSON-a).

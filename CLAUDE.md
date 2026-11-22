# Kawalerka A3 · Milczańska 18 (Poznań) – model 3D do spaceru

Jednoplikowa strona (`index.html`) z modelem 3D mieszkania kupionego w stanie deweloperskim.
Służy właścicielom (bez doświadczenia w 3D) do sprawdzania układu, mebli i wariantów łazienki
na etapie koncepcji, przed decyzjami instalacyjnymi. Interfejs i komentarze po polsku.

## Zasady pracy
- Wszystko zostaje w JEDNYM pliku `index.html` (HTML + CSS + JS). Bez bundlera, bez npm.
- three.js **r128** z CDN: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
  (API r128: `outputEncoding`, `BoxGeometry` itd. Nie podbijaj wersji bez potrzeby).
  Tryb realistyczny dociąga dwa dodatki r128 z jsDelivr: `examples/js/objects/Reflector.js` (lustro) i
  `examples/js/lights/RectAreaLightUniformsLib.js` (światło z drzwi tarasowych). Bez nich działa w uproszczeniu.
- Uruchomienie: otwórz `index.html` w przeglądarce (albo `npx serve .`).
- Po każdej zmianie zrób zrzut: `python3 tools/screenshot.py` (wymaga `pip install playwright && playwright install chromium`),
  potem obejrzyj `shots/*.png` (m.in. `szopka.png`, `real_szopka*.png`). `python3 tools/screenshot.py real` robi tylko kadry trybu realistycznego (`shots/real_*.png`, ok. 1 min).
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
| Ogródek | −0,15–4,40 | 6,95–12,20 | 23,49 m², ogrodzenie ~50 cm, teren 51 cm niżej niż podłoga (`GY`) |
| Stopnie do ogródka | 1,72–3,42 | 6,95–7,90 | 3 stopnie po 17 cm (przyjęte, do zmierzenia): górny 35 cm na poziomie podłogi, dwa po 30 cm; tablica `STEPS` |
Ściany zewnętrzne 25 cm, działowe 12 cm.

## Struktura kodu
- `W(x0,x1,z0,z1,y0,y1)`: ściana. Pełne (y0=0) trafiają do `wallsG` + kolizje `solids`, nadproża do `lintG`.
  W widoku z góry `wallsG.scale.y=0.42`, `lintG` ukryte, sufit ukryty.
- `DEFAULT` – lista mebli tworzona helperem `R(id,nazwa,kind,x0,x1,z0,z1,h,kolor,wariant)`.
  Obiekt mebla: `{id,name,kind,x,z (środek),w (wzdłuż x),d (wzdłuż z),h,rot (stopnie),color,v,hidden}`.
- `v`: `'all'` | `'dev'` | `'nasz'`. Przełącznik „Wariant łazienki i kuchni” ustawia `state.bath` i pokazuje odpowiedni wariant.
- Pola opcjonalne mebla: `y` (wys. dolnej krawędzi: szafki wiszące, lustro, drabinka), `mods` (linie podziału frontów), `hob:2` (płyta 2-palnikowa), `fr` (wariant lodówki), `sink`, `face:'+x'` (front szafy od +x).
- `build(it)` rysuje mebel wg `kind`: sofa, bed, table, chair, wardrobe, tall, upper, sinkc, cook, tv, sink,
  bath, wc, washer, fridge, shower, showerq (półokrągły, narożnik w lokalnym +x,+z), ladder (grzejnik drabinkowy), mirror (lustro; oba z opcjonalnym `y` = wys. dolnej krawędzi), rug, plant (domyślnie prostopadłościan),
  shed (szopka, `buildShed` wspólny dla obu trybów), tires (stos kół), bench (blat warsztatowy), rack (półki/regał: `levels` = wys. półek, `posts`), tools (narzędzia na listwie), raised (skrzynia warzywna, pole `crop`: 'pom' pomidory na tyczkach | 'pap' papryki), strawtower (wieża truskawkowa, 4 piętra). Nowy rodzaj = nowy `case`.
- `CATALOG` – meble do dodania z listy: `[nazwa, kind, w, d, h, kolor]`.
- Stan zapisuje się w `localStorage` (klucz `a3-milczanska-uklad-v10`; v1–v9 migrują się z zachowaniem pozycji, przy migracji meble łazienki „nasz” biorą się z `DEFAULT`). Po zmianie `DEFAULT` użyj „Reset”
  albo podbij wersję klucza.
- Sterowanie: Spacer (WASD/strzałki + przeciąganie myszą; telefon: lewa połowa = chodzenie, prawa = rozglądanie),
  Z góry (przeciąganie mebla, skok 5 cm; tło = obrót; kółko/szczypanie = zoom; R = obrót mebla).
- „Kopiuj układ” daje JSON z pozycjami w cm (plus `id`, `rodzaj`), do wklejenia w rozmowie. „Wklej układ” (`applyLayout`) przyjmuje ten tekst albo plik układu:
  meble dopasowuje po `id`, potem po nazwie; brakujące tworzy wg `rodzaj`, widoczne meble spoza listy ukrywa (jak „Usuń”).
- „Pobierz plik układu” zapisuje pełny stan do `uklad-A3-RRRR-MM-DD_GGMM.json` (`{plik,wersja,zapisano,stan}`), „Wczytaj plik” go przywraca.
  Wczytany stan przechodzi przez `fixState(s)` – tę samą normalizację co stan z `localStorage` (usunięte wersje, nowe meble z `DEFAULT`).
  Gdy `localStorage` nie działa, HUD podpowiada użycie pliku.

## Tryb realistyczny („Wygląd: Makieta | Realistyczny”)
- Ten sam `state.items` rysowany drugim builderem `buildReal(it)`; `rebuild()` wybiera builder wg `style`. Edycja, warianty i kolizje wspólne.
- Wybór zapisany w `localStorage` (klucz `a3-milczanska-styl`), link `index.html?styl=real` otwiera od razu ten tryb.
- `makeReal()` (raz, przy pierwszym włączeniu): tekstury proceduralne w canvasie (`T`, deska, dąb, płytki, kamień, tkanina, trawa…),
  materiały PBR (`MAT`, fabryka `RM` – kolory w sRGB), mapa otoczenia z PMREM, architektura z tej samej listy `WALLS` co makieta,
  cokoły, drzwi, zasłony, oprawy, obraz, ogród, elewacja, niebo, światła. Grupy: `REAL.walls` (skalowane w widoku z góry),
  `REAL.upper` (ukrywane z góry: sufit, nadproża, elewacja, lampy), `REAL.base`.
- Meble budowane w lokalnym układzie „front przy +z” (`frontOf(it)`, wyjątki w `FRONT` po id); `mods` i `sink` odwracane, gdy trzeba.
  Nowy rodzaj mebla = `case` w `build` (makieta) i w `buildReal`.
- Łazienka (22.11.2026): ściany malowane na biało, płytki 60×30 (poziomo) tylko: zabudowa stelaża WC + ściana nad nią do sufitu,
  ściany w narożniku prysznica do sufitu (z zabudową GK), jedna płytka 60×30 nad umywalką (blat → lustro). Panele płytek rysuje `buildReal`
  przy meblach (`tile`/`tileBox`, fugi liczone od lewego dolnego rogu panelu), więc idą za meblem. Podłoga łazienki w płytkach.
- „Pora dnia” (`applyTod`): dzień = słońce przez drzwi tarasowe + światło okna; wieczór = lampa nad stołem, LED pod szafkami, oprawy.
- Cienie liczone tylko po zmianie (`renderer.shadowMap.autoUpdate=false`, po zmianie ustaw `renderer.shadowMap.needsUpdate=true`).
- Materiały, kolory, dekoracje (rośliny, książki, obraz, zasłony, meble ogrodowe) są przykładowe – nie wynikają z decyzji właścicieli.
- `window.A3` (setStyle, setMode, setTod, view) służy do zrzutów ekranu.

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
  „Nasz plan” (decyzja 22.11.2026, pozostałe wersje usunięte): ściana z lodówką = `slupek`, ściana od RTV = `w2x60b`.
  Mechanizm wersji zostaje: tablice `FRIDGE_WALL` (pole mebla `fr`, `state.fridge`) i `RTV_WALL` (pole `rtv`, `state.rtv`); przy jednej wersji lista jest ukryta, widać nazwę + opis.
  Nowa wersja = wpis {id,name,desc} w tablicy + meble z `fr:'<id>'` / `rtv:'<id>'` (brakujące meble z `DEFAULT` dopisują się przy wczytaniu; meble wersji spoza tablic są usuwane z zapisanego stanu).
  `slupek` = słupek do sufitu x 1,90–2,50 (kind `slupek`, pole `split` = wysokości poziomych podziałów: cokół 10 cm, lodówka do zabudowy wnęka 140, podziały na 1,55 i 2,15 = linie szafek wiszących) + blat zmywarka/zlew x 2,50–3,65, nad nim para szafek `UPZ`;
  przy ścianie od RTV dolne 3×40 cm (z 2,76–3,96) z płytą 2-palnikową 30×52, nad nimi wiszące 2×60 jednej głębokości 40 cm od 1,55 do sufitu (`UPX(...,top=false)`, bez górnych 60 gł.).
  Szafki wiszące (obie ściany) = para mebli: górne 40 wys. × 60 gł. pod sufitem (dół `UT`=H−0,40) + dolne 60 wys. × 40 gł. bez przerwy (dół `UY`=H−1 = 1,55 m);
  helpery `UPZ` (ściana pod łazienką) i `UPX` (ściana od RTV).
  Linie podziału frontów z pola `mods` (szerokości modułów w m), pozycja zlewu z `sink:[x0,x1]`.
- Przedpokój „Nasz plan”: szafa do sufitu (z 0,62–2,04) + obudowa GK przewodu kominowego w narożniku przy wejściu
  (x 0–0,32, z 0,32–0,62, wymiar przyjęty, do zmierzenia) z płytką szafką 28 cm przed nią. „Deweloper” = szafa 2,40 m.

- Poziom ogródka (22.11.2026): mieszkanie jest wyżej, z drzwi tarasowych prowadzą 3 stopnie. Stałe `RISE`, `GY`, `STEPS`; `floorAt(x,z)` daje wysokość podłoża
  (0 / stopień / `GY`) – meble w ogródku stawiane są na niej w obu builderach, spacer podnosi/obniża oczy płynnie. Taras z płyt (stolik) u dołu stopni, z 7,90–9,00.

- Ogródek „szopka” (22.11.2026, koncepcja, v:'all'): wąska 85×240 przy płocie sąsiada i elewacji, po LEWEJ po wyjściu na taras (x 3,50–4,35, z 7,00–9,40).
  Pierwsza wersja (160×200 po prawej, id `sz*`) odrzucona – przy wczytaniu usuwana z zapisanego stanu; obecne meble mają id `sw*`.
  Szopka ma `rot:180`: lokalne −x (wysoka ściana 2,20) stoi przy płocie, dach spada na nasz ogródek (front 2,00, pole `fall`), rynna od strony ogrodu (bez beczki).
  Bez wchodzenia do środka: front od strony ogródka z dwoma drzwiami dwuskrzydłowymi (pole `doors` [[z0,z1,'double'|'z0'|'z1']] lokalnie od z0, czyli przy rot 180 od końca od ogrodu):
  przy budynku (z 7,10–8,14) narzędzia na listwie na ścianie od budynku + półka 1,75 + regał 70×60 z 5 półkami;
  od ogrodu (z 8,20–9,32) blat warsztatowy 118×73 na 1,06 (96 cm nad podłogą szopki) z tablicą narzędziową i 2 półkami przy płocie (1,55 i 1,85), pod blatem koła 4× 225/40 R18 w stosie (z 8,67–9,32) i skrzynka.
  Dwa warianty, lista „Ogródek: szopka” (tablica `SHEDS`, pole mebla `shed`, `state.shed`, domyślnie `srodek`):
  `boki` (A, meble `sw*`) = opis wyżej; `srodek` (B, meble `sm*`) = wejście na środku, drzwi przesuwne 80 cm (z 7,80–8,60, `doors` typ 'slide': skrzydło na szynie na zewnątrz, odsunięte w stronę ogrodu),
  przejście 80×73; od ogrodu blat 73×72 nad kołami (front do przejścia) + 2 półki na ścianie od ogrodu; od budynku regał 73×35 na ścianie od budynku + narzędzia na ścianie przy płocie + półka nad wejściem.
  Wnętrze 73 cm szerokości (koło Ø64). Podłoga na podeście 10 cm. Kolizje szopki = ściany (`shedRects`). Z góry: ściany ×0,42, bez dachu.
  Do sprawdzenia przez właścicieli: zgody wspólnoty / regulamin ogródków, MPZP i przepisy o odległości od granicy (2,20 m przy płocie), prąd do warsztatu.

- Ogródek „warzywnik” (22.11.2026, propozycja, v:'all'): skrzynie podwyższone 80 cm szer., 75 cm wys. w L przy płocie po prawej (x≈0) i tylnym,
  środek wolny (trawa ok. 2,8×3,2 m): `gPom` pomidory 240×80 (x −0,10–2,30, z 11,35–12,15), `gPap` papryki 200×80 (x −0,10–0,70, z 9,35–11,35),
  `gTrusk` wieża truskawkowa Ø60, wys. 110 (x 0,15–0,75, z 8,45–9,05) blisko tarasu. Lewy tylny narożnik wolny (drzewo usunięte 22.11.2026).

## Pomysły na dalsze kroki
- Łóżko vs sofa rozkładana.
- Etykiety wymiarów i odległości między meblami w widoku z góry (np. przejście ≥ 90 cm).
- Punkty elektryczne/wod-kan jako znaczniki na ścianach.
- Tekstury (płytki, panele), kolory ścian do wyboru.
- Eksport/import układu (wklejenie JSON-a).

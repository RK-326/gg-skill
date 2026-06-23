# Дизайн-спека (эталон для всех документов)

ВСЕ документы портала выглядят ИДЕНТИЧНО эталону. Здесь зафиксированы точные
значения, чтобы дизайн получался с первого раза.

Эталон оформления (живой файл-образец): `template/example.docx`
(копия «Бакалавриат Инструкция - обновлено.docx»). Пустая болванка с теми же
стилями/колонтитулами/водяным знаком — `template/blank.docx`.

Технические единицы: размеры шрифта в OOXML в half-points (sz=22 → 11pt).
EMU: 914400 EMU = 1 дюйм.

## Страница и поля
- Размер: Letter, `<w:pgSz w:w="12240" w:h="15840"/>` (8.5×11").
- Поля: `<w:pgMar w:top="576" w:right="432" w:bottom="0" w:left="432" w:header="720" w:footer="720" w:gutter="0"/>` (узкие: top 0.4", left/right 0.3").
- Полезная ширина текста ≈ 7223760 EMU — это ШИРИНА всех плашек-shape (`cx="7223760"`).

## Шрифты (все Montserrat, шрифты встроены в файл)
- Боди/по умолчанию: **Montserrat Medium**, sz 22 (11pt), межстрочный 276, spacing after 200.
- Заголовок документа (Title): **Montserrat Black**, sz 60 (30pt), letter-spacing `<w:spacing w:val="5"/>`, spacing after 300.
- Раздел (Heading1): **Montserrat** + `<w:b/>`, sz 36 (18pt), spacing before 480, `<w:pageBreakBefore/>` (каждый раздел с новой страницы), `<w:outlineLvl w:val="0"/>`.
- Подзаголовок (Heading2): тема majorHAnsi + `<w:b/>`, sz 26 (13pt), цвет `4F81BD`.

## Цветовая палитра (HEX, всегда srgbClr / w:color)
- Боди-текст и заголовки 1 уровня: **13445D** (фирменный тёмно-синий, цвет по умолчанию в docDefaults). ВЕСЬ текст в таблицах тоже 13445D (не 202A35, не чёрный).
- Акцент / маркеры списков / номера / подчёркивания в оглавлении: **1A5CA8**.
- Заголовок 2 уровня: **4F81BD**.
- Шапка таблиц: заливка **2C3E50**, текст **FFFFFF** (детали — `../tables/tables-standard.md`).
- Рамки (таблицы, картинки, светлые карточки): **D5DBDB**, толщина `w="9525"` (≈0.75pt), `single`.
- Плашка ВАЖНО: заливка **13445D**, заголовок «ВАЖНО» белый **FFFFFF**, текст **DCE6EC**.
- Плашка «Коротко по разделу»: заливка светло-зелёная **EAF6EF**, заголовок **2C3E50**, текст 13445D.
- Светлая инфо-карточка («Как устроен этот гайд», врезки): заливка **F4F6F7**, рамка D5DBDB, заголовок 13445D.
- Колонтитул: «CONFIDENTIAL» серый **D0D0D0**; бейдж номера страницы синий (1C6083/0B2E40), цифра белая.

## Тень (ОДНА на весь документ, у всех картинок и плашек)
```xml
<a:effectLst><a:outerShdw blurRad="50800" dist="25400" dir="5400000" rotWithShape="0">
  <a:srgbClr val="202A35"><a:alpha val="30000"/></a:srgbClr></a:outerShdw></a:effectLst>
```
Для картинок тень мягче: dist="19050", alpha="24000". 202A35 здесь — цвет ТЕНИ, не текста.

## Плашки = shape `wps:wsp` (НЕ таблицы). Общий рецепт
Inline-drawing, `<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 7000"/></a:avLst></a:prstGeom>`, ширина `cx="7223760"`, `<a:ln><a:noFill/></a:ln>` (у светлой карточки вместо noFill — рамка D5DBDB w=9525), тень (см. выше), `wps:bodyPr` с отступами `lIns="200000" tIns="150000" rIns="200000" bIns="150000"` и `<a:spAutoFit/>`. Внутри `wps:txbx/w:txbxContent` — обычные `w:p`.
- **ВАЖНО**: `solidFill 13445D`; п.1 = `<w:b/><w:color w:val="FFFFFF"/>` sz21 «ВАЖНО»; п.2 = `<w:color w:val="DCE6EC"/>` sz21 текст.
- **Коротко по разделу**: `solidFill EAF6EF`; заголовок `<w:b/><w:color w:val="2C3E50"/>` sz21; пункты с маркером «•».
- **Светлая карточка**: `solidFill F4F6F7` + `<a:ln w="9525"><a:solidFill><a:srgbClr val="D5DBDB"/></a:solidFill></a:ln>`, adj можно 5000.

## Картинки и скриншоты (ВСЕ одинаково)
В каждом `pic:spPr`: геометрия `roundRect` adj 4200 + рамка `<a:ln w="9525">` D5DBDB + тень (dist 19050, alpha 24000). Порядок детей spPr: xfrm, prstGeom, (fill), ln, effectLst. Скриншоты НЕ оставлять прямоугольными без рамки. Текстовый контент НЕ держать картинкой — переносить в обычный текст/маркеры. Стиль генерируемых картинок — `../images/README.md`.

## Списки-маркеры (обычный текст, без боксов)
Обычный `w:p`, `<w:spacing w:after="20"/>`, текст начинается с литерала «•  » (маркер можно цветом 1A5CA8). Никаких декоративных боксов вокруг простых перечислений.

## Сноски
Настоящие сноски Word (`footnotes.xml`), стиль FootnoteText sz20. Если ДВЕ сноски подряд — между ними запятая отдельным надстрочным ран'ом:
`<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/><w:vertAlign w:val="superscript"/></w:rPr><w:t>,</w:t></w:r>` → выглядит как «⁴,⁵».

## Водяной знак (в header1.xml, на каждой странице)
Логотип GG (VML `WordPictureWatermark1`, imagedata), washout `gain="42598f" blacklevel="13107f"` (заметный, но фоновый). ОБЯЗАТЕЛЬНО по центру страницы:
`style="...;margin-left:0;margin-top:0;width:455pt;height:374pt;mso-position-horizontal:center;mso-position-horizontal-relative:margin;mso-position-vertical:center;mso-position-vertical-relative:margin"`.

## Колонтитулы
- Footer: слева «CONFIDENTIAL» (D0D0D0), справа бейдж с номером страницы (поле PAGE, синий бейдж, белая цифра).
- Header: водяной знак + логотип GG.

## Сборка и ОБЯЗАТЕЛЬНАЯ визуальная проверка
Сложное оформление править прямой правкой OOXML через lxml (python-docx не умеет тени/скругления/водяные знаки). Распаковка/запаковка: `unzip` / `zip -X -9` ([Content_Types].xml первым). После сборки проверять ВИЗУАЛЬНО, не на глаз по XML:
1. Экспорт PDF через установленный Word (AppleScript): `osascript` → `tell application "Microsoft Word"` → open / `save as ... file format format PDF` / `close ... saving no`. Оборачивать в `perl -e 'alarm 200; exec @ARGV' osascript ...` от зависаний.
   ВНИМАНИЕ: стартовый экран Word блокирует экспорт. Снять «Show Start screen when opening» или нажать Cancel.
2. Номера страниц для оглавления: venv с `pypdf`, искать текст заголовка по страницам (`PdfReader(...).pages[i].extract_text()`). Сначала собрать с токенами `@@P1@@…`, узнать реальные страницы, подставить.
3. Рендер любой страницы: pypdf вытащить одну страницу в отдельный PDF → `qlmanage -t -s 1600 -o out page.pdf` → PNG → посмотреть. Так проверять плашки, тени, цвета таблиц, центровку водяного знака на стр. 2+ (qlmanage по .docx даёт только стр. 1).

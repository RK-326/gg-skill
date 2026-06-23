#!/usr/bin/env python3
"""
Батч-генерация картинок через OpenRouter (модель Gemini image / Nano Banana).

Ключ берётся из переменной окружения OPENROUTER_API_KEY (см. ../.env).
НЕ хранить ключ в коде.

Примеры:
  source ../.env
  python3 gen_images.py --prompt "схема пути абитуриента, стиль GG" --n 3 --out ../images/_drafts
  python3 gen_images.py --prompt-file prompt.txt --n 5 --out ../images/_drafts

На выходе: PNG-файлы в папке --out (по одному на вариант). Дальше Рената отсматривает,
лучшее переносит в images/reference/, промт дописывает в images/prompts/.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Модель, которая реально РИСУЕТ картинки (Gemini Pro картинки не генерирует).
# Берётся из OPENROUTER_IMAGE_MODEL (.env), иначе дефолт ниже.
DEFAULT_MODEL = os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-2.5-flash-image")

# Префикс фирменного стиля GG (синхронизирован с images/README.md).
# Стиль выбран Ренатой: плоский флэт со сценками и персонажами, палитра GG, БЕЗ текста.
STYLE_PREFIX = (
    "Плоская векторная иллюстрация (flat design) со сценкой и персонажами в действии, "
    "в фирменном стиле образовательного бренда, палитра тёмно-синий #13445D и синий "
    "акцент #1A5CA8, светлый/белый фон, чисто и современно, без стоковой пошлости. "
    "ВАЖНО: на изображении НЕТ никакого текста - ни букв, ни слов, ни надписей, ни "
    "подписей, ни цифр. "
)


def generate_one(prompt, model, api_key):
    """Один запрос к OpenRouter, возвращает bytes картинки (или None)."""
    body = json.dumps({
        "model": model,
        "modalities": ["image", "text"],
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # OpenRouter просит эти заголовки (необязательно, но вежливо):
            "HTTP-Referer": "https://global-generations.com",
            "X-Title": "gg-skill image generation",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # Картинка лежит в choices[0].message.images[0].image_url.url как data:image/...;base64,...
    try:
        images = data["choices"][0]["message"]["images"]
    except (KeyError, IndexError):
        print("  ! в ответе нет картинки. Ответ модели:",
              json.dumps(data)[:500], file=sys.stderr)
        return None
    if not images:
        return None
    url = images[0]["image_url"]["url"]
    if "," in url:
        url = url.split(",", 1)[1]
    return base64.b64decode(url)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt", help="текст промта")
    g.add_argument("--prompt-file", help="файл с промтом")
    ap.add_argument("--n", type=int, default=3, help="сколько вариантов (по умолч. 3)")
    ap.add_argument("--out", default="../images/_drafts", help="папка для PNG")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--no-style", action="store_true",
                    help="не добавлять фирменный префикс стиля")
    ap.add_argument("--name", default="img", help="префикс имени файлов")
    args = ap.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("Нет OPENROUTER_API_KEY. Сначала: source .env (см. .env.example)")

    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = args.prompt
    if not args.no_style:
        prompt = STYLE_PREFIX + prompt

    os.makedirs(args.out, exist_ok=True)
    print(f"Модель: {args.model}")
    print(f"Промт: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print(f"Вариантов: {args.n} → {args.out}\n")

    saved = 0
    for i in range(1, args.n + 1):
        print(f"[{i}/{args.n}] генерирую...")
        try:
            png = generate_one(prompt, args.model, api_key)
        except Exception as e:
            print(f"  ! ошибка запроса: {e}", file=sys.stderr)
            png = None
        if png:
            path = os.path.join(args.out, f"{args.name}_{int(time.time())}_{i}.png")
            with open(path, "wb") as f:
                f.write(png)
            print(f"  ✓ {path}")
            saved += 1
        time.sleep(1)  # не спамить API

    print(f"\nГотово: {saved}/{args.n} картинок в {args.out}")
    if saved:
        print("Дальше: отсмотреть, лучшее перенести в images/reference/, промт — в images/prompts/")


if __name__ == "__main__":
    main()

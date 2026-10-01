import json
import os
import urllib.request
import urllib.error

URL = os.getenv(
    "ULTRON_AI_URL",
    "http://127.0.0.1:8080/v1/chat/completions"
)

MODEL = os.getenv(
    "ULTRON_AI_MODEL",
    "local-model"
)

DEFAULT_SYSTEM = (
    "Você é o núcleo de inteligência artificial do ULTRON-EXPERIMENT. "
    "Responda em português do Brasil. "
    "Raciocine de forma clara e use o contexto fornecido. "
    "Não invente informações quando não souber algo."
)


def ask(
    prompt,
    system=DEFAULT_SYSTEM,
    temperature=0.2,
    max_tokens=256,
):
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "chat_template_kwargs": {
            "enable_thinking": False
        },
    }

    request = urllib.request.Request(
        URL,
        data=json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Não foi possível conectar ao servidor de IA em {URL}: {error}"
        ) from error

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "O servidor de IA retornou uma resposta inválida."
        ) from error

    choices = result.get("choices", [])

    if not choices:
        raise RuntimeError(
            f"Resposta da IA sem choices: {result}"
        )

    message = choices[0].get("message", {})
    content = message.get("content")

    if content is None:
        raise RuntimeError(
            f"Resposta da IA sem conteúdo: {result}"
        )

    return content.strip()


def available(timeout=3):
    request = urllib.request.Request(
        URL,
        method="GET",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout
        ):
            return True
    except Exception:
        return False

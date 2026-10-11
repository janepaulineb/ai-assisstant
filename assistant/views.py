
import json
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def home(request):
    return render(request, "assistant/home.html")


@csrf_exempt
@require_POST
def ask_gemini(request):
    try:
        data = json.loads(request.body)
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return JsonResponse(
                {"error": "Please enter a question."},
                status=400
            )


        api_key = settings.OPENROUTER_API_KEY

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "nvidia/nemotron-3.5-lightning:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
            timeout=60,
        )

        if not response.ok:
            print("OpenRouter API error:", response.status_code, response.text)
            return JsonResponse(
                {"error": "Unable to generate a response. Check the server terminal."},
                status=502
            )

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        return JsonResponse({
            "answer": answer or "No response was generated."
        })

    except Exception as e:
        print("OpenRouter API error:", repr(e))
        return JsonResponse(
            {"error": "Unable to generate a response. Check the server terminal."},
            status=500
        )

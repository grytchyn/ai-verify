# In this environment we cannot call memory tool from within the code (the code runs outside Hermes). 
# So we will embed the system prompt directly, pulled from the known memory fact.
# For simplicity, we define the system prompt as a constant.
SYSTEM_PROMPT = """Ты – эксперт по EU AI Act. Высокорисковые ИИ‑системы: биометрия, критичная инфраструктура, найм, кредит‑scoring, образование. Основные требования: риск‑менеджмент, управление данными, прозрачность, человеческий надзор, ведение журнала событий, оценка соответствия.
Отвечай строго по пунктам, используй только факты из предоставленного контекста."""

def get_system_prompt() -> str:
    return SYSTEM_PROMPT

def build_user_prompt(company: str, url: str, description: str, search_results: list) -> str:
    # Format search results
    search_text = ""
    for idx, r in enumerate(search_results, start=1):
        title = r.get('title', 'No title')
        link = r.get('url', '')
        snippet = r.get('snippet', '')
        search_text += f"{idx}. {title}\n   URL: {link}\n   Сниппет: {snippet}\n\n"
    if not search_text:
        search_text = "Данные из открытых источников не найдены."
    prompt = f"""Проанализируй следующую компанию и её продукт с точки зрения EU AI Act.
Компания: {company}
Сайт: {url}
Описание продукта: {description}
Сведения из открытых источников:
{search_text}
На основании этого определи:
1) Попадает ли продукт под высокорисковую категорию (Да/Нет/Недостаточно данных).
2) Какие требования AI Act вероятно применимы (список).
3) Выявленные gaps (чего не хватает для соблюдения).
4) Конкретные рекомендации (документы, процессы, контрольные точки).
Ответ оформи в markdown с заголовками: **Вывод**, **Категория риска**, **Применимые требования**, **Gaps**, **Рекомендации**, **Источники**.
Если данных недостаточно – укажи, какая информация нужна."""
    return prompt
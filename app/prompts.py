# System prompt for EU AI Act compliance analysis
SYSTEM_PROMPT = """Ты – эксперт по EU AI Act. Высокорисковые ИИ‑системы: биометрия, критичная инфраструктура, найм, кредит‑scoring, образование. Основные требования: риск‑менеджмент, управление данными, прозрачность, человеческий надзор, ведение журнала событий, оценка соответствия.
Отвечай строго по пунктам, используй только факты из предоставленного контекста.

Твой ответ должен быть на РУССКОМ языке (только термины на английском), строго в формате markdown."""

def build_company_profile(submission) -> str:
    """Build structured company profile from submission data."""
    import json
    
    profile = []
    profile.append(f"**Компания:** {submission.company or 'Не указано'}")
    profile.append(f"**Веб-сайт:** {submission.url or 'Не указан'}")
    profile.append(f"**Эл. почта:** {submission.email or 'Не указана'}")
    profile.append(f"**Размер компании:** {submission.company_size or 'Не указан'}")
    profile.append(f"**Сектор:** {submission.sector or 'Не указан'}")
    profile.append(f"**Количество сотрудников:** {submission.employees or 'Не указано'}")
    profile.append(f"**Годовой доход:** {submission.annual_revenue or 'Не указан'}")
    profile.append(f"**Штаб-квартира:** {submission.hq_location or 'Не указана'}")
    
    profile.append("")
    profile.append("### Детали ИИ-систем")
    profile.append(f"**Количество ИИ-систем:** {submission.ai_systems_count or 'Не указано'}")
    profile.append(f"**Названия систем:** {submission.ai_system_names or 'Не указаны'}")
    profile.append(f"**Назначение ИИ:** {submission.ai_purpose or 'Не указано'}")
    profile.append(f"**Тип развертывания:** {submission.deployment_type or 'Не указан'}")
    profile.append(f"**Источники данных:** {submission.data_sources or 'Не указаны'}")
    profile.append(f"**Тип принятия решений:** {submission.decision_type or 'Не указан'}")
    profile.append(f"**Самооценка риска:** {submission.risk_self_assessment or 'Не указана'}")
    
    profile.append("")
    profile.append("### Технические детали")
    profile.append(f"**Типы моделей:** {submission.model_types or 'Не указаны'}")
    profile.append(f"**Происхождение данных:** {submission.training_data_origin or 'Не указано'}")
    profile.append(f"**Механизмы человеческого контроля:** {submission.human_oversight or 'Не указаны'}")
    profile.append(f"**Объяснимость:** {submission.explainability or 'Не указана'}")
    profile.append(f"**Политика хранения данных:** {submission.data_retention or 'Не указана'}")
    
    profile.append("")
    profile.append("### Статус соответствия")
    profile.append(f"**Документация:** {submission.has_documentation or 'Не указано'}")
    profile.append(f"**Назначен DPO:** {submission.dpo_appointed or 'Не указано'}")
    profile.append(f"**Соответствие GDPR:** {submission.gdpr_compliant or 'Не указано'}")
    profile.append(f"**Сертификации:** {submission.existing_certifications or 'Не указаны'}")
    profile.append(f"**Предыдущие аудиты:** {submission.previous_audits or 'Не указаны'}")
    profile.append(f"**CE-маркировка:** {submission.ce_marking or 'Не указана'}")
    
    profile.append("")
    profile.append("### Высокорисковые категории (отмеченные)")
    active = submission.risk_categories_active() if hasattr(submission, 'risk_categories_active') else []
    if active:
        for cat in active:
            profile.append(f"- [x] {cat}")
    else:
        profile.append("- Ни одна из категорий не отмечена")
    
    # Additional info JSON
    if submission.additional_info:
        try:
            extra = json.loads(submission.additional_info)
            if extra:
                profile.append("")
                profile.append("### Дополнительная информация")
                for k, v in extra.items():
                    profile.append(f"- **{k}:** {v}")
        except:
            pass
    
    profile.append("")
    if submission.description:
        profile.append(f"**Описание AI-деятельности:** {submission.description}")
    
    return "\n".join(profile)

def build_user_prompt(company: str, url: str, description: str, search_text: str) -> str:
    """Compatibility: build user prompt from simple fields."""
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

def build_enhanced_prompt(submission, search_text: str = "") -> str:
    """Build enhanced prompt from complete submission object with all fields."""
    profile = build_company_profile(submission)
    
    if not search_text:
        search_text = "Данные из открытых источников не найдены."
    
    prompt = f"""Проанализируй следующую компанию и её ИИ-системы с точки зрения EU AI Act.

## Профиль компании

{profile}

Сведения из открытых источников:
{search_text}

На основании всех предоставленных данных определи и подробно опиши:

## 1. ОБЩИЙ ВЫВОД
Попадает ли деятельность компании под регулирование EU AI Act? Какой общий уровень риска?

## 2. КЛАССИФИКАЦИЯ ПО EU AI ACT
- Категория риска по EU AI Act (Unacceptable / High / Limited / Minimal)
- Обоснование классификации со ссылками на конкретные статьи
- Какие именно ИИ-системы компании подпадают под регулирование

## 3. ПРИМЕНИМЫЕ ТРЕБОВАНИЯ
Детальный список требований EU AI Act, применимых к данному случаю:
- Управление рисками (Article 9)
- Управление данными и обучение (Article 10)
- Техническая документация и прозрачность (Articles 11-12)
- Автоматизированное принятие решений и человеческий надзор (Article 14)
- Точность, устойчивость и кибербезопасность (Article 15)
- Регистрация в базе данных EU (Article 49)
- Требования к прозрачности для пользователей (Article 50)

## 4. ВЫЯВЛЕННЫЕ ПРОБЕЛЫ (GAPS)
Для каждого требования укажи, соответствует ли компания, и если нет — в чём конкретно пробел:
- Отсутствующая документация
- Недостаточные меры контроля
- Проблемы с данными
- Отсутствие человеческого надзора
- Недостаточная прозрачность

## 5. КОНКРЕТНЫЕ РЕКОМЕНДАЦИИ
Пошаговый план действий:
- Какие документы нужно подготовить
- Какие процессы внедрить
- Какие технические меры реализовать
- Сроки и приоритеты (немедленно / краткосрочно / долгосрочно)
- Необходимость DPO и регистрации

## 6. РИСКИ И ШТРАФЫ
- Потенциальные штрафы за несоответствие (до 35 млн EUR или 7% оборота)
- Репутационные риски
- Риски приостановки деятельности

Ответ оформи в markdown с заголовками уровня ## (H2) и ### (H3).
Используй таблицы, списки и жирный текст для акцентирования."""
    
    return prompt

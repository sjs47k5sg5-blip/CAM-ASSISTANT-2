# handlers/contour/processing/data.py

PROCESSING_STEPS = [

    {
        "id": "roughing",
        "title": "🪓 Черновая обработка",
        "field": "roughing_enabled",
        "type": "choice",

        "choices": [

            ("✅ Да", True),

            ("❌ Нет", False),

        ],

    },

    {
        "id": "step_z",

        "title": "📏 Шаг по Z",

        "field": "step_z",

        "type": "number",

        "values": [

            ("1 мм", 1.0),

            ("2 мм", 2.0),

            ("3 мм", 3.0),

        ],

    },

    {
        "id": "stepover",

        "title": "📐 Боковой шаг",

        "field": "roughing_stepover",

        "type": "number",

        "values": [

            ("20 %", 0.2),

            ("40 %", 0.4),

            ("60 %", 0.6),

            ("80 %", 0.8),

        ],

    },

    {
        "id": "direction",

        "title": "🧭 Направление обработки",

        "field": "cut_direction",

        "type": "choice",

        "choices": [

            ("➡ Попутное", "CLIMB"),

            ("⬅ Встречное", "CONVENTIONAL"),

        ],

    },

    {
        "id": "allowance",

        "title": "📉 Припуск",

        "field": "allowance",

        "type": "number",

        "values": [

            ("0", 0.0),

            ("0.2", 0.2),

            ("0.5", 0.5),

            ("1.0", 1.0),

        ],

    },

    {
        "id": "finish",

        "title": "✨ Чистовой проход",

        "field": "finish_pass",

        "type": "choice",

        "choices": [

            ("✅ Да", True),

            ("❌ Нет", False),

        ],

    },

    {
        "id": "finish_tool",

        "title": "🔧 Инструмент чистовой",

        "field": "finish_tool",

        "type": "choice",

        "choices": [

            ("Тот же", False),

            ("Другой", True),

        ],

    },

    {
        "id": "corner",

        "title": "⚙ Обработка углов",

        "field": "corner_type",

        "type": "choice",

        "choices": [

            ("Острые", "SHARP"),

            ("Радиус", "RADIUS"),

            ("Фаска", "CHAMFER"),

        ],

    },

]
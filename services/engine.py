def build_plan(data):
    return {
        "strategy": "rough_finish",
        "material": data.get("material"),
        "tool": data.get("tool"),
        "allowance": data.get("allowance"),
        "feature": data.get("feature")
    }

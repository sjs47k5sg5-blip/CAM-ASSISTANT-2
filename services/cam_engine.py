
class CAMEngine:
    def build(self, data):
        return {
            "strategy": "balanced",
            "stock_to_leave": 0.2,
            "step": data.get("step", 2.0),
            "chamfer": True
        }

import json


class CuttingEngine:

    def __init__(self, db):
        self.db = db


    # =========================
    # NORMALIZE INPUT
    # =========================
    def normalize(self, value):
        try:
            return float(value)
        except:
            return value


    # =========================
    # SAFE KEY BUILDER
    # =========================
    def build_key(self, diameter, flutes):
        d = int(float(diameter))
        z = int(float(flutes))
        return f"D{d}_Z{z}"


    # =========================
    # MAIN SEARCH
    # =========================
    def get_modes(self, material, diameter, flutes):

        material = str(material).lower().strip()
        key = self.build_key(diameter, flutes)

        # 1. проверка материала
        if material not in self.db:
            return self.fallback(diameter, flutes)

        mat_data = self.db[material]

        # 2. точный поиск
        if key in mat_data:
            return mat_data[key]

        # 3. мягкий поиск (если нет ключа)
        for k in mat_data.keys():
            if str(diameter) in k and str(flutes) in k:
                return mat_data[k]

        # 4. fallback
        return self.fallback(diameter, flutes)


    # =========================
    # FALLBACK MODES
    # =========================
    def fallback(self, diameter, flutes):

        d = float(diameter)

        # очень безопасные режимы (универсальные)
        return {
            "rpm": int(8000 / (d if d > 0 else 1)),
            "feed": int(0.02 * 8000),
            "note": "fallback safe mode"
        }
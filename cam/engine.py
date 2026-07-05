class CAMEngine:
    def __init__(self):
        self.modules = {}

    def register(self, name, handler):
        self.modules[name] = handler

    async def run(self, name, data):
        if name not in self.modules:
            return "❌ Module not found"

        return await self.modules[name](data)


cam_engine = CAMEngine()
from services.cam_engine.models import (
    Project,
    Workpiece,
    Tool,
    Material,
    Corner,
    Finish,
    Machining,
    Machine,
)


class ProjectManager:

    @staticmethod
    def new_project() -> Project:

        return Project(

            workpiece=Workpiece(
                x=0.0,
                y=0.0,
                z=0.0,
                zero="CENTER",
                zero_z="TOP",
            ),

            tool=Tool(
                number=1,
                diameter=0.0,
                flutes=2,
                length_offset=1,
                spindle=3000,
                feed=300,
                plunge=120,
            ),

            material=Material(
                name="Steel",
                vc=150,
                fz=0.05,
            ),

            corner=Corner(
                kind="SHARP",
                position="ALL",
                value=0.0,
            ),

            finish=Finish(
                allowance=0.0,
                enabled=False,
                another_tool=False,
            ),

            machining=Machining(
                direction="CLIMB",
                roughing=False,
                stepover=0.6,
                step_z=2.0,
            ),

            machine=Machine(
                name="Victor Center 136",
                controller="Fanuc Oi-MF",
                safe_z=100.0,
                rapid_z=5.0,
                spindle_max=15000,
            ),
        )
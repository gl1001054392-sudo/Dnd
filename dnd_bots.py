"""
Three-bot D&D 5E chat scaffold.
Bot1 (DM) enforces 5E rules and asks the user for setting.
Bot2/3 are player bots with user-defined personalities.
"""

from dataclasses import dataclass
from typing import List, Optional


def ask(prompt: str) -> str:
    return input(f"{prompt.strip()} ")


@dataclass
class Bot:
    name: str
    role: str
    personality: str

    def speak(self, content: str) -> None:
        print(f"[{self.name} - {self.role}]: {content}")


class DungeonMaster(Bot):
    def ask_setting(self) -> str:
        setting = ask("DM: What is the setting for this adventure? (e.g., haunted forest, desert ruin)")
        return setting

    def enforce_rules(self) -> None:
        self.speak(
            "We'll follow D&D 5E rules. When rolls are needed, I'll ask you to roll and provide the result."
        )

    def request_roll(self, roll: str) -> int:
        while True:
            value = ask(f"DM: Please roll {roll} and enter the total:")
            try:
                return int(value)
            except ValueError:
                print("Please enter a number.")


class DnDSession:
    def __init__(self, dm: DungeonMaster, players: List[Bot]) -> None:
        self.dm = dm
        self.players = players
        self.setting: Optional[str] = None

    def intro(self) -> None:
        self.setting = self.dm.ask_setting()
        self.dm.enforce_rules()
        self.dm.speak(
            f"Welcome to the adventure set in {self.setting}. You may steer the story at any time."
        )
        for player in self.players:
            player.speak(
                f"I am ready! I will act according to my personality: {player.personality}."
            )

    def turn(self) -> None:
        self.dm.speak("What do you do next? You can also direct any bot or change the story's direction.")
        user_input = ask("You:")

        if user_input.lower().startswith("roll"):
            roll_type = user_input[4:].strip() or "1d20"
            result = self.dm.request_roll(roll_type)
            self.dm.speak(f"Noted. You rolled a {result} on {roll_type}.")
            return

        self.dm.speak(
            "Understood. I'll narrate and ask for rolls if necessary based on your direction."
        )

        for player in self.players:
            player.speak(
                f"In line with my personality ({player.personality}), I respond to: '{user_input}'."
            )

    def run(self) -> None:
        self.intro()
        while True:
            self.turn()
            cont = ask("Continue? (y/n):").strip().lower()
            if cont != "y":
                self.dm.speak("Session ended. Thanks for playing!")
                break


def build_bots() -> DnDSession:
    dm = DungeonMaster(name="Bot1", role="DM", personality="Rules-focused, narrative-driven")
    p1_personality = ask("Define Bot2's personality:")
    p2_personality = ask("Define Bot3's personality:")

    bot2 = Bot(name="Bot2", role="Player", personality=p1_personality)
    bot3 = Bot(name="Bot3", role="Player", personality=p2_personality)

    return DnDSession(dm=dm, players=[bot2, bot3])


if __name__ == "__main__":
    session = build_bots()
    session.run()

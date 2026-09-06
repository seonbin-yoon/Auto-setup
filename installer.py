from modules import config, console, datatype, system
from modules._except import InitError
from modules.console import Color
from modules.system import program_exit
from system import edk2, qemu

class ShellMessage:
    def __init__(self):
        self.help_message = ""

    def _cache_help_message(self):
        message: list[str] = []
        for command in __COMMANDS:
            message.append(f"{command["Command"][0]}\n")
        return "".join(message)

    def show_message(self):
        if not self.help_message:
            self.help_message = self._cache_help_message()

        console.write(self.help_message)

shell = ShellMessage()

__COMMANDS: list[datatype.ShellCommand] = [
    {
        "Need_argu": True,
        "Command": ("ie",),
        "Exec": edk2.install
    },
    {
        "Need_argu": True,
        "Command": ("iq",),
        "Exec": qemu.install
    },
    {
        "Need_argu": False,
        "Command": ("help",),
        "Exec": shell.show_message,
    },
    {
        "Need_argu": False,
        "Command":("clear", "cls"),
        "Exec": console.clear_screen,
    },
    {
        "Need_argu": False,
        "Command": ("exit", "e"),
        "Exec": program_exit
    },
    {
        "Need_argu": False,
        "Command": ("color",),
        "Exec": console.config.toogle_color_mode
    }
]

def check_done(result: bool):
    if result:
        console.write(
            "모든 변경 사항이 잘 반영되게 재로그인을 권장합니다!", Color.YELLOW
            )
        console.write("작업을 성공적으로 완료 했습니다.", Color.BLUE)

def main():
    try:
        program_contexts = datatype.Contexts(
            config=config.get_config(),
            distro=system.get_distro(),
            home=system.get_home_path(),
            program=system.get_program_path()
        )
    except InitError.ConfigNotFoundError:
        program_exit(1, "설정 파일을 찾을 수 없습니다.", Color.RED)
    except InitError.UnsupportedOSError as os_name:
        program_exit(1, f"{os_name}는 지원되는 OS가 아닙니다.", Color.RED)
    except InitError.HomePathNotFoundError:
        program_exit(1, "사용자 기본 폴더를 찾을 수 없습니다.", Color.RED)
    except Exception:
        program_exit(1, "프로그램 초기화중 오류가 발생했습니다.", Color.RED)

    config.replace_config_values(program_contexts.config, program_contexts.home)
    console.clear_screen()
    console.write("자동 설치 프로그램에 오신 것을 환영합니다!", Color.MAGENTA)
    shell.show_message()

    while True:
        _input = console.read("메뉴 입력 > ")
        if not _input:
            continue

        for command in __COMMANDS:
            if _input in command["Command"]:
                if command["Need_argu"]:
                    check_done(command["Exec"](program_contexts))
                else:
                    command["Exec"]()
                break
        else:
            console.write("없는 기능을 지정했습니다..", Color.RED)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.clear_screen()
        program_exit(130)

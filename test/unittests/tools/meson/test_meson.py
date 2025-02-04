import textwrap

from conan.tools.meson import Meson
from conan.tools.meson.helpers import to_meson_machine
from conan.internal.model.conf import ConfDefinition
from conan.test.utils.mocks import ConanFileMock, MockSettings


def test_meson_build():
    c = ConfDefinition()
    c.loads(textwrap.dedent("""\
        tools.build:jobs=10
    """))

    settings = MockSettings({"build_type": "Release",
                             "compiler": "gcc",
                             "compiler.version": "7",
                             "os": "Linux",
                             "arch": "x86_64"})
    conanfile = ConanFileMock()
    conanfile.settings = settings
    conanfile.display_name = 'test'
    conanfile.conf = c.get_conanfile_conf(None)

    meson = Meson(conanfile)
    meson.build()

    assert '-j10' in str(conanfile.command)


def test_to_meson_machine_subsystem():
    macos = to_meson_machine("Macos", "x86_64", None)
    assert "subsystem" not in macos

    macos_sdk = to_meson_machine("Macos", "x86_64", "my_cool_sdk")
    assert "subsystem" in macos_sdk
    assert macos_sdk["subsystem"] == "my_cool_sdk"

    ios = to_meson_machine("iOS", "aarch64", None)
    assert "subsystem" not in ios

    ios_simulator = to_meson_machine(iOS, "aarch64", "iphoneos-simulator")
    assert "subsystem" in ios
    assert ios_simulator["subsystem"] == "ios-simulator"

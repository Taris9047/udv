#!/usr/bin/env python3

### Installs Some pre-built editors ###
###
from .Utils import RunCmd, program_exists
from .DistroDetect import GetDistro

import os
import sys

### Sublie-text, Atom, VSCode, etc.
###
class InstallEditors(GetDistro, RunCmd):

    pkgman_to_name_map = {
        "apt": ["ubuntu", "debian", "elementary", "pop", "linuxmint"],
        "dnf": ["fedora", "rhel", "Red Hat Enterprise Linux", "CentOS Linux"],
        "zypper": ["openSUSE Leap"],
        "pacman": ["manjaro", "Arch Linux"],
    }

    def __init__(self, list_of_editors_to_install=None):
        GetDistro.__init__(self)
        RunCmd.__init__(self, shell_type="bash", verbose=True)
        if not list_of_editors_to_install:
            print("Nothing to do!")
            sys.exit(0)

        # Let's determine what kind of package manager this distro is
        # based on.
        name = self.rel_data["ID"]
        pkg_mans = self.pkgman_to_name_map.keys()

        pkgman = None
        for pm in pkg_mans:
            if name in self.pkgman_to_name_map[pm]:
                pkgman = str(pm)
                break

        editors_to_inst = []
        for edi in list_of_editors_to_install:
            if edi.lower() == "sublime-text":
                editors_to_inst.append("subl")
            else:
                editors_to_inst.append(edi.lower())

        self.methods_to_run = []
        for edi in editors_to_inst:
            self.methods_to_run.append(f"install_{edi}_{pkgman}")

        self.RunInstall()

    def RunInstall(self):
        for method in self.methods_to_run:
            self.switcher(method)

    def switcher(self, method_to_run):
        return getattr(self, method_to_run)()

    ### Now those Installation methods... ###
    ### As this moment, we can install...
    ### sublime_text, atom, vscode
    ###
    ### with apt, dnf, zypper, and pacman
    ###
    def install_subl_apt(self):
        if not program_exists("subl"):
            print("Installilng Sublime Text ...")
            cmds = [
                "wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -",
                'echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list',
                "sudo apt-get -y update && sudo apt-get -y install sublime-text sublime-merge",
            ]
            self.Run(cmds)

        else:
            print("Updating Sublime Text ...")
            self.Run("sudo apt-get -y update && sudo apt-get -y upgrade")

    def install_subl_dnf(self):
        if not program_exists("subl"):
            print("Installilng Sublime Text ...")
            cmds = [
                "sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg",
                "sudo dnf -y config-manager --add-repo https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo",
                "sudo dnf install -y sublime-text sublime-merge",
            ]
            self.Run(cmds)
        else:
            print(">>> Updating Sublimt Text ...")
            self.Run("sudo dnf -y update")

    def install_subl_pacman(self):
        if not program_exists("subl"):
            print("Installilng Sublime Text ...")
            cmds = [
                "curl -O https://download.sublimetext.com/sublimehq-pub.gpg && sudo pacman-key --add sublimehq-pub.gpg && sudo pacman-key --lsign-key 8A8F901A && rm sublimehq-pub.gpg",
                'echo -e "\n[sublime-text]\nServer = https://download.sublimetext.com/arch/stable/x86_64" | sudo tee -a /etc/pacman.conf',
                "sudo pacman -Syyu sublime-test sublime-merge",
            ]
            self.Run(cmds)
        else:
            self.Run("sudo pacman -Syyu")

    def install_subl_zypper(self):
        if not program_exists("subl"):
            print("Installilng Sublime Text ...")
            cmds = [
                "sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg",
                "sudo zypper addrepo -g -f https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo",
                "sudo zypper install sublime-text sublime-merge",
            ]

            self.Run(cmds)
        else:
            self.Run("sudo zypper refresh && sudo zypper update")

    def install_atom_apt(self):
        if not program_exists("atom"):
            print("Installilng Atom ...")
            cmds = [
                "sudo apt-get update && sudo apt-get install -y software-properties-common apt-transport-https wget",
                "wget -q https://packagecloud.io/AtomEditor/atom/gpgkey -O- | sudo apt-key add -",
                'sudo add-apt-repository "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main"',
                "sudo apt-get -y update && sudo apt-get -y install atom",
            ]
            self.Run(cmds)
        else:
            self.Run("sudo apt-get -y update && sudo apt-get -y upgrade")

    def install_atom_dnf(self):
        print("Installilng Atom ...")

        cmds = [
            'sudo dnf install -y $(curl -sL "https://api.github.com/repos/atom/atom/releases/latest" | grep "https.*atom.x86_64.rpm" | cut -d \'"\' -f 4);',
            "ATOM_INSTALLED_VERSION=$(rpm -qi atom | grep \"Version\" | cut -d ':' -f 2 | cut -d ' ' -f 2);",
            "ATOM_LATEST_VERSION=$(curl -sL \"https://api.github.com/repos/atom/atom/releases/latest\" | grep -E \"https.*atom-amd64.tar.gz\" | cut -d '\"' -f 4 | cut -d '/' -f 8 | sed 's/v//g');",
            "if [[ $ATOM_INSTALLED_VERSION < $ATOM_LATEST_VERSION ]]; then sudo dnf install -y https://github.com/atom/atom/releases/download/v${ATOM_LATEST_VERSION}/atom.x86_64.rpm;fi",
        ]

        self.Run(cmds)

    def install_atom_pacman(self):
        if not program_exists("atom"):
            print("Installilng Atom ...")
            self.Run("sudo -H pacman -Syyu atom")
        else:
            print("Updating Atom ...")
            self.Run("sudo -H pacman -Syyu")

    def install_atom_zypper(self):
        if not program_exists("atom"):
            print("Installilng Atom ...")
            cmds = [
                "sudo sh -c 'echo -e \"[Atom]\nname=Atom Editor\nbaseurl=https://packagecloud.io/AtomEditor/atom/el/7/\$basearch\nenabled=1\ntype=rpm-md\ngpgcheck=0\nrepo_gpgcheck=1\ngpgkey=https://packagecloud.io/AtomEditor/atom/gpgkey\" > /etc/zypp/repos.d/atom.repo'",
                "sudo zypper --gpg-auto-import-keys refresh",
                "sudo zypper install atom",
            ]
            self.Run(cmds)
        else:
            self.Run("sudo zypper refresh && sudo zypper update")

    def install_vscode_apt(self):
        if not program_exists("code"):
            print("Installilng Visual Studio Code ...")
            cmds = [
                "curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -",
                'sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"',
                "sudo apt-get -y update && sudo apt-get -y install code",
                "rm -rf ./packages.microsoft.gpg",
            ]
            self.Run(cmds)
        else:
            print("Updating Visual Studio Code ...")
            self.Run("")

    def install_vscode_dnf(self):
        if not program_exists("code"):
            print("Installilng Visual Studio Code ...")
            cmds = [
                "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                "sudo sh -c 'echo -e \"[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc\" > /etc/yum.repos.d/vscode.repo'",
                "sudo dnf -y check-update && sudo dnf -y install code",
            ]

            self.Run(cmds)
        else:
            print("Updating Visual Studio Code ...")
            self.Run("sudo dnf -y update")

    def install_vscode_pacman(self):
        if not program_exists("code"):
            print("Installilng Visual Studio Code ...")
            cwd = os.getcwd()
            cmds = [
                "sudo pacman -Syyu git",
                f"mkdir -pv {cwd}/.vscode_src",
                f"cd {cwd}/.vscode_src && git clone https://AUR.archlinux.org/visual-studio-code-bin.git",
                f"cd {cwd}/.vscode_src/visual-studio-code-bin",
                "makepkg -s",
                "sudo pacman -U visual-studio-code-bin-*.pkg.tar.*",
                f"cd {cwd}",
                f"rm -rf {cwd}/.vscode_src",
            ]
            self.Run(" && ".join(cmds))
        else:
            print("Updating Visual Studio Code ...")
            self.Run("sudo -H pacman -Syyu")

    def install_vscode_zypper(self):
        if not program_exists("code"):
            print("Installilng Visual Studio Code ...")
            cmds = [
                "sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc",
                "sudo zypper addrepo https://packages.microsoft.com/yumrepos/vscode vscode",
                "sudo zypper refresh && sudo zypper install code",
            ]
            self.Run(cmds)
        else:
            print("Updating Visual Studio Code ...")
            self.Run("sudo zypper refresh && sudo zypper update")

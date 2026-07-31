# cp2077dot

Personal Cyberpunk 2077-styled dotfiles managed with [chezmoi](https://www.chezmoi.io/).

Contains my Linux configuration, shell setup, window manager, system configs, and provisioning.

## !! IMPORTANT !!

This setup is only for Arch / Arch-based distros.

## What's included

| Category | Tools / Configs |
|---|---|
| **Shell** | bash, git |
| **WM / Desktop** | niri, sddm (sddm-astronaut-theme), ghostty, mako |
| **System** | pacman.conf, paru.conf, sudoers, vconsole, locale, hostname, mkinitcpio, modprobe, zram-generator |
| **Apps** | fastfetch, fuzzel, spicetify, dolphin, noctalia (Cyberpunk colorscheme) |
| **Boot** | CyberGRUB-2077 theme & config |
| **Provisioning** | Ansible playbook (packages, AUR, flatpak, themes) |

## Setup

```bash
# Install chezmoi
sudo pacman -S chezmoi
```

```bash
# Apply dotfiles (installs Ansible and runs the playbook automatically)
chezmoi init --apply git@github.com:murcdemurc/cp2077dot.git
```

You'll be prompted for your sudo password where needed.

## Daily use

```bash
chezmoi update         # pull & apply latest changes
chezmoi git push       # push local changes
chezmoi status         # check what's modified
chezmoi diff           # see pending changes
```

## How it works

`chezmoi init --apply` copies all dotfiles into place and then runs
`.chezmoiscripts/run_after_10_bootstrap-ansible.sh.tmpl`, which:

1. Installs Ansible if missing
2. Installs the required collections (`kewlfft.aur`, `community.general`) from `ansible/requirements.yml`
3. Runs `ansible-playbook -i localhost, -c local ansible/site.yml --ask-become-pass`

All provisioning is idempotent and controlled via feature flags in `ansible/site.yml`.

## Structure

```
~/.local/share/chezmoi/
|-- ansible/                       # Ansible provisioning
|   |-- site.yml                   # playbook with feature toggles
|   |-- ansible.cfg                # ask_become_pass, local inventory
|   |-- requirements.yml           # Ansible collections
|   `-- roles/
|       |-- essential/             # base packages, services, paru bootstrap, sudoers
|       |-- grub_theme/            # CyberGRUB-2077 theme & config (+ regen grub.cfg)
|       |-- sddm_theme/            # SDDM sddm-astronaut-theme, deps, theme.conf
|       |-- noctalia_git/          # noctalia-git (AUR) + wallpaper
|       |-- noctalia_shell/        # noctalia-shell (AUR) + wallpaper
|       |-- aur_leisure/           # librewolf-bin, deezer, spotify
|       |-- aur_work/              # onlyoffice-bin
|       |-- gaming/                # linux-rt, steam, gamescope, wine, lact, ...
|       |-- utils/                 # btop, fastfetch, fuzzel, ranger, ...
|       |-- productivity/          # thunderbird, reaper, waydroid, flatpak apps
|       `-- ltr/                   # placeholder
|-- dot_bash*                      # shell configs
|-- dot_gitconfig                  # git config
|-- dot_local/                     # ~/.local/ state (noctalia, etc.)
|-- private_dot_config/            # ~/.config/ (niri, ghostty, noctalia, spicetify, ...)
|-- etc_*                          # /etc/ configs (pacman, sudoers, systemd, ...)
`-- .chezmoiscripts/               # post-apply scripts (Ansible bootstrap)
```

## Notes

- The Ansible playbook requires `ask_become_pass` (configured in `ansible.cfg`).
- Some files are marked `private_` (age-encrypted secrets).
- `.chezmoiignore` excludes runtime state files (e.g. Noctalia git plugins, notification history).

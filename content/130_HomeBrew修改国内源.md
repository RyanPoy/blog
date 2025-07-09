+++
title = "HomeBrew修改国内源"
date = 2020-12-19
categories = ["Tech"]
tags = ["配置"]
+++

# 对于 homebrew，需要替换的是4个模块的镜像：

- Homebrew
- Homebrew Core
- Homebrew-bottles
- Homebrew Cask


### 替换 Homebrew
git -C "$(brew --repo)" remote set-url origin https://mirrors.ustc.edu.cn/brew.git

### 替换 Homebrew Core
git -C "$(brew --repo homebrew/core)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

### 替换 Homebrew Cask
git -C "$(brew --repo homebrew/cask)" remote set-url origin https://mirrors.ustc.edu.cn/homebrew-cask.git

### 替换 Homebrew-bottles

- 对于 bash 用户：

echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile

- 对于 zsh 用户：

echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc




## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Class Diagram](#diagram)
- [Contributing](#contributing)
- [License](#license)

## Requirements
<a id='requirements'></a>
To use the Nextcloud Talk Bot, you will need:

 - A Nextcloud instance with the Talk app installed
 - A bot user with apppassword setup
 - Python 3.7 or higher
 - Pip modules: "cryptography" and "requests"



## Installation
<a id='installation'></a>

Via PIP:

```
pip install nextcloudtalkbot
```

or manually:

Clone this repository:

```
git clone https://github.com/sowoi/nextcloud-talk-bot.git
```

Not a developer?
There is a fully automated bash script that you can run on your NextcloudServer to do the installation and configuration: See [Commands](NextcloudCommands).
For those who don't want to use a bash script, there is also an Ansible script: See [AnsiblePlaybook](AnsiblePlaybook). 


## Configuration
<a id='configuration'></a>

There is an interactive script which guides you through the configuration, see [FirstRunSetup](FirstRunSetup)



## Usage
<a id='usage'></a>
The FirstRunSetup does not have to be performed, but it makes it easier to use.

```
from nextcloud_talk_bot.Nextcloudtalkbot import NextcloudTalkBot


bot = NextcloudTalkBot()
url = bot.NEXTCLOUD_URL
username = bot.USERNAME
password = bot.PASSWORD

user = NextcloudUser(url, username, password)
preferred_language = user.get_preferred_language()

```

## Class Diagram
<a id='diagarm'></a>

![ClassDiagram](./diagrams/ClassDiagram.png)


## Contributing
<a id='contributing'></a>

Create a PullRequest on the [Git](https://github.com/sowoi/nextcloud-talk-bot).  
You are also welcome to translate.  
Contact me via my [website](https://okxo.de).  

## License

Licensed under the terms of GNU General Public License v3.0.



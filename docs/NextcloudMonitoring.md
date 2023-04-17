# Nextcloud Talk Bot: Monitoring

NextcloudMonitoring interacts with Nextcloud's monitoring API to fetch server information. It allows users to check the current status of their Nextcloud instance, including memory usage, storage space, CPU load, and available app updates.

## Initialization

To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- nextcloud_url = "https://your-nextcloud-instance.com"
- nc_token = "your-token-here"  # Replace with your own nc token created via ocs command on your server (this is not your bot app token!)

```
monitoring = NextcloudMonitoring(nextcloud_url, nc_token)
```

If the token is not provided, the class will attempt to read the token from a .monitoring file in the user's home directory.


## Usage

```
# Via module
from nextcloud_talk_bot.nextcloud_monitoring import NextcloudMonitoring

# create instance
monitoring = NextcloudMonitoring(nextcloud_url, nc_token)

monitoring.check_monitoring()
```
    
## Methods

1. get_monitoring_data_raw()  
Prints raw data of your Nextcloud instance  
2. check_monitoring()  
This method will print the memory usage, storage space, CPU load, and available app updates, along with any applicable warnings.
returns: mesage dictionary with message_id and actor

## Warnings

The check_monitoring() method will generate warnings under the following conditions:

- less than 20% of memory is free.
- the system is swapping.
- Less than 10 GB of storage space is free.
- the CPU load is greater than 10.
- App updates are available.


## Nextcloud Talk Command

If you want to use monitoring via nextcloud commands, follow the steps under [Commands](NextcloudCommands)  or if you want to implement it afterwards, start the bash script with the --monitoring flag.

You can manually create a token using the `occ config:app:set serverinfo token --value <YourToken>` command
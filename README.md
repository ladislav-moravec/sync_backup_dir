# Automatic backup of your folder to keep your data safe! 

## To run (cmd):
`python sync_backup_script.py /path/to/source /path/to/replica 60 /path/to/logfile`

## example usage:
`python sync_backup_script.py .\test_sync_dir .\test_created_backup_dir 60 .\logfile`

### files only to demo show (can be deleted/edited): 
* **test_sync_dir** (dir I want to sync),
* **test_created_backup_dir** (dir which was synced),
* **logfile** (contains actions which script did with timestamp)
  * can be edited but **logfile** must exists!

# Media_Downloader

Media_Downloader python script finds image, audio and videos URLs scraped by file type Selector in a CSV file and downloads them.
Files are nemed/renamed as `.csv file link source`.

### Windows usage

1. Download & install python 3.x from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download `Media_Downloader.py` script from:
[https://github.com/amiMohammad/Media_Downloader][Media_Downloader]
3. Scrape the target site and export data as CSV file
4. Edit CSV file so that, CSV file has no `Serial column` or `Header row`. Only `Link column` is present
5. Drag and drop the CSV file on top of the `Media_Downloader.py`
![Fig. 1: windows image download][windows-image-download-script]

### Windows troubleshooting

If the script doesn't run or Windows says `python is not recognized or found`:

#### Step 1: Open `CMD (Run as administrator)`

1. Right-click the `Start menu` and select `CMD (Run as administrator)` or `Terminal (Admin)`
![How to run CMD as Admin][run-cmd-admin]

2. Click `Yes` if asked for permission

#### Step 2: Check Python In the CMD window, type or Copy>Paste:

```bat
python --version
```
Press `Enter`

If it shows a Python 3 version, Python is installed correctly. Skip to Step 3.

If it says `python is not recognized`, reinstall Python:

1. Go to [python.org/downloads](https://www.python.org/downloads/windows/)
2. Download the latest `Python 3.x installer`
3. Run the installer
4. **IMPORTANT:** Check the box `Add python.exe to PATH`
![Python PATH install option][python-path-install]
5. Click `Install Now`
6. Close and reopen CMD as Admin, then run `python --version` again

#### Step 3: Go to where your script & CSV file are > Run the Script In CMD.

or

#### Assuming files are in Downloads > Run the Script In CMD:

```bat
cd C:\Users\YourName\Downloads
py -3 Media_Downloader.py scraped_data.csv
```

Replace `YourName` with your `Windows username` and the file paths with your `actual file location` (ex; Downloads, Desktop....).

#### Still having issues?

- Python opens the Microsoft Store: Disable the App alias in **Settings > Apps > App execution aliases** and turn off `python.exe` and `python3.exe`
- Multiple Python versions installed: Use `py -3` instead of `python`
- Permission denied error: Make sure you opened CMD as **Admin**

### macOS, Linux usage

1. Install python if necessary through your package manager. Most likely you already have it pre-installed.
2. Download `Media_Downloader.py` script from here:
[https://github.com/amiMohammad/Media_Downloader][Media_Downloader]
3. Move `Media_Downloader.py` to `Downloads` directory
4. Scrape the target site and export data as CSV file
5. Save the CSV file in `Downloads` directory
6. Edit CSV file so that, CSV file has no `Serial column` or `Header row`. Only `Link column` is present
7. Open `Terminal` application. You should have one pre-installed
8. Change working PATH to `Downloads` directory by typing:

    ```bash
    cd Downloads
    ```
10. Run image downloader script by typing:
    ````bash
    python Media_Downloader scraped_data.csv
    ````

![Fig. 2: macOS image download][osx-image-download-script]

 [windows-image-download-script]: Tutorials/Windows_Tutorial.gif?raw=true
 [run-cmd-admin]: Tutorials/CMD_as_Admin.webp?raw=true
 [python-path-install]: Tutorials/Python_vs_Java.gif?raw=true
 [osx-image-download-script]: Tutorials/OSX_Tutorial.gif?raw=true
 [Media_Downloader]: https://github.com/amiMohammad/Media_Downloader/releases

import os
import sys
import argparse
import signal
import time
import readchar
import requests

sys.stdout = open(1, "w", encoding="utf-8", closefd=False)

def handler(signum, frame):
    print("\nInterrupting the process. Do you really want to exit? (y/n) ")
    res = readchar.readchar()
    if res.lower() == 'y':
        print("Stopping the process!")
        exit(1)
    else:
        print("Continuing execution...")

signal.signal(signal.SIGINT, handler)


class GoProPlus:
    def __init__(self, auth_token, user_id):
        self.base = "api.gopro.com"
        self.host = "https://{}".format(self.base)
        self.auth_token = auth_token
        self.user_id = user_id

    def default_headers(self):
        return {
            "Accept": "application/vnd.gopro.jk.media+json; version=2.0.0",
            "Accept-Language": "en-US,en;q=0.9,bg;q=0.8,es;q=0.7",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

    def default_cookies(self):
        return {
            "gp_access_token": self.auth_token,
            "gp_user_id": self.user_id,
        }

    def validate(self):
        url = f"{self.host}/media/user"
        resp = requests.get(
            url,
            headers=self.default_headers(),
            cookies=self.default_cookies(),
        )

        if resp.status_code != 200:
            print("Failed to validate auth token. Issue a new one.")
            print(f"Status code: {resp.status_code}")
            return False

        return True

    def parse_error(self, resp):
        try:
            err = resp.json()
        except:
            err = resp.text
        return err

    def get_filenames_from_media(self, media):
        return [x.get("filename") for x in media if x.get("filename")]

    def get_media(self, start_page=1, pages=1, per_page=10):
        url = "{}/media/search".format(self.host)

        output_media = {}
        total_pages = 0
        current_page = start_page
        while True:
            params = {
                "per_page": per_page,
                "page": current_page,
                "fields": "id,created_at,content_title,filename,file_extension",
            }

            resp = requests.get(
                url,
                params=params,
                headers=self.default_headers(),
                cookies=self.default_cookies()
            )
            if resp.status_code != 200:
                err = self.parse_error(resp)
                print("Failed to get media for page {}: {}. Try renewing the auth token".format(current_page, err))
                return []

            content = resp.json()
            output_media[current_page] = content.get("_embedded", {}).get("media", [])
            
            if total_pages == 0:
                total_pages = content.get("_pages", {}).get("total_pages", 1)

            if current_page >= total_pages or current_page >= (start_page + pages) - 1:
                break

            current_page += 1

        return output_media

    def download_media_ids(self, ids, filepath, progress_mode="inline"):
        url = "{}/media/x/zip/source".format(self.host)
        params = {
            "ids": ",".join(ids),
            "access_token": self.auth_token,
        }

        try:
            resp = requests.get(
                url,
                params=params,
                headers=self.default_headers(),
                cookies=self.default_cookies(),
                stream=True)

            if resp.status_code != 200:
                print("Request failed with status code: {} and error: {}".format(resp.status_code, self.parse_error(resp)))
                return False

            downloaded_size = 0
            with open(filepath, 'wb') as file:
                for chunk in resp.iter_content(chunk_size=8192):
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress = ((downloaded_size / 1024) / 1024)

                    if progress_mode == "inline":
                        print(f"\rDownloaded: {progress:.2f}MB ({downloaded_size} bytes)", end='')
                    elif progress_mode == "newline":
                        print(f"Downloaded: {progress:.2f}MB ({downloaded_size} bytes)")

            print("\nDownload completed!")
            return True
        except Exception as e:
            print("\nDownload failed due to an exception: {}".format(e))
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    print("Removed partially downloaded file: {}".format(filepath))
                except Exception as rm_err:
                    print("Failed to remove partial file: {}".format(rm_err))
            return False


def main():
    # Load .env file manually to support zero-dependency environments
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

    # Interactively prompt for credentials if not found in environment
    if "AUTH_TOKEN" not in os.environ or "USER_ID" not in os.environ:
        print("=== GoPro Batch Downloader Setup ===")
        print("Credentials not found in environment or .env file.")
        print("Please paste them below to set them up. They will be saved to '.env' so you won't be asked again.")
        print("--------------------------------------------------------------------------------------------------")
        
        auth_token = input("1. Enter your GoPro gp_access_token (AUTH_TOKEN):\n> ").strip()
        while not auth_token:
            auth_token = input("Token cannot be empty. Paste gp_access_token:\n> ").strip()
            
        user_id = input("\n2. Enter your GoPro gp_user_id (USER_ID):\n> ").strip()
        while not user_id:
            user_id = input("User ID cannot be empty. Enter gp_user_id:\n> ").strip()
            
        download_path = input("\n3. Enter target download directory [default: G:/goprodownloads]:\n> ").strip()
        if not download_path:
            download_path = "G:/goprodownloads"

        # Write to .env
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"AUTH_TOKEN={auth_token}\n")
            f.write(f"USER_ID={user_id}\n")
            f.write(f"DOWNLOAD_PATH={download_path}\n")
            
        print("\nConfiguration saved successfully to '.env'!")
        print("==================================================================================================\n")
        
        os.environ["AUTH_TOKEN"] = auth_token
        os.environ["USER_ID"] = user_id
        os.environ["DOWNLOAD_PATH"] = download_path

    auth_token = os.environ["AUTH_TOKEN"]
    user_id = os.environ["USER_ID"]
    download_path = os.environ.get("DOWNLOAD_PATH", "G:/goprodownloads")

    parser = argparse.ArgumentParser(prog="gopro", description="GoPro Batch Downloader")
    parser.add_argument("--limit", type=int, help="Limit the number of files to download (defaults to all)", default=None)
    args = parser.parse_args()

    gpp = GoProPlus(auth_token, user_id)
    if not gpp.validate():
        return -1

    # Ensure download folder exists
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path, exist_ok=True)
            print(f"Created download directory at: {download_path}")
        except Exception as e:
            print(f"Failed to create download folder at '{download_path}': {e}")
            return -1

    print(f"Target Download Directory: {download_path}")
    print("Connecting to GoPro Plus Cloud Library...")

    import zipfile
    downloaded_count = 0
    page = 1
    
    while True:
        # Fetch metadata in batches of 10 items at a time
        media_pages = gpp.get_media(start_page=page, pages=1, per_page=10)
        if not media_pages or page not in media_pages:
            break
            
        media = media_pages[page]
        if not media:
            break

        print(f"\nProcessing page {page} metadata (found {len(media)} items)...")

        for item in media:
            # Stop if we hit the limit
            if args.limit is not None and downloaded_count >= args.limit:
                print(f"\nReached specified download limit of {args.limit} files. Stopping.")
                return

            filename = item.get("filename")
            item_id = item.get("id")
            if not filename or not item_id:
                continue

            final_filepath = os.path.join(download_path, filename)
            if os.path.exists(final_filepath):
                print(f"-> Skipping '{filename}' (already downloaded).")
                downloaded_count += 1
                continue

            temp_zip_filepath = os.path.join(download_path, f"temp_{item_id}.zip")
            print(f"\nDownloading '{filename}'...")
            
            max_retries = 3
            success = False
            for attempt in range(1, max_retries + 1):
                if attempt > 1:
                    print(f"Download attempt {attempt} of {max_retries} for {filename}...")
                if gpp.download_media_ids([item_id], temp_zip_filepath, progress_mode="inline"):
                    try:
                        print(f"Extracting '{filename}' from zip...")
                        with zipfile.ZipFile(temp_zip_filepath, 'r') as zip_ref:
                            zip_ref.extractall(download_path)
                        success = True
                        break
                    except Exception as ext_err:
                        print(f"Failed to extract zip file: {ext_err}")
                    finally:
                        if os.path.exists(temp_zip_filepath):
                            try:
                                os.remove(temp_zip_filepath)
                            except Exception as rm_err:
                                print(f"Failed to remove temp zip: {rm_err}")
                else:
                    print(f"Attempt {attempt} failed for {filename}.")
                    if attempt < max_retries:
                        time.sleep(5)

            if success:
                downloaded_count += 1
            else:
                print(f"Failed to download {filename} after {max_retries} attempts. Skipping.")

        page += 1

    print(f"\nFinished! Successfully processed {downloaded_count} files.")


if __name__ == "__main__":
    main()

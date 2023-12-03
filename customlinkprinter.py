from icrawler.builtin import ImageDownloader
from google_images_download import google_images_download
class CustomLinkPrinter(ImageDownloader):
    file_urls = []

    def get_filename(self, task, default_ext):
        file_idx = self.fetched_num + self.file_idx_offset
        return '{:04d}.{}'.format(file_idx, default_ext)

    def download(self, task, default_ext, timeout=5, max_retry=3, overwrite=False, **kwargs):
        """Download the image and save it to the corresponding path.

        Args:
            task (dict): The task dict got from ``task_queue``.
            timeout (int): Timeout of making requests for downloading images.
            max_retry (int): the max retry times if the request fails.
            **kwargs: reserved arguments for overriding.
        """
        file_url = task["file_url"]
        task["success"] = False
        task["filename"] = None
        retry = max_retry

        if not overwrite:
            with self.lock:
                self.fetched_num += 1
                filename = self.get_filename(task, default_ext)
                if self.storage.exists(filename):
                    self.logger.info("skip downloading file %s", filename)
                    return
                self.fetched_num -= 1

        while retry > 0 and not self.signal.get("reach_max_num"):
            try:
                response = self.session.get(file_url, timeout=timeout)
            except Exception as e:
                self.logger.error(
                    "Exception caught when downloading file %s, " "error: %s, remaining retry times: %d",
                    file_url,
                    e,
                    retry - 1,
                )
            else:
                if self.reach_max_num():
                    self.signal.set(reach_max_num=True)
                    break
                elif response.status_code != 200:
                    self.logger.error("Response status code %d, file %s", response.status_code, file_url)
                    break
                elif not self.keep_file(task, response, **kwargs):
                    break
                with self.lock:
                    self.fetched_num += 1
                    filename = self.get_filename(task, default_ext)
                self.logger.info("image #%s\t%s", self.fetched_num, file_url)
                task["success"] = True
                task["filename"] = filename
                self.file_urls.append(file_url)  # ADDED
                break
            finally:
                retry -= 1
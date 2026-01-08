import logging
import requests 


logger = logging.getLogger(__name__)


def check_urls(urls: list[str], timeout: int = 5) -> dict[str, str]:
    """
    Check the availability of a list of URLs and their status.

    Args:
        url (list[str]): List of URLs to check.
        timeout (int): Timeout for the HTTP request in seconds.

    Returns:
        dict[str, str]: A dictionary with URLs as keys and their availability as boolean values.
    """
    # results = {}
    # for link in url:
    #     try:
    #         response = requests.get(link, timeout=timeout)
    #         results[link] = response.status_code == 200
    #         logger.info(f"Checked {link}: {response.status_code}")
    #     except requests.RequestException as e:
    #         results[link] = False
    #         logger.error(f"Error checking {link}: {e}")
    # return results.  ---- these lines are pre populated and should not be use ----

    logger.info(f"Starting URL checks for {len(urls)} URLs with timeout {timeout} seconds.")
    results = {}
    for url in urls:
        status = "unreachable"
        try:
            logger.debug(f"checking url: {url}")
            response = requests.get(url, timeout=timeout)

            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "timeout"
            logger.warning(f"Timeout occurred for URL: {url}")
        except requests.exceptions.ConnectionError:
            status = "connection error"
            logger.warning(f"Connection error occurred for URL: {url}")
        except requests.RequestException as e:
            status = f"request_error:{type(e).__name__}"
            logger.error(f"An error occurred for URL: {url} - {e}", exc_info=True)

        results[url] = status
        logger.debug(f"checked:{url:<40}->{status}")

    logger.info("Completed URL checks.")
    return results


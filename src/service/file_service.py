from enum import Enum


class FilePath(Enum):
    URLS = "src/output/urls.txt"


def save_to_file(file_path: FilePath, data: list):
    with open(file_path.value, "w") as f:
        for item in data:
            f.write(f"{item}\n")
    print(f"Data saved to {file_path.value}")


def read_from_file(file_path: FilePath):
    data = []
    with open(file_path.value, "r") as f:
        for line in f:
            data.append(line.strip())
    return data


def save_urls_to_file(urls: list):
    save_to_file(FilePath.URLS, urls)


def read_urls_from_file():
    return read_from_file(FilePath.URLS)

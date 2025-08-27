from typing import Optional


class JobPosting:
    title: str
    externalPath: str
    locationsText: Optional[str]
    postedOn: str

    def __init__(self, title: str, externalPath: str, locationsText: Optional[str], postedOn: str) -> None:
        self.title = title
        self.externalPath = externalPath
        self.locationsText = locationsText
        self.postedOn = postedOn

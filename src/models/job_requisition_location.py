class JobRequisitionLocation:
    descriptor: str
    country: str
    countryCode: str

    def __init__(self, descriptor: str, country: str, countryCode: str) -> None:
        self.descriptor = descriptor
        self.country = country
        self.countryCode = countryCode

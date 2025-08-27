from datetime import datetime

from src.models.job_requisition_location import JobRequisitionLocation


class JobPostingInfo:
    id: str
    title: str
    jobDescription: str
    location: str
    postedOn: str
    startDate: datetime | None
    timeType: str
    jobReqId: str
    jobPostingId: str | None
    jobPostingSiteId: str | None
    country: str
    canApply: bool
    jobRequisitionLocation: JobRequisitionLocation | None
    remoteType: str
    externalUrl: str
    jobSource: str
    hiringOrganization: str | None

    def __init__(self, id: str, title: str, jobDescription: str, location: str, postedOn: str, startDate: datetime | None,
                 timeType: str, jobReqId: str, jobPostingId: str | None, jobPostingSiteId: str | None, country: str, canApply: bool,
                 jobRequisitionLocation: JobRequisitionLocation | None, remoteType: str, externalUrl: str,
                 jobSource: str, hiringOrganization: str | None) -> None:
        self.id = id
        self.title = title
        self.jobDescription = jobDescription
        self.location = location
        self.postedOn = postedOn
        self.startDate = startDate
        self.timeType = timeType
        self.jobReqId = jobReqId
        self.jobPostingId = jobPostingId
        self.jobPostingSiteId = jobPostingSiteId
        self.country = country
        self.canApply = canApply
        self.jobRequisitionLocation = jobRequisitionLocation
        self.remoteType = remoteType
        self.externalUrl = externalUrl
        self.jobSource = jobSource
        self.hiringOrganization = hiringOrganization

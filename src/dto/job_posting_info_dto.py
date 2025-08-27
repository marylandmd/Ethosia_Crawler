from src.models.job_info import JobPostingInfo
from src.models.job_requisition_location import JobRequisitionLocation


class JobPostingInfoDTO:

    @staticmethod
    def to_mongo_dicts(job_posting_infos: list[JobPostingInfo]) -> list[dict]:
        return [JobPostingInfoDTO.to_mongo_dict(job_posting_info) for job_posting_info in job_posting_infos]

    @staticmethod
    def to_mongo_dict(job_posting: JobPostingInfo) -> dict:
        return {
            '_id': job_posting.id,
            'title': job_posting.title,
            'jobDescription': job_posting.jobDescription,
            'location': job_posting.location,
            'postedOn': job_posting.postedOn,
            'startDate': job_posting.startDate if job_posting.startDate else None,
            'timeType': job_posting.timeType,
            'jobReqId': job_posting.jobReqId,
            'jobPostingId': job_posting.jobPostingId,
            'jobPostingSiteId': job_posting.jobPostingSiteId,
            'country': job_posting.country,
            'canApply': job_posting.canApply,
            'jobRequisitionLocation': vars(job_posting.jobRequisitionLocation) if job_posting.jobRequisitionLocation else None,
            'remoteType': job_posting.remoteType,
            'externalUrl': job_posting.externalUrl,
            'jobSource': job_posting.jobSource,
            'hiringOrganization': job_posting.hiringOrganization
        }

    def from_mongo_dicts(data: list[dict]) -> list[JobPostingInfo]:
        return [JobPostingInfoDTO.from_mongo_dict(job_posting_info) for job_posting_info in data]

    @staticmethod
    def from_mongo_dict(data: dict) -> JobPostingInfo:
        return JobPostingInfo(
            id=data.get('_id') if data.get('_id') else data.get('id'),
            title=data.get('title'),
            jobDescription=data.get('jobDescription'),
            location=data.get('location'),
            postedOn=data.get('postedOn'),
            startDate=data.get('startDate'),
            timeType=data.get('timeType'),
            jobReqId=data.get('jobReqId'),
            jobPostingId=data.get('jobPostingId'),
            jobPostingSiteId=data.get('jobPostingSiteId'),
            country=data.get('country'),
            canApply=data.get('canApply'),
            jobRequisitionLocation=JobRequisitionLocation(**data.get('jobRequisitionLocation')) if data.get('jobRequisitionLocation') else None,
            remoteType=data.get('remoteType'),
            externalUrl=data.get('externalUrl'),
            jobSource=data.get('jobSource'),
            hiringOrganization=data.get('hiringOrganization')
        )

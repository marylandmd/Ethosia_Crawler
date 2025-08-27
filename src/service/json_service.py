import json
from datetime import datetime
from typing import Dict, Any, Optional

from src.models.job_info import JobPostingInfo
from src.models.job_requisition_location import JobRequisitionLocation


def json_to_posting_info(json_data: Dict[str, Any], source="") -> JobPostingInfo:
    # Extract data from JSON
    job_posting_info_json = json_data.get("jobPostingInfo", {})

    # Convert nested models
    job_requisition_location_json = job_posting_info_json.get("jobRequisitionLocation", {})
    job_requisition_location_country_json = job_requisition_location_json.get("country", {})
    job_requisition_location = JobRequisitionLocation(
        descriptor=job_requisition_location_json.get("descriptor", ""),
        country=job_requisition_location_country_json.get("descriptor", ""),
        countryCode=job_requisition_location_country_json.get("alpha2Code", "")
    )
    job_hiring_organization = json_data.get("hiringOrganization", "").get("name", "")

    # Create JobPostingInfo instance
    job_posting_info = JobPostingInfo(
        id=job_posting_info_json.get("id", ""),
        title=job_posting_info_json.get("title", ""),
        jobDescription=job_posting_info_json.get("jobDescription", ""),
        location=job_posting_info_json.get("location", ""),
        postedOn=job_posting_info_json.get("postedOn", ""),
        startDate=datetime.strptime(job_posting_info_json.get("startDate", ""), "%Y-%m-%d"),
        timeType=job_posting_info_json.get("timeType", ""),
        jobReqId=job_posting_info_json.get("jobReqId", ""),
        jobPostingId=job_posting_info_json.get("jobPostingId", ""),
        jobPostingSiteId=job_posting_info_json.get("jobPostingSiteId", ""),
        country=job_posting_info_json.get("country", ""),
        canApply=job_posting_info_json.get("canApply", False),
        jobRequisitionLocation=job_requisition_location,
        remoteType=job_posting_info_json.get("remoteType"),
        externalUrl=job_posting_info_json.get("externalUrl", ""),
        jobSource=source,
        hiringOrganization=job_hiring_organization
    )

    return job_posting_info

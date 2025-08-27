from typing import List

from src.models.job_posting import JobPosting


class Job:
    total: int
    jobPostings: List[JobPosting]

    def __init__(self, total: int, jobPostings: List[JobPosting]) -> None:
        self.total = total
        self.jobPostings = jobPostings

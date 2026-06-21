"""Tests for the scm_agent orchestrator package."""

from scm_agent.types import JobRequest, JobResult


def test_job_request_defaults():
    req = JobRequest(brief="set up reorder points")
    assert req.brief == "set up reorder points"
    assert req.data_path is None
    assert req.job_type is None
    assert req.params == {}
    assert req.client == "Client"


def test_job_result_holds_status_and_deliverables():
    res = JobResult(
        status="ok",
        tool="inventory_optimization",
        confidence=0.9,
        deliverables={"report": "out/report.md"},
        summary="done",
    )
    assert res.status == "ok"
    assert res.qa_issues == []
    assert res.clarifications == []
    assert res.deliverables["report"].endswith("report.md")

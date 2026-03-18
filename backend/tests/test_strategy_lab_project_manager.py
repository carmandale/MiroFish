from app.models.project import Project, ProjectManager
from app.models.strategy_lab import (
    DocumentSegment,
    ExtractedDocument,
    LocatorType,
    WorkflowMode,
)


def test_project_manager_persists_workflow_mode_and_strategy_lab_paths(
    monkeypatch,
    tmp_path,
):
    projects_dir = tmp_path / "projects"
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(projects_dir))

    project = ProjectManager.create_project(
        name="Strategy Lab",
        workflow_mode=WorkflowMode.STRATEGY_LAB,
    )

    loaded = ProjectManager.get_project(project.project_id)
    assert loaded is not None
    assert loaded.workflow_mode == WorkflowMode.STRATEGY_LAB

    strategy_lab_dir = projects_dir / project.project_id / "strategy_lab"
    assert strategy_lab_dir.exists()
    assert (strategy_lab_dir / "current").exists()
    assert (strategy_lab_dir / "runs").exists()


def test_project_manager_defaults_legacy_projects_and_roundtrips_documents(
    monkeypatch,
    tmp_path,
):
    projects_dir = tmp_path / "projects"
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(projects_dir))

    project = ProjectManager.create_project(name="Legacy Compatible")

    legacy_payload = project.to_dict()
    legacy_payload.pop("workflow_mode")
    legacy_project = Project.from_dict(legacy_payload)
    assert legacy_project.workflow_mode == WorkflowMode.DEFAULT

    extracted_document = ExtractedDocument(
        document_id="doc_alpha",
        original_filename="alpha.docx",
        saved_filename="saved.docx",
        file_path="/tmp/alpha.docx",
        extension="docx",
        text="Alpha\n\nBeta",
        segments=[
            DocumentSegment(
                locator_type=LocatorType.HEADING,
                locator="heading:1",
                start_char=0,
                end_char=5,
                text="Alpha",
            ),
            DocumentSegment(
                locator_type=LocatorType.PARAGRAPH,
                locator="paragraph:2",
                start_char=7,
                end_char=11,
                text="Beta",
            ),
        ],
    )

    ProjectManager.save_extracted_documents(project.project_id, [extracted_document])
    loaded_documents = ProjectManager.get_extracted_documents(project.project_id)

    assert len(loaded_documents) == 1
    assert loaded_documents[0].original_filename == "alpha.docx"
    assert loaded_documents[0].segments[0].locator == "heading:1"

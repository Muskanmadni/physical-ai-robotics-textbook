from typing import List, Optional
from src.models.chapter import Chapter
from src.models.module import Module

def get_all_modules() -> List[Module]:
    """
    Retrieve all modules from the database.
    In a real implementation, this would query the database.
    """
    # This would typically query the database:
    # return db.query(Module).order_by(Module.order).all()
    
    # For now, returning mock data:
    return [
        Module(
            id="mod-ros2",
            title="ROS 2",
            description="Robot Operating System version 2",
            order=1,
            createdAt="2023-01-01T00:00:00Z",
            updatedAt="2023-01-01T00:00:00Z"
        ),
        Module(
            id="mod-gazebo-unity",
            title="Gazebo / Unity Simulation",
            description="Simulation environments for robotics",
            order=2,
            createdAt="2023-01-01T00:00:00Z",
            updatedAt="2023-01-01T00:00:00Z"
        ),
        Module(
            id="mod-nvidia-isaac",
            title="NVIDIA Isaac Robotics",
            description="Advanced robotics platform by NVIDIA",
            order=3,
            createdAt="2023-01-01T00:00:00Z",
            updatedAt="2023-01-01T00:00:00Z"
        ),
        Module(
            id="mod-vla-systems",
            title="Vision-Language-Action Systems",
            description="Integration of perception, reasoning, and action",
            order=4,
            createdAt="2023-01-01T00:00:00Z",
            updatedAt="2023-01-01T00:00:00Z"
        )
    ]

def get_chapters_for_module(module_id: str) -> List[Chapter]:
    """
    Retrieve all chapters for a specific module.
    """
    # This would typically query the database:
    # return db.query(Chapter).filter(Chapter.module == module_id).order_by(Chapter.order).all()
    
    # For now, returning mock data:
    chapter_titles = {
        "mod-ros2": [
            "Introduction to ROS 2",
            "Nodes and Topics",
            "Practical Examples"
        ],
        "mod-gazebo-unity": [
            "Gazebo Basics",
            "Unity Simulation",
            "Comparison Study"
        ],
        "mod-nvidia-isaac": [
            "Isaac Sim Overview",
            "Robotics Scenarios",
            "Deployment Guide"
        ],
        "mod-vla-systems": [
            "Vision Models",
            "Language Models",
            "Action Planning"
        ]
    }
    
    if module_id not in chapter_titles:
        return []
    
    chapters = []
    for idx, title in enumerate(chapter_titles[module_id]):
        chapters.append(Chapter(
            id=f"{module_id}-ch{idx+1}",
            title=title,
            content="This is placeholder content for the chapter.",
            module=module_id,
            order=idx+1,
            language="en",
            createdAt="2023-01-01T00:00:00Z",
            updatedAt="2023-01-01T00:00:00Z",
            metadata={}
        ))
    
    return chapters

def get_chapter_by_id(chapter_id: str) -> Optional[Chapter]:
    """
    Retrieve a specific chapter by its ID.
    """
    # This would typically query the database:
    # return db.query(Chapter).filter(Chapter.id == chapter_id).first()
    
    # For now, returning mock data if we recognize the pattern:
    if chapter_id.startswith("mod-") and "-ch" in chapter_id:
        module_id, chapter_num = chapter_id.split("-ch")
        chapter_idx = int(chapter_num) - 1
        
        chapter_titles = {
            "mod-ros2": [
                "Introduction to ROS 2",
                "Nodes and Topics",
                "Practical Examples"
            ],
            "mod-gazebo-unity": [
                "Gazebo Basics",
                "Unity Simulation",
                "Comparison Study"
            ],
            "mod-nvidia-isaac": [
                "Isaac Sim Overview",
                "Robotics Scenarios",
                "Deployment Guide"
            ],
            "mod-vla-systems": [
                "Vision Models",
                "Language Models",
                "Action Planning"
            ]
        }
        
        if module_id in chapter_titles and chapter_idx < len(chapter_titles[module_id]):
            return Chapter(
                id=chapter_id,
                title=chapter_titles[module_id][chapter_idx],
                content="This is placeholder content for the chapter.",
                module=module_id,
                order=chapter_idx+1,
                language="en",
                createdAt="2023-01-01T00:00:00Z",
                updatedAt="2023-01-01T00:00:00Z",
                metadata={}
            )
    
    return None
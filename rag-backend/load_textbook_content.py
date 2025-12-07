import os
import asyncio
from pathlib import Path
import json
from src.services.rag_service import RAGService

async def load_textbook_content_to_rag():
    """
    Load textbook content from the Docusaurus docs directory into the RAG system
    """
    # Initialize the RAG service
    rag_service = RAGService()

    # Define the path to the textbook content using absolute path
    current_dir = Path(__file__).parent
    textbook_path = current_dir / ".." / "textbook" / "docs"
    textbook_path = textbook_path.resolve()  # Convert to absolute path

    print(f"Loading content from: {textbook_path}")

    # Walk through all markdown files in the textbook
    md_files = list(textbook_path.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files to process")

    for md_file in md_files:
        try:
            # Read the content of the markdown file
            content = md_file.read_text(encoding='utf-8')

            # Extract title from the file content (usually first H1 or filename)
            title = extract_title(content, md_file.name)

            # Create a chapter ID based on the file path
            chapter_id = str(md_file.relative_to(textbook_path)).replace("/", "_").replace("\\", "_").replace(".md", "")

            print(f"Indexing chapter: {chapter_id} - {title}")

            # Index the content in the RAG system
            await rag_service.index_textbook_content(
                chapter_id=chapter_id,
                title=title,
                content=content
            )

        except Exception as e:
            print(f"Error processing file {md_file}: {str(e)}")

    print("Textbook content indexing completed!")


def extract_title(content, filename):
    """
    Extract title from markdown content or use filename as fallback
    """
    # Try to get title from the first H1 header
    lines = content.split('\n')
    for line in lines[:10]:  # Check first 10 lines
        if line.strip().startswith('# '):
            return line.strip()[2:]  # Remove '# ' prefix

    # If no H1 header found, use the filename
    return filename.replace('.md', '').replace('_', ' ').title()


if __name__ == "__main__":
    asyncio.run(load_textbook_content_to_rag())
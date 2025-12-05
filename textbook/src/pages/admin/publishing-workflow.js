import React, { useState } from 'react';
import Layout from '@theme/Layout';
import ContentEditor from '@site/src/components/ContentManagement/ContentEditor';
import PublishingWorkflow from '@site/src/components/PublishingWorkflow/PublishingWorkflow';

function PublishingWorkflowPage() {
  const [content, setContent] = useState(`# Sample Content\n\nThis is sample content that can go through the publishing workflow.\n\n## Section 1\n\nSome sample content for the textbook.\n\n## Section 2\n\nMore content to demonstrate the editing and publishing process.`);
  
  const handleContentSave = async (newContent) => {
    // In a real implementation, this would save to the backend
    setContent(newContent);
    console.log('Content saved:', newContent);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    alert('Content saved successfully!');
  };
  
  const handleStatusChange = (newStatus, history) => {
    console.log('Status changed to:', newStatus);
    console.log('New history:', history);
    // In a real app, this would update the content's status in the backend
  };

  return (
    <Layout title="Publishing Workflow" description="Manage the publishing workflow for textbook content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--10 col--offset--1">
            <h1>Publishing Workflow</h1>
            
            <ContentEditor 
              initialContent={content}
              onSave={handleContentSave}
              canEdit={true}
            />
            
            <div className="margin-vert--lg">
              <PublishingWorkflow
                contentId="sample-content-1"
                currentStatus="review"
                onStatusChange={handleStatusChange}
                canPublish={true}
                canReview={true}
              />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default PublishingWorkflowPage;
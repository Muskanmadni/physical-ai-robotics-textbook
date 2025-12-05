import React from 'react';
import Layout from '@theme/Layout';
import ContentManagementToolbar from '@site/src/components/ContentManagement/ContentManagementToolbar';
import PublishingWorkflow from '@site/src/components/PublishingWorkflow/PublishingWorkflow';

function AdminDashboard() {
  const handleEditContent = () => {
    // In a real implementation, this would open the content editor
    alert('Content editing functionality would be implemented here');
  };

  const handleViewHistory = () => {
    // In a real implementation, this would show content history
    alert('Content history would be displayed here');
  };

  const handlePublish = () => {
    // In a real implementation, this would publish content
    alert('Content publishing functionality would be implemented here');
  };

  return (
    <Layout title="Content Creator Dashboard" description="Manage textbook content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset--2">
            <h1>Content Creator Dashboard</h1>
            
            <ContentManagementToolbar 
              chapterId="All"
              moduleId="All"
              onEdit={handleEditContent}
              onViewHistory={handleViewHistory}
              onPublish={handlePublish}
              canEdit={true}
              canPublish={true}
            />
            
            <div className="margin-vert--lg">
              <div className="card">
                <div className="card__header">
                  <h3>Content Management</h3>
                </div>
                <div className="card__body">
                  <p>Use this dashboard to manage textbook content:</p>
                  <ul>
                    <li>Edit existing chapters</li>
                    <li>Create new content</li>
                    <li>Review content history</li>
                    <li>Publish updates</li>
                    <li>View content statistics</li>
                  </ul>
                </div>
              </div>
              
              <div className="margin-vert--lg">
                <h3>Recent Activity</h3>
                <table className="table">
                  <thead>
                    <tr>
                      <th>Chapter</th>
                      <th>Module</th>
                      <th>Last Modified</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Introduction to ROS 2</td>
                      <td>ROS 2</td>
                      <td>Today, 10:30 AM</td>
                      <td>Draft</td>
                      <td>
                        <button className="button button--sm button--primary">Edit</button>
                        <button className="button button--sm button--success margin-left--sm">Publish</button>
                      </td>
                    </tr>
                    <tr>
                      <td>Gazebo Basics</td>
                      <td>Gazebo/Unity Simulation</td>
                      <td>Yesterday, 3:45 PM</td>
                      <td>Published</td>
                      <td>
                        <button className="button button--sm button--primary">Edit</button>
                      </td>
                    </tr>
                    <tr>
                      <td>Vision Models Overview</td>
                      <td>Vision-Language-Action Systems</td>
                      <td>Dec 3, 2025</td>
                      <td>Published</td>
                      <td>
                        <button className="button button--sm button--primary">Edit</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default AdminDashboard;
import React, { useState } from 'react';
import Layout from '@theme/Layout';
import ContentEditor from '@site/src/components/ContentManagement/ContentEditor';

function CreateContent() {
  const [title, setTitle] = useState('');
  const [moduleId, setModuleId] = useState('');
  const [content, setContent] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  
  const modules = [
    { id: 'intro', title: 'Introduction' },
    { id: 'ros2', title: 'ROS 2' },
    { id: 'gazebo-unity', title: 'Gazebo/Unity Simulation' },
    { id: 'nvidia-isaac', title: 'NVIDIA Isaac Robotics' },
    { id: 'vla-systems', title: 'Vision-Language-Action Systems' },
    { id: 'conclusion', title: 'Conclusion' }
  ];

  const handleSave = async (contentToSave) => {
    setIsSaving(true);
    // In a real implementation, this would call the backend API to save content
    console.log('Saving content:', { title, moduleId, content: contentToSave });
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    alert('Content saved successfully!');
    setIsSaving(false);
  };

  return (
    <Layout title="Create New Content" description="Create new textbook content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset--2">
            <h1>Create New Content</h1>
            
            <div className="margin-vert--lg">
              <div className="form-group margin-bottom--md">
                <label htmlFor="title">Content Title</label>
                <input
                  type="text"
                  id="title"
                  className="form-control"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter content title"
                />
              </div>
              
              <div className="form-group margin-bottom--md">
                <label htmlFor="module">Module</label>
                <select
                  id="module"
                  className="form-control"
                  value={moduleId}
                  onChange={(e) => setModuleId(e.target.value)}
                >
                  <option value="">Select a module</option>
                  {modules.map(module => (
                    <option key={module.id} value={module.id}>{module.title}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <ContentEditor 
              initialContent={content}
              onSave={(newContent) => {
                setContent(newContent);
                return handleSave(newContent);
              }}
              canEdit={true}
            />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default CreateContent;
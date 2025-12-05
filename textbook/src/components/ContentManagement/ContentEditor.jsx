import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './ContentEditor.module.css';

// This component provides a simple UI for editing textbook content
// It includes a markdown editor, preview functionality, and save controls
const ContentEditor = ({ initialContent, onSave, canEdit = false }) => {
  const [content, setContent] = useState(initialContent || '');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');

  const handleEdit = () => {
    if (canEdit) {
      setIsEditing(true);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus('Saving...');
    
    try {
      // In a real implementation, this would call the backend API
      await onSave(content);
      setSaveStatus('Saved successfully!');
      setIsEditing(false);
    } catch (error) {
      setSaveStatus('Error saving: ' + error.message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setContent(initialContent);
    setIsEditing(false);
    setSaveStatus('');
  };

  return (
    <div className={styles.contentEditor}>
      <div className={styles.editorHeader}>
        {!isEditing && canEdit && (
          <button 
            className={clsx('button button--secondary', styles.editButton)}
            onClick={handleEdit}
          >
            Edit Content
          </button>
        )}
        
        {isEditing && (
          <div className={styles.editControls}>
            <button 
              className={clsx('button button--success', styles.saveButton)}
              onClick={handleSave}
              disabled={isSaving}
            >
              {isSaving ? 'Saving...' : 'Save'}
            </button>
            <button 
              className={clsx('button button--secondary', styles.cancelButton)}
              onClick={handleCancel}
              disabled={isSaving}
            >
              Cancel
            </button>
          </div>
        )}
        
        {saveStatus && (
          <div className={clsx(
            styles.saveStatus, 
            saveStatus.includes('Error') ? styles.error : styles.success
          )}>
            {saveStatus}
          </div>
        )}
      </div>
      
      <div className={styles.editorContainer}>
        {isEditing ? (
          <textarea
            className={clsx('form-control', styles.textarea)}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={20}
          />
        ) : (
          <div className={styles.contentDisplay}>
            {initialContent ? (
              <div dangerouslySetInnerHTML={{ __html: initialContent }} />
            ) : (
              <p>No content available.</p>
            )}
          </div>
        )}
      </div>
      
      {isEditing && (
        <div className={styles.markdownHelp}>
          <details>
            <summary>Markdown Help</summary>
            <ul>
              <li># Heading 1, ## Heading 2, ### Heading 3</li>
              <li>**bold**, *italic*</li>
              <li>[Link text](url)</li>
              <li>![Alt text](image-url)</li>
              <li>`inline code`, ```code blocks```</li>
              <li>- Unordered lists, 1. Ordered lists</li>
            </ul>
          </details>
        </div>
      )}
    </div>
  );
};

export default ContentEditor;
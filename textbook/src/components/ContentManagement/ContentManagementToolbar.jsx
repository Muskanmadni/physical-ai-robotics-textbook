import React from 'react';
import clsx from 'clsx';
import styles from './ContentManagementToolbar.module.css';

// This component provides a toolbar for content management actions
const ContentManagementToolbar = ({ 
  chapterId, 
  moduleId, 
  onEdit, 
  onViewHistory, 
  onPublish,
  canEdit = false,
  canPublish = false 
}) => {
  return (
    <div className={styles.toolbar}>
      <div className={styles.sectionTitle}>Content Management</div>
      <div className={styles.actions}>
        {canEdit && (
          <button 
            className={clsx('button button--primary', styles.actionButton)}
            onClick={onEdit}
          >
            Edit
          </button>
        )}
        
        <button 
          className={clsx('button button--secondary', styles.actionButton)}
          onClick={onViewHistory}
        >
          View History
        </button>
        
        {canPublish && (
          <button 
            className={clsx('button button--success', styles.actionButton)}
            onClick={onPublish}
          >
            Publish
          </button>
        )}
        
        <div className={styles.info}>
          Chapter: {chapterId || 'N/A'} | Module: {moduleId || 'N/A'}
        </div>
      </div>
    </div>
  );
};

export default ContentManagementToolbar;
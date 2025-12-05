import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import styles from './PublishingWorkflow.module.css';

// This component manages the workflow for publishing content updates
const PublishingWorkflow = ({ 
  contentId, 
  currentStatus = 'draft', 
  onStatusChange,
  canPublish = false,
  canReview = false 
}) => {
  const [status, setStatus] = useState(currentStatus);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [workflowHistory, setWorkflowHistory] = useState([
    { 
      id: 1, 
      status: 'draft', 
      user: 'Content Creator', 
      timestamp: new Date(Date.now() - 86400000).toISOString(), 
      comment: 'Initial draft created' 
    },
    { 
      id: 2, 
      status: 'review', 
      user: 'Content Creator', 
      timestamp: new Date(Date.now() - 43200000).toISOString(), 
      comment: 'Ready for review' 
    }
  ]);
  
  const statusSteps = [
    { id: 'draft', label: 'Draft', description: 'Content is being created' },
    { id: 'review', label: 'Review', description: 'Content under review' },
    { id: 'approved', label: 'Approved', description: 'Content approved for publishing' },
    { id: 'published', label: 'Published', description: 'Content is live' },
    { id: 'archived', label: 'Archived', description: 'Content archived' }
  ];
  
  const currentStepIndex = statusSteps.findIndex(step => step.id === status);
  
  const handlePublish = async () => {
    if (!canPublish) return;
    
    setPublishing(true);
    
    try {
      // In a real implementation, this would call the backend API
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API call
      
      const newStatus = 'published';
      setStatus(newStatus);
      
      // Update workflow history
      const newHistory = [
        ...workflowHistory,
        {
          id: workflowHistory.length + 1,
          status: newStatus,
          user: 'Admin User', // In real app, get from auth context
          timestamp: new Date().toISOString(),
          comment: 'Content published'
        }
      ];
      setWorkflowHistory(newHistory);
      
      // Notify parent component of status change
      if (onStatusChange) {
        onStatusChange(newStatus, newHistory);
      }
    } catch (error) {
      console.error('Error publishing content:', error);
      alert('Error publishing content: ' + error.message);
    } finally {
      setPublishing(false);
      setShowConfirmation(false);
    }
  };

  const handleStatusChange = (newStatus) => {
    if (!canReview && newStatus !== 'published') return; // Only allow publishing if not reviewer
    
    setStatus(newStatus);
    
    // Update workflow history
    const newHistory = [
      ...workflowHistory,
      {
        id: workflowHistory.length + 1,
        status: newStatus,
        user: 'Admin User', // In real app, get from auth context
        timestamp: new Date().toISOString(),
        comment: `Status changed to ${newStatus}`
      }
    ];
    setWorkflowHistory(newHistory);
    
    // Notify parent component of status change
    if (onStatusChange) {
      onStatusChange(newStatus, newHistory);
    }
  };

  return (
    <div className={styles.publishingWorkflow}>
      <div className={styles.workflowHeader}>
        <h3>Publishing Workflow</h3>
        <div className={styles.currentStatus}>
          Current Status: <span className={styles.statusBadge}>{status}</span>
        </div>
      </div>
      
      <div className={styles.workflowSteps}>
        {statusSteps.map((step, index) => (
          <div 
            key={step.id}
            className={clsx(
              styles.step, 
              index <= currentStepIndex && styles.completed,
              status === step.id && styles.active
            )}
          >
            <div className={styles.stepIndicator}>
              {index < currentStepIndex ? (
                <span className={styles.completedIcon}>✓</span>
              ) : (
                <span className={styles.stepNumber}>{index + 1}</span>
              )}
            </div>
            <div className={styles.stepContent}>
              <div className={styles.stepLabel}>{step.label}</div>
              <div className={styles.stepDescription}>{step.description}</div>
            </div>
          </div>
        ))}
      </div>
      
      <div className={styles.workflowActions}>
        {canPublish && status !== 'published' && (
          <button 
            className={clsx('button button--success', styles.publishButton)}
            onClick={() => setShowConfirmation(true)}
            disabled={publishing || status !== 'approved'}
          >
            {publishing ? 'Publishing...' : 'Publish Now'}
          </button>
        )}
        
        {canReview && status !== 'published' && (
          <div className={styles.reviewActions}>
            {status !== 'review' && (
              <button 
                className={clsx('button button--secondary', styles.reviewButton)}
                onClick={() => handleStatusChange('review')}
              >
                Send to Review
              </button>
            )}
            {status !== 'approved' && status === 'review' && (
              <button 
                className={clsx('button button--primary', styles.approveButton)}
                onClick={() => handleStatusChange('approved')}
              >
                Approve
              </button>
            )}
            {status !== 'draft' && status !== 'published' && (
              <button 
                className={clsx('button button--warning', styles.draftButton)}
                onClick={() => handleStatusChange('draft')}
              >
                Send to Draft
              </button>
            )}
          </div>
        )}
      </div>
      
      {showConfirmation && (
        <div className={styles.confirmationModal}>
          <div className={styles.modalContent}>
            <h4>Confirm Publication</h4>
            <p>Are you sure you want to publish this content? This will make it live for all users.</p>
            <div className={styles.modalActions}>
              <button 
                className={clsx('button button--success')}
                onClick={handlePublish}
              >
                Yes, Publish
              </button>
              <button 
                className={clsx('button button--secondary')}
                onClick={() => setShowConfirmation(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
      
      <div className={styles.workflowHistory}>
        <h4>Workflow History</h4>
        <ul className={styles.historyList}>
          {workflowHistory.map((entry) => (
            <li key={entry.id} className={styles.historyItem}>
              <div className={styles.historyStatus}>
                <span className={clsx(styles.statusBadge, styles[`status-${entry.status}`])}>
                  {entry.status}
                </span>
              </div>
              <div className={styles.historyDetails}>
                <div className={styles.historyUser}>by {entry.user}</div>
                <div className={styles.historyTime}>
                  {new Date(entry.timestamp).toLocaleString()}
                </div>
                <div className={styles.historyComment}>{entry.comment}</div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PublishingWorkflow;
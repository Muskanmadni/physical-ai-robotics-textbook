import React from 'react';
import Layout from '@theme/Layout';
import RagChat from '../../components/RagChat/RagChat';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function Chat() {
  const { siteConfig } = useDocusaurusContext();
  
  return (
    <Layout
      title={`Chat - ${siteConfig.title}`}
      description="Chat with the Physical AI & Humanoid Robotics textbook assistant">
      <main>
        <div className="container padding-horiz--md">
          <RagChat />
        </div>
      </main>
    </Layout>
  );
}

export default Chat;